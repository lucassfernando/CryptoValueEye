import requests
import json
import threading

from sqlite_database_manager import DataBase


def db_model_coinmarketcap():

    db = DataBase('CRIPTOS_INFO.db')

    db.create_table('CRIPTOS_COINMARKETCAP', '''NAME, SIGLE, ID_COINMARKETCAP, VALUE_1H, VALUE_6H, VALUE_12H, VALUE_24H, 
                    PERCENTAGE_1H, PERCENTAGE_6H, PERCENTAGE_12H, PERCENTAGE_24H, LAST_ANALYSIS, DB_REGISTER_DATE''')
    
    db.close()

def update_reference_db_coinmarketcap():

    db = DataBase('CRIPTOS_INFO.db')
    request = requests.get('https://api.coinmarketcap.com/data-api/v3/cryptocurrency/listing?start=1&limit=30000')
    request_json = json.loads(request.text)
    count = 0

    for cripto in request_json['data']['cryptoCurrencyList']:

        cripto_id = cripto['id']
        check_cripto = db.check_column_exist_value('CRIPTOS_COINMARKETCAP', 'ID_COINMARKETCAP', cripto_id)
        
        if check_cripto:
            
            continue

        else:

            db.insert_data('CRIPTOS_COINMARKETCAP', 'NAME, SIGLE, ID_COINMARKETCAP', (cripto['name'], cripto['symbol'], cripto['id']))
            count += 1
            print(cripto['name'], count)
            
    print(f"TOTAL CADASTRADO: {count}")

