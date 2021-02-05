import datetime  
import mysql.connector
import pymongo
import requests
import json
import time
import random
import string


def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

mydb = mysql.connector.connect(
  host="127.0.0.1",
  port=3306,
  database="wordpress",
  user="root",
  password="somewordpress"
)

mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
sanare_log = mongo_client["sanare"]
httplogentries = sanare_log["httplogentries"]

def getHttpLog(time):
    #Get the HTTP logs from sanare-log (which is a mongo database)
    x = httplogentries.find_one(sort=[( '_id', pymongo.DESCENDING )])
    return x

def getDbLogEntries(time_str):

    cursor = mydb.cursor()
    sql_query = "select event_time, user_host, command_type, convert(argument using utf8) as query from mysql.general_log where event_time >= '"+time_str+"'"
    cursor.execute(sql_query)
    rows = cursor.fetchall()
    print("Found " + str(len(rows)) + " db log entries ")
    for row in rows:
      print(row)



with open('endpoints.json') as json_file:
    endpoints = json.load(json_file)
    host = endpoints["host"]
    port = endpoints["port"]
    for endpoint in endpoints['endpoints']:
        current_time = datetime.datetime.now() #- datetime.timedelta(seconds=2)
        time_str = current_time.strftime('%Y-%m-%d %H:%M:%S')
        print(endpoint['desc'] + " - " + time_str)
        print("   uri: " + endpoint['uri'])
        print("   method: " + endpoint['method'])
        print("   params: " + str(endpoint['params']))
        print("--------------------------------------------------------")
        time.sleep(1)

        for key, value in endpoint['params'].items():
            if(endpoint['params'][key] == '<random>'):
                endpoint['params'][key] = get_random_string(6)

        print(str(endpoint['params']))

        url = host + ":" + str(port) + endpoint['uri']

        if(endpoint['method'] == "GET"):
            print("Executing GET to " + endpoint['uri'])
            r = requests.get(url) 
            print("-")

        if(endpoint['method'] == "POST"):
            print("Executing POST to " + endpoint['uri'])
            r = requests.post(url, data = endpoint['params']) 
            print("-")
            #exit
            
        #print(r)

        #give it time to generate the logs
        time.sleep(3)

        #request performed, now we get the HTTP log and the database log

        httpLogEntry = getHttpLog(current_time)    
        print(str(httpLogEntry))

        dbLogEntries = getDbLogEntries(time_str)



















