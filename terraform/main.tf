provider "aws" {
  region = "eu-west-1"
}

locals {
  common_tags = {
    Terraform = "true"
    Environment = "dev"
  }
  environment_name = "gpt4mud"
  current_time = timestamp()
  _ = data.archive_file.lambda_zip
}

resource "aws_dynamodb_table" "game_state" {
  name           = "game-state"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "id"
#   range_key      = "sk"

  attribute {
    name = "id"
    type = "S"
  }

#   attribute {
#     name = "sk"
#     type = "S"
#   }

  tags = local.common_tags
}

resource "aws_iam_role" "lambda_exec" {
  name = "lambda_exec_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })

  tags = local.common_tags
}

resource "aws_iam_role_policy_attachment" "lambda_exec_policy" {
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
  role       = aws_iam_role.lambda_exec.name
}

resource "aws_iam_role_policy_attachment" "lambda_dynamodb_policy" {
  policy_arn = aws_iam_policy.lambda_dynamodb.arn
  role       = aws_iam_role.lambda_exec.name
}

resource "aws_iam_policy" "lambda_dynamodb" {
  name        = "LambdaDynamoDBPolicy"
  path        = "/"
  description = "IAM policy for Lambda to access DynamoDB"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "dynamodb:GetItem",
          "dynamodb:PutItem",
          "dynamodb:UpdateItem",
          "dynamodb:DeleteItem",
          "dynamodb:Query",
          "dynamodb:Scan",
        ]
        Effect   = "Allow"
        Resource = aws_dynamodb_table.game_state.arn
      },
      {
        Action = [
            "execute-api:ManageConnections"
        ]
        Effect = "Allow"
        Resource = [
            "*"
        ]
      }
    ]
  })

  tags = local.common_tags
}

resource "aws_apigatewayv2_api" "websocket" {
  name          = "websocket-api"
  protocol_type = "WEBSOCKET"
  route_selection_expression = "$request.body.action"

  tags = local.common_tags
}

resource "aws_apigatewayv2_integration" "lambda" {
  api_id           = aws_apigatewayv2_api.websocket.id
  integration_type = "AWS_PROXY"

  connection_type      = "INTERNET"
  content_handling_strategy = "CONVERT_TO_TEXT"
  integration_uri = aws_lambda_function.websocket_handler.invoke_arn
}

resource "aws_apigatewayv2_route" "connect" {
  api_id    = aws_apigatewayv2_api.websocket.id
  route_key = "$connect"
  target    = "integrations/${aws_apigatewayv2_integration.lambda.id}"
}

resource "aws_apigatewayv2_route" "disconnect" {
  api_id    = aws_apigatewayv2_api.websocket.id
  route_key = "$disconnect"
  target    = "integrations/${aws_apigatewayv2_integration.lambda.id}"
}

resource "aws_apigatewayv2_route" "route_key" {
  api_id    = aws_apigatewayv2_api.websocket.id
  route_key = "$default"
  target    = "integrations/${aws_apigatewayv2_integration.lambda.id}"
}

resource "aws_apigatewayv2_stage" "production" {
  api_id = aws_apigatewayv2_api.websocket.id
  name   = "production"
  deployment_id = aws_apigatewayv2_deployment.websocket_deployment.id

  access_log_settings {
    destination_arn = aws_cloudwatch_log_group.access_logs.arn
    format          = "$context.identity.sourceIp - - [$context.requestTime] \"$context.httpMethod $context.routeKey $context.protocol\" $context.status $context.responseLength $context.requestId"
  }

  default_route_settings {
    logging_level         = "INFO"
    data_trace_enabled    = true
    throttling_burst_limit = 5000
    throttling_rate_limit  = 10000
  }

  route_settings {
    route_key = "$default"
    logging_level         = "INFO"
    data_trace_enabled    = true
    throttling_burst_limit = 5000
    throttling_rate_limit  = 10000
  }

  lifecycle {
    ignore_changes = [
      # Ignore changes to deployment_id, so that terraform does not redeploy
      # the websocket when configuration changes
      deployment_id
    ]
  }

  depends_on = [aws_apigatewayv2_deployment.websocket_deployment]
  tags = local.common_tags
}

resource "aws_cloudwatch_log_group" "access_logs" {
  name = "/aws/apigateway/${aws_apigatewayv2_api.websocket.name}/access_logs"
}

resource "aws_lambda_function" "websocket_handler" {

  source_code_hash = data.archive_file.lambda_zip.output_md5
  

  function_name    = "websocket_handler"
#   handler          = "websocket_handler.handler"
  handler          = "app.handler"
  runtime          = "python3.9"
  memory_size      = 128
  timeout          = 10
  publish          = true

  role             = aws_iam_role.lambda_exec.arn
  s3_bucket        = aws_s3_bucket_object.lambda_zip.bucket
  s3_key           = aws_s3_bucket_object.lambda_zip.key

  environment {
    variables = {
      DYNAMODB_TABLE = aws_dynamodb_table.game_state.name
      WEBSOCKET_API_ID = aws_apigatewayv2_api.websocket.id
    #   WEBSOCKET_STAGE  = aws_apigatewayv2_stage.production.name
    }
  }

  tags = local.common_tags
}

resource "aws_lambda_permission" "apigateway_invoke" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.websocket_handler.function_name
  principal     = "apigateway.amazonaws.com"

  source_arn = "arn:aws:execute-api:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:${aws_apigatewayv2_api.websocket.id}/*/*"
}

data "aws_region" "current" {}

data "aws_caller_identity" "current" {}

resource "aws_s3_bucket" "lambda_bucket" {
  bucket = "gpt4mud-data"
  acl    = "private"

  tags = local.common_tags
}

resource "null_resource" "create_lambda_zip" {
  triggers = {
    alwaus_run = local.current_time
  }

  provisioner "local-exec" {
    command = "../scripts/build_lambda.sh"
  }
}

resource "null_resource" "cleanup" {
  triggers = {
    alwaus_run = local.current_time
  }

  provisioner "local-exec" {
    command = "../scripts/cleanup.sh"
  }

  depends_on = [
    aws_lambda_function.html_handler,
    aws_lambda_function.websocket_handler,
  ]
}

data "archive_file" "lambda_zip" {
  depends_on = [null_resource.create_lambda_zip]
  type        = "zip"
  source_dir  = "${path.module}/websocket_handler_build"
  output_path = "${path.module}/websocket_handler.zip"
}

resource "aws_s3_bucket_object" "lambda_zip" {

  depends_on = [data.archive_file.lambda_zip, null_resource.create_lambda_zip]

  bucket = aws_s3_bucket.lambda_bucket.id
  key    = "websocket_handler.zip"
  source = "/Users/wlw/Documents/Code/gptmud/gptmud/terraform/websocket_handler.zip"
  etag   = data.archive_file.lambda_zip.output_md5
}

# Lambda for serving index.html
resource "aws_lambda_function" "html_handler" {
  
  source_code_hash = data.archive_file.lambda_zip.output_md5
  function_name = "${local.environment_name}-html-handler"
  description   = "Lambda function to serve index.html"
  runtime       = "python3.9"
  handler       = "app.http_handler"
  role          = aws_iam_role.lambda_exec.arn
  timeout       = 10

  s3_bucket        = aws_s3_bucket_object.lambda_zip.bucket
  s3_key           = aws_s3_bucket_object.lambda_zip.key

  environment {
    variables = {
      WSS_URL = "${aws_apigatewayv2_api.websocket.api_endpoint}/${aws_apigatewayv2_stage.production.name}"
      DYNAMODB_TABLE = aws_dynamodb_table.game_state.name
    }
  }

  tags = local.common_tags
}



# API Gateway REST API for serving index.html
resource "aws_api_gateway_rest_api" "html_api" {
  name        = "${local.environment_name}-html-api"
  description = "REST API for serving index.html"
  tags        = local.common_tags
}

resource "aws_api_gateway_resource" "html_api_resource" {
  rest_api_id = aws_api_gateway_rest_api.html_api.id
  parent_id   = aws_api_gateway_rest_api.html_api.root_resource_id
  path_part   = "index.html"
}

resource "aws_api_gateway_method" "html_api_method" {
  rest_api_id   = aws_api_gateway_rest_api.html_api.id
  resource_id   = aws_api_gateway_resource.html_api_resource.id
  http_method   = "GET"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "html_api_integration" {
  rest_api_id = aws_api_gateway_rest_api.html_api.id
  resource_id = aws_api_gateway_resource.html_api_resource.id
  http_method = aws_api_gateway_method.html_api_method.http_method

  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.html_handler.invoke_arn
}

resource "aws_api_gateway_deployment" "html_api_deployment" {
  depends_on = [aws_api_gateway_integration.html_api_integration]

  rest_api_id = aws_api_gateway_rest_api.html_api.id
  stage_name  = "prod"
}

resource "aws_lambda_permission" "html_api_permission" {
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.html_handler.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gateway_rest_api.html_api.execution_arn}/*/*"
}


# resource "aws_apigatewayv2_api" "websocket_api" {
#   name          = "GPTMUDWebSocketAPI"
#   protocol_type = "WEBSOCKET"
# }

resource "aws_apigatewayv2_deployment" "websocket_deployment" {
  api_id      = aws_apigatewayv2_api.websocket.id
  description = "WebSocket API deployment"

  depends_on = [
    aws_apigatewayv2_route.connect,
    aws_apigatewayv2_route.disconnect,
    aws_apigatewayv2_route.route_key
  ]
}

# resource "aws_apigatewayv2_stage" "websocket_stage" {
#   api_id     = aws_apigatewayv2_api.websocket_api.id
#   deployment_id = aws_apigatewayv2_deployment.websocket_deployment.id
#   name       = "prod"
# }

# resource "aws_apigatewayv2_integration" "websocket_integration_connect" {
#   api_id           = aws_apigatewayv2_api.websocket_api.id
#   integration_type = "AWS_PROXY"
#   connection_type  = "INTERNET"

#   integration_uri = aws_lambda_function.websocket_handler.invoke_arn
#   passthrough_behavior = "WHEN_NO_MATCH"
# }

# resource "aws_apigatewayv2_integration" "websocket_integration_disconnect" {
#   api_id           = aws_apigatewayv2_api.websocket_api.id
#   integration_type = "AWS_PROXY"
#   connection_type  = "INTERNET"

#   integration_uri = aws_lambda_function.websocket_handler.invoke_arn
#   passthrough_behavior = "WHEN_NO_MATCH"
# }

# resource "aws_apigatewayv2_integration" "websocket_integration_route_key" {
#   api_id           = aws_apigatewayv2_api.websocket_api.id
#   integration_type = "AWS_PROXY"
#   connection_type  = "INTERNET"

#   integration_uri = aws_lambda_function.websocket_handler.invoke_arn
#   passthrough_behavior = "WHEN_NO_MATCH"
# }

# resource "aws_apigatewayv2_route" "connect_route" {
#   api_id = aws_apigatewayv2_api.websocket_api.id
#   route_key = "$connect"
#   target     = "integrations/${aws_apigatewayv2_integration.websocket_integration_connect.id}"
# }

# resource "aws_apigatewayv2_route" "disconnect_route" {
#   api_id = aws_apigatewayv2_api.websocket_api.id
#   route_key = "$disconnect"
#   target     = "integrations/${aws_apigatewayv2_integration.websocket_integration_disconnect.id}"
# }

# resource "aws_apigatewayv2_route" "route_key_route" {
#   api_id = aws_apigatewayv2_api.websocket_api.id
#   route_key = "message"
#   target     = "integrations/${aws_apigatewayv2_integration.websocket_integration_route_key.id}"
# }

resource "aws_iam_role" "apigw_cloudwatch_logs_role" {
  name = "apigw-cloudwatch-logs-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "apigateway.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy" "apigw_cloudwatch_logs_policy" {
  name = "apigw-cloudwatch-logs-policy"
  role = aws_iam_role.apigw_cloudwatch_logs_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:DescribeLogGroups",
          "logs:DescribeLogStreams",
          "logs:PutLogEvents",
          "logs:GetLogEvents",
          "logs:FilterLogEvents",
          "execute-api:ManageConnections"
        ]
        Effect   = "Allow"
        Resource = "*"
      }
    ]
  })
}



output "html_api_url" {
  description = "The URL of the API Gateway REST API serving index.html"
  value = "https://${aws_api_gateway_rest_api.html_api.id}.execute-api.${var.aws_region}.amazonaws.com/prod/index.html"
}

output "websocket_api_url" {
  description = "The WebSocket API URL for your game"
  value = "wss://${aws_apigatewayv2_api.websocket.api_endpoint}/${aws_apigatewayv2_stage.production.name}"
}