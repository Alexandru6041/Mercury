import sqlite3

class Database(object):
    def __init__(self, PATH, cursor, sqliteConnection):
        self.PATH = PATH
        self.sqliteConnection = sqliteConnection
        self.cursor = cursor

    def __createconnection(self):
        try:
            self.sqliteConnection = sqlite3.connect(self.PATH)
            self.cursor = self.sqliteConnection.cursor()

        except sqlite3.Error as e:
            print(e)

    def __closeconnection(self):
        return self.sqliteConnection.close()

    def InsertData(self, table_to, data):
        self.__createconnection()

        if(self.__lookUpData(table_to, data) == True):
            return None

        try:
            self.cursor.execute(f"INSERT INTO {table_to} VALUES (?)", [data])
            self.sqliteConnection.commit()
            print(
                f"{data} successfully added to database: {self.PATH} \ntable_name: {table_to}")
        except Exception as e:
            print(e)

        self.__closeconnection()

    def DeleteData(self, table_from, data, condition: str = ""):
        self.__createconnection()

        if(self.__lookUpData(table_from, data) == False):
            return None
        try:
            self.cursor.execute(
                f"DELETE FROM {table_from} {condition}", [data])
            self.sqliteConnection.commit()
            print(
                f"{data} successfully removed from database: {self.PATH} \ntable_name: {table_from}")
        except Exception as e:
            print(e)

    def SelectData(self, table_from):
        self.__createconnection()

        try:
            self.cursor.execute(f"SELECT * FROM {table_from}")
            data = self.cursor.fetchall()

            return data
        except Exception as e:
            print(e)

        self.__closeconnection()

    def __lookUpData(self, table_from, data):
        self.__createconnection()

        try:
            self.cursor.execute(f"SELECT * FROM {table_from}")
            data_look = self.cursor.fetchall()
            self.sqliteConnection.commit()

            for i in range(len(data_look)):
                for row in data_look:
                    if row[i] == data:
                        self.__closeconnection()
                        return True
        except IndexError:
            self.__closeconnection()
            return False

    def Createdatabase(self, table_name, rows: str):
        self.__createconnection()

        try:
            Data_Table = f""" CREATE TABLE {table_name} ({rows}) """
            self.cursor.execute(Data_Table)
        except Exception as e:
            print(e)

        self.__closeconnection()
        print(
            f"\nDatabase Created: \nPath: {self.PATH} \nTable_Name: {table_name}, \nRows: {rows}")

    def find(self, table_from, data):
        return self.__lookUpData(table_from, data)
