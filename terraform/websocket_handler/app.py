import os
import json
import boto3
import logging
from game.core import Game

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())

table_name = os.getenv("DYNAMODB_TABLE")
wss_url = os.getenv("WSS_URL")

logger.info(f"table_name: {table_name}")
logger.info(f"wss_url: {wss_url}")

def send_message(connection_id, message):
    gateway_api = boto3.client("apigatewaymanagementapi",
                               endpoint_url=f"https://{os.environ['WEBSOCKET_API_ID']}.execute-api.{os.environ['AWS_REGION']}.amazonaws.com/production")
    gateway_api.post_to_connection(ConnectionId=connection_id, Data=message)


def load_game_state():
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(table_name)
    response = table.get_item(Key={"id": "game_state"})
    if "Item" in response:
        game_state = json.loads(response["Item"]["state"])
        game = Game.from_dict(game_state)
        return game
    else:
        game = Game()
        save_game_state(game)
        return game

def save_game_state(game):
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(table_name)
    game_state = game.to_dict()
    logger.debug(f"Saving game state: {game_state}")
    table.put_item(Item={"id": "game_state", "state": json.dumps(game_state)})

def on_connect(event, context):
    game = load_game_state()
    game.add_player(event["requestContext"]["connectionId"])
    # ... (Handle new connection, update game state if necessary)
    save_game_state(game)

def on_disconnect(event, context):
    game = load_game_state()
    game.remove_player(event["requestContext"]["connectionId"])
    # ... (Handle disconnection, update game state if necessary)
    save_game_state(game)

def on_message(event, context):
    game = load_game_state()
    connection_id = event["requestContext"]["connectionId"]
    message = event["body"]
    reply = game.process_command(connection_id, message)
    send_message(connection_id, reply)
    save_game_state(game)

def handler(event, context):
    logger.debug(f"Event: {event}")
    logger.debug(f"Context: {context}")
    route_key = event["requestContext"]["routeKey"]
    connection_id = event["requestContext"]["connectionId"]
    event_type = event["requestContext"]["eventType"]
    
    if event_type == "MESSAGE":
        # send_message(connection_id, "Got it!")
        on_message(event, context)
    
    elif event_type == "DISCONNECT":
        # send_message(connection_id, "Goodbye!")
        on_disconnect(event, context)

    elif event_type == "CONNECT":
        on_connect(event, context)
        
    
    return {
        "statusCode": 200
    }

    if route_key == "$connect":
        return on_connect(event, context)
    elif route_key == "$disconnect":
        return on_disconnect(event, context)
    elif route_key == "sendmessage":
        return on_message(event, context)

def http_handler(event, context):
    with open(os.path.join(os.path.dirname(__file__), 'templates/index.html'), 'r') as f:
        content = f.read()

    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'text/html'
        },
        'body': content.replace('{{wss_url}}', wss_url)
    }