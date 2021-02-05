import flask
from flask import jsonify
from pymongo import MongoClient
from bson.json_util import loads, dumps
import reverse_proxy
import threading 


app = flask.Flask(__name__)


hostname = 'localhost:8000'
db = None






@app.route('/logs/http/entries',methods=['GET'])
def getHttpLogEntries():
    if db is None:
        client = MongoClient('mongodb://%s:%s@10.1.0.101' % ('root', 'sanare'))
        db = client.sanare
    entries = [10]
    i = 0
    return dumps(db.httplogentries.find(limit=10))





@app.route('/start_reverse_proxy',methods=['GET'], defaults={'port': 8080})
@app.route('/start_reverse_proxy/<port>',methods=['GET'])
def startReverseProxy(port):
    if db is None:
        client = MongoClient('mongodb://%s:%s@10.1.0.101' % ('root', 'sanare'))
        db = client.sanare
    t1 = threading.Thread(target=reverse_proxy.start_reverse_proxy, args=(8080,)) 
    t1.start()
    return "reverse proxy started on port " + str(port)
    



if __name__ == "__main__":
    t1 = threading.Thread(target=reverse_proxy.start_reverse_proxy, args=(8080,)) 
    t1.start()
    app.run(host="0.0.0.0", port=3002)




