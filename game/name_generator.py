import random

PREFIXES = [
    'Ael', 'Aer', 'Af', 'Al', 'An', 'Ar', 'Bar', 'Bel', 'Bon',
    'Cal', 'Cel', 'Cor', 'Dae', 'Dal', 'Del', 'Dor', 'Eir', 'El',
    'Eli', 'Eol', 'Eri', 'Far', 'Fen', 'Fer', 'Fin', 'Fol', 'Gel',
    'Gor', 'Gre', 'Gul', 'Har', 'Hel', 'Hor', 'Iri', 'Kan', 'Kel',
    'Ker', 'Kil', 'Lan', 'Lar', 'Lor', 'Mar', 'Mel', 'Mor', 'Nar',
    'Nel', 'Nor', 'Ori', 'Orl', 'Por', 'Raf', 'Ral', 'Rel', 'Ril',
    'Sal', 'Sel', 'Sil', 'Sol', 'Tal', 'Tel', 'Tor', 'Ty', 'Ul', 'Uri'
]

ROOTS = [
    'ad', 'aed', 'ael', 'aer', 'ai', 'ail', 'ain', 'air', 'al',
    'am', 'an', 'ao', 'ar', 'ath', 'ay', 'dal', 'dar', 'del', 'den',
    'dra', 'du', 'dul', 'dur', 'ean', 'ed', 'eid', 'eil', 'ein',
    'el', 'em', 'en', 'er', 'ess', 'est', 'eth', 'il', 'im', 'in',
    'ir', 'is', 'iss', 'ist', 'ith', 'lan', 'lar', 'lin', 'lor', 'ly',
    'ma', 'man', 'mar', 'mel', 'men', 'mi', 'mo', 'na', 'nar', 'nen',
    'ni', 'no', 'ol', 'om', 'on', 'or', 'oth', 'ra', 'rad', 'rak',
    'ral', 'ran', 'ras', 'rath', 'rav', 'ray', 'ri', 'ril', 'rim',
    'rin', 'ris', 'rod', 'rok', 'rol', 'rom', 'ron', 'ros', 'roth',
    'rov', 'ry', 'sa', 'sar', 'sel', 'sen', 'ser', 'sor', 'syl', 'ta',
    'tan', 'tas', 'tay', 'tel', 'ther', 'thi', 'tho', 'thor', 'thu',
    'tir', 'tis', 'to', 'tor', 'tur', 'ty', 'va', 'val', 'van', 'var',
    'ven', 'vin', 'vor', 'vyn', 'wa', 'war', 'wen', 'win', 'wor', 'wyn'
]

SUFFIXES = [
    'a', 'ace', 'ae', 'ael', 'af', 'ah', 'al', 'all', 'am',
    'an', 'ar', 'ard', 'as', 'ath', 'ay', 'e', 'el', 'em', 'en',
    'er', 'ess', 'est', 'eth', 'i', 'ia', 'ian', 'il', 'im', 'in',
    'ir', 'is', 'ish', 'ist', 'ith', 'ius', 'o', 'oa', 'od', 'oe',
    'of', 'oh', 'ol', 'om', 'on', 'or', 'os', 'ot', 'oth', 'ou',
    'ow', 'u', 'um', 'un', 'ur', 'us', 'ut', 'uth', 'y', 'yr'
]

def generate_name():
    prefix = random.choice(PREFIXES)
    root = random.choice(ROOTS)
    suffix = random.choice(SUFFIXES)
    return f"{prefix}{root}{suffix}"


