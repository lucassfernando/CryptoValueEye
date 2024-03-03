import requests
import decimal
from time import sleep
import json
import threading

from sqlite_database_manager import DataBase

def procentage_calculated(initial_value, final_value):

    if final_value > initial_value:

        subtracting_values = final_value - initial_value
        percentage_value = (subtracting_values / initial_value) * 100
        return 'high', "%.2f" % percentage_value

    else:
        
        subtracting_values = initial_value - final_value
        percentage_value = (subtracting_values / initial_value) * 100
        return 'low', "%.2f" % percentage_value

def parse_float(val):

    return decimal.Decimal(val)


def start_check(cripto_id):

    try:
        request = requests.get(f'https://api.coinmarketcap.com/data-api/v3.1/cryptocurrency/historical?id={cripto_id}&interval=1h&convertId=2781')
    except Exception as erro:
        print(erro)

        #COLOCAR UM DB COM LOGs DE ERRO
    
    if 'open' and 'close' in request.text:

        json_converted = json.loads(request.text, parse_float=parse_float)
        closed_cripto_value = json_converted['data']['quotes'][-1]['quote']['close']
        db = DataBase('CRIPTOS_INFO.db')
        db.update_values('CRIPTOS_COINMARKETCAP', 'VALUE_1H', str(closed_cripto_value), 'ID_COINMARKETCAP', information[2])
        db.close()

db = DataBase('CRIPTOS_INFO.db')
all_cripto_data = db.consult_all_information('CRIPTOS_COINMARKETCAP')
db.close()

for information in all_cripto_data:
    
    thread = threading.Thread(target=start_check, args=(information[2],))
    thread.start()
    sleep(0.3)