import json
from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/home")
def hello_world():
  return 


@app.route("/find_mutuals")
def find_mutuals():
  # read data from DB

  # construct connections graph

  # run mutual finder algorithm for each person

  # update db

  # return
  return jsonify({
    "success": True
  })


@app.route("/find_common_interests")
def find_common_interests():
  # read data from DB

  # construct connections graph

  # run mutual finder algorithm

  # update db

  # return
  return jsonify({
    "success": True
  })
