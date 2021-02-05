import consul

from flask import Flask
from flask_cors import CORS

from pymongo import MongoClient
from bson.json_util import loads, dumps

import socket
import threading 
import time

app = Flask(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})







#starts the connection with the database and 
#publishes its IP address to the consul service
def init():
    time.sleep(30)
    IPAddr = socket.gethostbyname(hostname)  
    mongoClient = MongoClient('10.1.0.101', 27017)
    db = mongoClient.sanare

    c = consul.Consul()
    c.kv.put('sanare-manager', IPAddr+':3000')


t1 = threading.Thread(target=init, args=()) 
t1.start()


@app.route('/logs/http/entries/', methods=['GET'], defaults={'n':10})
@app.route('/logs/http/entries/<n>', methods=['GET'])
def getHttpLogEntries(n):
    n = int(n)
    entries = [n]
    return dumps(db.httplogentries.find(limit=n))


@app.route('/')
def hello_world():

    routes = [
        "/logs/http/entries/",
        "/logs/http/entries/[n]"
    ]

    return  "<ul><li>" + "</li><li>".join(routes) + "</li></ul>" 


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=3000)
