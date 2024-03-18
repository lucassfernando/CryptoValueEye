import requests
import decimal
from time import sleep
import json
import threading
import logging

from sqlite_database_manager import DataBase
from telegram_manager import BotTelegram
from db_construction import update_reference_db_coinmarketcap



def monitor_climb(json, hours_ago, selected_percentage, return_text):

    opened_cripto_value = json['data']['quotes'][hours_ago]['quote']['open'] 
    closed_cripto_value = json['data']['quotes'][-1]['quote']['close']  
    high_percentage = percentage_calculated(float(opened_cripto_value), float(closed_cripto_value))

    if high_percentage >= selected_percentage:
        return f'{return_text}: {"%.2f" % high_percentage}% ✅'
    else:
        return f'{return_text}: {"%.2f" % high_percentage}% ❌'

def percentage_calculated(initial_value, final_value):

    if final_value > initial_value:

        subtracting_values = final_value - initial_value
        percentage_value = (subtracting_values / initial_value) * 100
        return percentage_value


def parse_float(val):

    return decimal.Decimal(val)


def start_check(cripto_id, cripto_name):

    try:

        request = requests.get(f'https://api.coinmarketcap.com/data-api/v3.1/cryptocurrency/historical?id={cripto_id}&interval=1h&convertId=2781')
        
        if 'open' and 'close' in request.text:

            json_converted = json.loads(request.text, parse_float=parse_float)

            return_analyze_1h = monitor_climb(json_converted, -1, 10.00, '1H')
            return_analyze_2h = monitor_climb(json_converted, -2, 20.00, '2H')
            return_analyze_3h = monitor_climb(json_converted, -3, 30.00, '3H')
            return_analyze_6h = monitor_climb(json_converted, -6, 55.00, '6H')
            return_analyze_total = f'{return_analyze_1h}\n{return_analyze_2h}\n{return_analyze_3h}\n{return_analyze_6h}'
            
            if '✅' in return_analyze_total:

                bot.send_message(-4148057761, f"TOKEN: {cripto_name}\n\n{return_analyze_total}")

    except Exception as erro:

        logging.error(f'analyze crypto {cripto_name} | error: {error}')

bot = BotTelegram()
logging.basicConfig(level=logging.DEBUG, filename='register.log', format='%(asctime)s - %(levelname)s - %(message)s')

while True:

    try:

        logging.debug('init database update')
        tokens_added = update_reference_db_coinmarketcap()

        if int(tokens_added) > 0:
            bot.send_message(-4148057761, f'TOKENS ADDED IN DATABASE: {tokens_added}')

        logging.debug('finishing database update')
    
    except Exception as error:
        
        logging.error(f'error database update: {error}')

    db = DataBase('CRIPTOS_INFO.db')
    all_cripto_data = db.consult_all_information('CRIPTOS_COINMARKETCAP')
    db.close()
    logging.debug('function consult_all_information concluded')

    try:

        for information in all_cripto_data:

            thread = threading.Thread(target=start_check, args=(information[2], information[0],))
            thread.start()
            sleep(0.2)
    
    except Exception as error:

        logging.error(f'threading error in crypto: {information[0]} | error: {error}')