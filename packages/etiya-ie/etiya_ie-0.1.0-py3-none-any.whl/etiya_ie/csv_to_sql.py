import psycopg2 as pg
import pandas.io.sql as psql
import pandas as pd


class csv_to_sql:
    def __init__(self, connection):
        self.connection = connection

    def create_table(self, table_name, df):
        cursor = self.connection.cursor()
        query = list(df)[0] + " serial primary key,"
        for name, t in zip(list(df)[1:], list(df.dtypes)[1:]):
            query += name + " "
            if 'int' in t:
                query += "int not null"
            elif t == "object":
                query += "varchar(255) not null"
            else:
                query += "varchar(255) not null"
        query = " (" + query + ");"
        create_table = "create table " + table_name + query
        cursor.execute(create_table)
        self.connection.commit()

    def insert_data_many(self, table_name, df):
        try:
            cursor = self.connection.cursor()
            rows = []
            for index, row in df.iterrows():
                rows.append(list(row))
            cursor.executemany(
                f"INSERT INTO {table_name}({','.join(list(df))}) VALUES ({','.join(['%s']*len(list(df)))})", rows)
            self.connection.commit()
            count = cursor.rowcount
            print(count, "Inserted -executemany- succesfully")
        except (Exception, pg.Error) as error:
            if(self.connection):
                print("Failed to insert record into mobile table", error)

    def insert_data_batch(self, table_name, df):
        try:
            cursor = self.connection.cursor()
            rows = []
            for index, row in df.iterrows():
                rows.append(list(row))
            query = f"INSERT INTO {table_name}({','.join(list(df))}) VALUES ({','.join(['%s']*len(list(df)))})"
            pg.extras.execute_batch(cursor, query, rows)
            self.connection.commit()
            print("Inserted -executebatch- succesfully")
        except (Exception, pg.Error) as error:
            if(self.connection):
                print("Failed to insert record into mobile table", error)

    def delete_student(self, table_name, _id):
        try:
            cursor = self.connection.cursor()
            cursor.execute("DELETE FROM " + table_name +
                           " WHERE _id = (%s)", (_id, ))
            self.connection.commit()
            count = cursor.rowcount
            print(count, "Deleted succesfully")
        except (Exception, pg.Error) as error:
            if(self.connection):
                print("Failed to delete record into mobile table", error)

    def update_column(self, table_name, _id, column_name, new_value):
        try:
            cursor = self.connection.cursor()
            cursor.execute("UPDATE "+table_name +
                           " SET (%s) = (%s) where _id = (%s)", (column_name, new_value, _id))
            self.connection.commit()
            count = cursor.rowcount
            print(count, "Updated succesfully")
        except (Exception, pg.Error) as error:
            if(self.connection):
                print("Failed to update record into mobile table", error)
