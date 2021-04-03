import json
import io
import hashlib 
from flask import Flask, request, render_template, url_for, make_response, jsonify, send_file
from flask_mongoengine import MongoEngine
from constants import *
import requests
app = Flask(__name__)
mongodb_pass = '4v38Z9oFAxnKm6SG'
db_name = "Main"
DB_URI = "mongodb+srv://s3kim2018:{}@cluster0.xfm8y.mongodb.net/{}?retryWrites=true&w=majority".format(mongodb_pass, db_name)
app.config["MONGODB_HOST"] = DB_URI
db = MongoEngine()
db.init_app(app)

app = Flask(__name__)

class User(db.Document):
    username = db.StringField()
    password = db.StringField()
    investmentstyle = db.StringField() #Choice of Value, Growth, Speculative
    investmenthorizon = db.StringField() #Choice of Day, Monthly, Annual, Long-Term

    def to_json(self): 
        return {
            "username": self.username,
            "investmentstyle": self.investmentstyle, 
            "investmenthorizon": self.investmenthorizon,

        }


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


#Example http://127.0.0.1:5000/register?username=bob&style=long&horizon=annual       

@app.route("/register", methods = ['POST'] )
def register(): 
    username = request.args.get("username")
    #password = request.form['password']
    style = request.args.get("style")
    horizon = request.args.get("horizon")
    print(username)
    return make_response("success", 201)


if __name__ == '__main__':
    app.run(debug = True)