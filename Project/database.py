import sqlite3




class Database:
    def __init__(self, databasename):
        self.dbname=databasename



    def create_table (self, table_name, statement):
        con = sqlite3.connect(self.dbname)
        c = con.cursor()
        c.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({statement})")
        con.commit()
        con.close()

    def insert_data (self, table_name, value: list):
        value_string=""
        for i in value:
            value_string += i + ","

        value_string = value_string[:-1]
        con = sqlite3.connect(self.dbname)
        c = con.cursor()
        c.execute(f"INSERT INTO {table_name} VALUES ({value_string})")
        con.commit()
        con.close()

    # def get_data()