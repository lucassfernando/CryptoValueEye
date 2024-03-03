import requests
import json
import threading
from time import sleep
import decimal


headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'}


def parse_float(val):
    return decimal.Decimal(val)

r = requests.get('https://api.coinmarketcap.com/data-api/v3.1/cryptocurrency/historical?id=16389&interval=1h&convertId=2781', headers=headers)


if 'open' and 'close' in r.text:
    a = json.loads(r.text, parse_float=parse_float)
    print(a)
else:
    print(r.text)