import json
import connection_suggestions
import sql_database
from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/home")
def hello_world():
    return 


@app.route("/find_mutuals")
def find_mutuals():
    # read data from DB
    messages = sql_database.get_messages()
    # construct connections graph
    connection_graph = sql_data_transforms.create_connections_graph(messages)
    # run mutual finder algorithm
    uids = []
    suggestions = dict()
    for uid in uids:
        suggs = connection_suggestions.get_mutuals(uid, connection_graph)
        suggestions[uid] = suggs
    # update db
    
    # return
    return jsonify({
        "success": True
    })


@app.route("/find_common_interests")
def find_common_interests():
    # read data from DB
    messages = sql_database.get_messages()
    # get keywords
    
    # run mutual finder algorithm
    
    # update db
    
    # return
    return jsonify({
        "success": True
    })
