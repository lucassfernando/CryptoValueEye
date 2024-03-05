import requests
import decimal
from time import sleep
import json
import threading

from sqlite_database_manager import DataBase

def percentage_calculated(initial_value, final_value):

    if final_value > initial_value:

        subtracting_values = final_value - initial_value
        percentage_value = (subtracting_values / initial_value) * 100
        return 'high', percentage_value

    else:
        
        subtracting_values = initial_value - final_value
        percentage_value = (subtracting_values / initial_value) * 100
        return 'low', percentage_value

def parse_float(val):

    return decimal.Decimal(val)

def start_check(cripto_id):

    try:

        request = requests.get(f'https://api.coinmarketcap.com/data-api/v3.1/cryptocurrency/historical?id={cripto_id}&interval=1h&convertId=2781')
        
        if 'open' and 'close' in request.text:

            json_converted = json.loads(request.text, parse_float=parse_float)
            #ABAIXO POSSO SELECIONAR QUALQUER PERIODO NO INTERVALO DE UMA HORA QUE EU QUISER, ENTÃO CONSIGO PEGAR O DE 6 HORAS SELECIONANDO -6 E COMPARANDO COM 1 HORA ATRAS PARA SABER A PORCENTAGEM
            opened_cripto_value = json_converted['data']['quotes'][-1]['quote']['open'] 
            closed_cripto_value = json_converted['data']['quotes'][-1]['quote']['close']  
            high_or_low, percentage_value = percentage_calculated(float(opened_cripto_value), float(closed_cripto_value))

            if high_or_low == 'high' and percentage_value >= 6.25:
                print(f"CRIPTO: {cripto_id} = {opened_cripto_value} {closed_cripto_value} {round(percentage_value, 2)} {high_or_low}")

    except Exception as erro:

        print(erro)

db = DataBase('CRIPTOS_INFO.db')
all_cripto_data = db.consult_all_information('CRIPTOS_COINMARKETCAP')
db.close()

for information in all_cripto_data:

    thread = threading.Thread(target=start_check, args=(information[2],))
    thread.start()
    sleep(0.2)