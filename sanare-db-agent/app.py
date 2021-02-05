from flask import Flask
import mysql.connector
from flask import jsonify
from datetime import datetime

import json

mydb = None
mycursor = None

def get_connection():
    mydb = mysql.connector.connect(
        host="10.1.0.99",
        user="wordpress",
        passwd="wordpress"
    )

    mycursor = mydb.cursor()

    mycursor.execute("SET GLOBAL log_output = 'TABLE';")
    mycursor.execute("SET GLOBAL general_log = 'ON';")


app = Flask(__name__)

def parse_query_david(query_bytes):
    if mydb is None:
        get_connection()
    query = query_bytes#.decode("utf-8")
    parsed = {}
    query = query.replace("\n", " ")
    query = ' '.join(query.split())
    
    if(query.startswith("SELECT")):
        parsed["type"] = "SELECT"
        try:
            parsed["table"] = query.split(" FROM ")[1].split(" ")[0]
            parsed["affected_columns"] = -1 if query.startswith("SELECT *") else len(query.split(" FROM ")[0].split(","))
        except:
            parsed["table"] = ""
            parsed["affected_columns"] = 0
        try:
            parsed["predicates"] = len(query.split(" WHERE ")[1].replace("OR", "AND").split("AND"))
        except:
            parsed["predicates"] = 0

        if(query.find("ORDER BY") > -1):
            parsed["order_by"] = True
            if(query.split("ORDER BY")[1].find("DESC")>-1):
                parsed["order_by_param"] = "DESC"
            else:
                parsed["order_by_param"] = "ASC"
        else:
            parsed["order_by"] = False


        if (query.find(" LIMIT ") > -1):
            parsed["limit"] = True
            if(query.split(" LIMIT ")[1].find(",")>-1):
                parsed["limit_n"] = int(query.split(" LIMIT ")[1].split(",")[1])
                parsed["limit_offset"] = int(query.split(" LIMIT ")[1].split(",")[0])
            else:
                parsed["limit_n"] = int(query.split(" LIMIT ")[1])
                parsed["limit_offset"] = 0
        else:
            parsed["limit"] = False
            parsed["limit_n"] = 0
            parsed["limit_offset"] = 0



        

    else:
        print("Não eh um select ")

    return parsed





@app.route('/logs/db/entries', methods=['GET'], defaults={'n': 10})
@app.route('/logs/db/entries/<n>', methods=['GET'])
def get_n_db_entries(n):
    if mydb is None:
        get_connection()
    result = list()

    mycursor.execute("SELECT * FROM mysql.general_log order by event_time desc limit " + str(n) + ";")

    log_entries = mycursor.fetchall()

    print(len(result))

    for log_entry in log_entries:
        row = {
            "event_time": log_entry[0],
            "user_host": log_entry[1],
            "thread_id": log_entry[2],
            "server_id": log_entry[3],
            "command_type": log_entry[4],
            "argument": log_entry[5]
        }
        result.append(row)

        print(log_entry[5])
        parse_query_david(log_entry[5])

        # print(log_entry)

    return jsonify(str(result))



#Get db entries between 'start' and 'end'
@app.route('/logs/db/entries/<int:start>/<int:end>', methods=['GET'])
def get_db_entries_time_frame(start, end):
    if mydb is None:
        get_connection()
    result = list()


    print("Start: " + str(start))
    print("End: " + str(end))

    start_dt = datetime.fromtimestamp(start)
    end_dt = datetime.fromtimestamp(end)

    cursor = mydb.cursor(prepared=True)


    query = "SELECT * FROM mysql.general_log where event_time >= %s and event_time <= %s  order by event_time desc"
    cursor.execute(query, (start_dt, end_dt) )

    log_entries = cursor.fetchall()

    print(len(result))

    for log_entry in log_entries:
        row = {
            "event_time": log_entry[0],
            "user_host": log_entry[1],
            "thread_id": log_entry[2],
            "server_id": log_entry[3],
            "command_type": log_entry[4],
            "argument": log_entry[5]
        }
        result.append(parse_query_david(log_entry[5]) )

        
        print(parse_query_david(log_entry[5]))
        #parse_query_david(log_entry[5])

        # print(log_entry)

    return jsonify(str(result))





if __name__ == '__main__':
    app.run(host="0.0.0.0", port=3001)
