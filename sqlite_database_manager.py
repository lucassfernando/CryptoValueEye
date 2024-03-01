import sqlite3


class DataBase:

    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    def close(self):
        self.connection.close()

    def create_table(self, table_name, table_columns):
        self.cursor.execute(f'CREATE TABLE {table_name}({table_columns})')

    def insert_data(self, selected_table, selecteds_columns, values):
        place_holders = ', '.join('?' * len(values))
        query = f'INSERT INTO {selected_table} ({selecteds_columns}) VALUES ({place_holders})'
        self.cursor.execute(query, (values))
        self.connection.commit()
    
    def check_column_exist_value(self, table_name, column, check_value):
        self.cursor.execute(f"SELECT * FROM {table_name} WHERE {column} = '{check_value}'")
        result = self.cursor.fetchone()
        return result

