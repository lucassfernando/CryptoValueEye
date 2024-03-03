import sqlite3


class DataBase:

    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    def close(self):
        self.connection.close()

    def create_table(self, table_name, columns_name):
        self.cursor.execute(f'CREATE TABLE {table_name}({columns_name})')

    def insert_data(self, selected_table, selecteds_columns, values):
        place_holders = ', '.join('?' * len(values))
        query = f'INSERT INTO {selected_table} ({selecteds_columns}) VALUES ({place_holders})'
        self.cursor.execute(query, (values))
        self.connection.commit()
    
    def check_column_exist_value(self, table_name, column_name, check_value):
        self.cursor.execute(f"SELECT * FROM {table_name} WHERE {column_name} = {check_value}")
        result = self.cursor.fetchone()
        return result

    def update_values(self, table_name, column_name, new_value, condition_column, condition_value):
        query = f'UPDATE {table_name} SET {column_name} = ? WHERE {condition_column} = ?'
        self.cursor.execute(query, (new_value, condition_value))
        self.connection.commit()
    
    def consult_all_information(self, table_name):
        self.cursor.execute(f'SELECT * FROM {table_name}')
        result = self.cursor.fetchall()
        return result
