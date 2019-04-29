import psycopg2


def get_db_connection():
    connection = psycopg2.connect("dbname='Transport' "
                                  "user='postgres' "
                                  "host='localhost' "
                                  "port='5639' "
                                  "password='secret'")
    return connection
