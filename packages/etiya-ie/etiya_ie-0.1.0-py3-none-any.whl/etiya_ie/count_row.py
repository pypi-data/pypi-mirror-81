from pyspark.sql import SparkSession
from pyspark.sql.session import SparkSession
from pyspark.context import SparkContext
from pyspark.sql import SQLContext
import findspark
import psycopg2 as pg
import pandas.io.sql as psql
import pandas as pd
import pandasql as ps


class count_row:
    def __init__(self, connection, table_name):
        self.connection = connection
        self.table_name = table_name

    def pandas_count_row(self):
        df = psql.read_sql(f"SELECT *FROM {self.table_name}", self.connection)
        return df.count()[0]

    def sql_count_row(self):
        df = psql.read_sql(f"SELECT *FROM {self.table_name}", self.connection)
        q1 = """SELECT count(*) FROM df """
        return ps.sqldf(q1, locals())

    def psycopg2_count_row(self):
        cursor = self.connection.cursor()
        cursor.execute(f"select count(*) from {self.table_name}")
        return cursor.fetchone()[0]

    def spark_count_row(self,):
        findspark.init()
        sc = SparkContext.getOrCreate()
        spark = SparkSession(sc)
        spark = SparkSession \
            .builder \
            .appName("Python Spark SQL basic example") \
            .getOrCreate()
        df = spark.read \
            .format("jdbc") \
            .option("url", "jdbc:postgresql://"+self.connection.host+":"+str(self.connection.port)+"/"+self.connection.database) \
            .option("dbtable", self.table_name) \
            .option("user", self.connection.user) \
            .option("password", self.connection.password) \
            .option("driver", "org.postgresql.Driver") \
            .load()
        df.printSchema()
        return df.count()
