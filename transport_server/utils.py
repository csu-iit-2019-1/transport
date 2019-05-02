import logging
import traceback

import psycopg2


def get_db_connection():
    connection = psycopg2.connect("dbname='Transport' "
                                  "user='postgres' "
                                  "host='localhost' "
                                  "port='5432' "
                                  "password='secret'")
    return connection


def get_logs_connection():
    connection = psycopg2.connect("dbname='Logs' "
                                  "user='postgres' "
                                  "host='localhost' "
                                  "port='5432' "
                                  "password='secret'")
    return connection


class psqlHandler(logging.Handler):
    insertion_sql = """INSERT INTO "Logs"("Time", "Name", "Status", "Message") VALUES (
                            %(asctime)s,
                            %(name)s,
                            %(levelname)s,
                            %(message)s
                    );"""

    def connect(self):
        try:
            self.__connect = psycopg2.connect(
                database=self.__database,
                host=self.__host,
                user=self.__user,
                password=self.__password,
                port=self.__port)

            return True
        except:
            return False

    def __init__(self, params):

        if not params:
            raise Exception("No database where to log ☻")

        self.__database = params['database']
        self.__host = params['host']
        self.__user = params['user']
        self.__password = params['password']
        self.__port = params['port']

        self.__connect = None

        if not self.connect():
            raise Exception("Database connection error, no logging ☻")

        logging.Handler.__init__(self)

    def emit(self, record):

        # Use default formatting:
        self.format(record)

        if record.exc_info:
            record.exc_text = logging._defaultFormatter.formatException(record.exc_info)
        else:
            record.exc_text = ""

        # Insert log record:
        try:
            cur = self.__connect.cursor()
        except:
            self.connect()
            cur = self.__connect.cursor()

        cur.execute(psqlHandler.insertion_sql, record.__dict__)

        self.__connect.commit()
        self.__connect.cursor().close()
