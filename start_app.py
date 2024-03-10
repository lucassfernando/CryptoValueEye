import requests
import decimal
from time import sleep
import json
import threading

from sqlite_database_manager import DataBase



def monitor_climb(json, hours_ago, selected_percentage, return_text):

    opened_cripto_value = json['data']['quotes'][hours_ago]['quote']['open'] 
    closed_cripto_value = json['data']['quotes'][-1]['quote']['close']  
    high_percentage = percentage_calculated(float(opened_cripto_value), float(closed_cripto_value))

    if high_percentage >= selected_percentage:
        return f'{return_text}: {high_percentage}'


def percentage_calculated(initial_value, final_value):

    if final_value > initial_value:

        subtracting_values = final_value - initial_value
        percentage_value = (subtracting_values / initial_value) * 100
        return percentage_value


def parse_float(val):

    return decimal.Decimal(val)


def start_check(cripto_id):

    try:

        request = requests.get(f'https://api.coinmarketcap.com/data-api/v3.1/cryptocurrency/historical?id={cripto_id}&interval=1h&convertId=2781')
        
        if 'open' and 'close' in request.text:

            json_converted = json.loads(request.text, parse_float=parse_float)
            return_analyze = monitor_climb(json_converted, -1, 8.00, '1H')
            
            if return_analyze:
                print(return_analyze, cripto_id)

    except Exception as erro:

        pass

db = DataBase('CRIPTOS_INFO.db')
all_cripto_data = db.consult_all_information('CRIPTOS_COINMARKETCAP')
db.close()

for information in all_cripto_data:

    thread = threading.Thread(target=start_check, args=(information[2],))
    thread.start()
    sleep(0.2)