import json
import io
import hashlib 
from flask import Flask, request, render_template, url_for, make_response, jsonify, send_file
from flask_mongoengine import MongoEngine
from constants import *
import requests

app = Flask(__name__)

@app.route("/")
def mainpage():
    response = requests.get('https://sandbox.tradier.com/v1/markets/search',
        params={'q': 'alphabet', 'indexes': 'false'},
        headers={'Authorization': 'Bearer EQGhrbEgpNGAVsdNEDJ4RT0TJoBY', 'Accept': 'application/json'}
    )
    print("hello")
    #json_response = response.json()
    print(response.status_code)
    #print(json_response)
    return "bob"

if __name__ == '__main__':
    app.run(debug = True)