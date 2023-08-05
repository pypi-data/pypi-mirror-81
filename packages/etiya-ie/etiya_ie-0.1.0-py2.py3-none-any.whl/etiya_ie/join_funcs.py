import pandas as pd
import psycopg2


class join_funcs:
    def __init__(self, conn, tables):
        self.connection = conn
        self.tables = tables

    def join(self):
        m = pd.DataFrame()
        for table_name, suffixs in self.tables.items():
            df = pd.read_sql_query(
                "select * from {}".format(table_name), self.connection)
            m = df if m.empty else m.join(
                df, lsuffix=suffixs['lsuffix'], rsuffix=suffixs['rsuffix'])
        return m
