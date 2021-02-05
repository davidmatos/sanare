#import psycopg2 # PostgreSQL adapter for Python
import asyncio
#import configparser
import json
from pymongo import MongoClient
from datetime import datetime


# Create a config.ini file having database credentials and the port number.
#CONFIG = configparser.ConfigParser()
#CONFIG.read("config.ini")

#TCP_PORT = int(CONFIG["RSYSLOG"]["FORWARD_PORT"])


DB_INSTANCE = None
def get_db():
    global DB_INSTANCE
    if DB_INSTANCE is None:
        client = MongoClient('mongodb://10.1.0.101:27017')
        DB_INSTANCE = client.sanare
    return DB_INSTANCE


# try:
#     credentials = {
#         "host": CONFIG["POSTGRESQL"]["DB_HOST"],
#         "port": int(CONFIG["POSTGRESQL"]["DB_PORT"]),
#         "database": CONFIG["POSTGRESQL"]["DB_NAME"],
#         "user": CONFIG["POSTGRESQL"]["DB_USER"],
#         "password": CONFIG["POSTGRESQL"]["DB_PASSWORD"]
#     }
#     CONN = psycopg2.connect(**credentials)
#     CURSOR = CONN.cursor()
# except:
#     print("Unable to connect to the database")
#     quit()

# INSERT_QUERY = "INSERT INTO access_log (log_line, created_at) VALUES (%s, %s);"


# def execute_sql(params):
#     try:
#         CURSOR.execute(INSERT_QUERY, params)
#         CURSOR.close()
#         CONN.commit()
#     except Exception as e:
#         CONN.rollback()
#         raise e

def insert_log_entry(httplogentry):
    db = get_db()
    httplogentries = db.httplogentries
    httplogentries.insert_one(httplogentry)


class LogAnalyser:

    def __init__(self):
        pass

    # def process(self, str_input):
    #     str_input = str_input.decode("utf-8", errors="ignore")
    #     # Add your processing steps here
    #     # ...
    #     try:
    #         # Extract created_at from the log string
    #         str_splits = str_input.split("{", 1)
    #         json_text = "{" + str_splits[1]
    #         data = json.loads(json_text)
    #         created_at = data["time"]
    #         log_line = json_text
    #         return log_line, created_at # The order is relevant for INSERT query params
    #     except Exception as e:
    #         print(e)
    #     return None


@asyncio.coroutine
def handle_echo(reader, writer):
    # log_filter = LogAnalyser()
    while True:
        line = yield from reader.readline()
        if not line:
            break
        try:
            line = line.decode("utf-8", errors="ignore")
            print(line)
            str_splits = line.split("{")
            json_text = "{" + str_splits[1]
            data = json.loads(json_text)
            insert_log_entry(data)
        except Exception as e:
            print(e)


loop = asyncio.get_event_loop()
coro = asyncio.start_server(handle_echo, '127.0.0.1', 6000, loop=loop)
server = loop.run_until_complete(coro)

# Serve requests until Ctrl+C is pressed
print('Serving on {}'.format(server.sockets[0].getsockname()))
try:
    loop.run_forever()
except KeyboardInterrupt:
    pass

# Close the server
print("Closing the server.")
server.close()
loop.run_until_complete(server.wait_closed())
loop.close()
# CURSOR.close()
# CONN.close()