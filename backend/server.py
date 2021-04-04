import json
import io
from hashlib import * 
from flask import Flask, request, render_template, url_for, make_response, jsonify, send_file, session
from flask_mongoengine import MongoEngine
import mongoengine as db 
from google.cloud import vision
import NaiveBayes as nb
from constants import *
import numpy as np
import requests
import random
app = Flask(__name__)
mongodb_pass = 'MyBiLU2HPTEYnoN5'
db_name = "Main"
DB_URI = "mongodb+srv://Brian:{}@princetonunihack.rvwct.mongodb.net/{}?retryWrites=true&w=majority".format(mongodb_pass, db_name)
app.config["MONGODB_HOST"] = DB_URI
db = MongoEngine()
db.init_app(app)

app = Flask(__name__)

class User(db.Document):
    username = db.StringField()
    password = db.StringField()
    email = db.EmailField() #adding email address field to the document
    investmentstyle = db.StringField() #Choice of Value, Growth, Speculative
    investmenthorizon = db.StringField() #Choice of Day, Monthly, Annual, Long-Term
    favourites = db.DictField()
    friends = db.DictField()
    def to_json(self): 
        return {
            "username": self.username,
            "email":self.email, #adding email address field to JSON
            "investmentstyle": self.investmentstyle, 
            "investmenthorizon": self.investmenthorizon,
            "favourites": self.favourites,
            "friends": self.friends
        }

class Chat(db.Document):
    chatid = db.StringField()
    content = db.DictField() 
    stock = db.StringField()
    participant1 = db.StringField()
    participant2 = db.StringField()
    def to_json(self): 
        return { 
            "chatid": self.chatid,
            "content": self.content,
            "stock": self.stock,
            "participant1": self.participant1,
            "participant2": self.participant2
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

@app.route("/register", methods = ['POST'])
def register(): 
    user = request.form["username"]
    passw = request.form['password']
    mail = request.form["email"]
    style = request.form["style"]
    horizon = request.form["horizon"]
    favorites = request.form["favourites"]
    favlst = favorites.split(",")
    json = {'0':favlst[0], '1':favlst[1], '2':favlst[2]}
    if User.objects(username = user).first(): 
        return make_response("That username already exists", 400)
    else:
        newuser = User(username = user, password = sha256(passw.encode('utf-8')).hexdigest(), email = mail, investmentstyle = style, investmenthorizon = horizon, favourites = json, friends = {})
        newuser.save() 
    return make_response("success", 201)

@app.route("/login", methods = ['POST'])
def login(): 
    if "user" in session: 
        return make_response("User already logged in", 400)
    else: 
        user = request.form["username"]
        passw = sha256(request.form["password"].encode('utf-8')).hexdigest()
        if User.objects(username = user, password = passw):
            Userobj = User.objects(username = user, password = passw).first()
            print(Userobj.to_json())
            session["user"] = Userobj.to_json()
            return make_response("Login Success", 200)
        else:
            return make_response("Wrong username or password", 400)


@app.route("/logout", methods = ['POST'])
def logout(): 
    if "user" in session:
        session.pop("user", None)
        return make_response("Success", 200)
    else:
        return make_response("User not logged in", 400)

autokeyword = ['Car', 'Bus', 'Truck', 'Automobile', 'Wheel', 'Tire']
electronickeyword = ['Phone', 'Refrigerator', 'Mobile phone', 'Television', 'Microwave', 'Laptop']
jewelerykeyword = ['Earrings', 'Watch', 'Ring', "Necklace"]
foodkeyword = ['Packaged goods', 'Food']
depstorekeyword = ['Building']
clothingkeyword = ['Shirts', 'Pants', 'Clothes', "Socks", "Jeans", "Shoes"]
educationkeyword = ['Book', 'Textbook', 'Ruler', 'Pencil', 'Pen', 'Eraser']
planekeyword = ['Airplane', 'Helicopter', 'Rocket']
@app.route("/analyzeimage", methods = ['POST'])
def analyzeimage():  ##RECOMMENDATION SYSTEM, SEND IMAGE AS BOD
    ret = []
    client = vision.ImageAnnotatorClient()
    file = request.get_data() 
    filemark = file
    image = vision.Image(content=filemark)
    objects = client.object_localization(image=image).localized_object_annotations
    logos = client.logo_detection(image=image).logo_annotations

    
    for logo in logos:
        print(logo.description)
    if len(objects) == 0 and len(logos) == 0:
        return make_response("No object found", 400)
    else:
        industry = ""
        special = ""
        for object in objects: 
            print(object.name)
            if object.name in autokeyword: 
                industry = "sector?collectionName=Manufacturing"
                special = "cars"
            elif object.name in electronickeyword:
                #industry = "Electronic Technology"
                industry = "sector?collectionName=Technology"
            elif object.name in jewelerykeyword:
                industry = "tag?collectionName=Department%20Stores"
            elif object.name in foodkeyword: 
                industry = "collectionName=Food%20Retail"
            elif object.name in depstorekeyword:
                industry = "tag?collectionName=Department%20Stores"
            elif object.name in clothingkeyword:
                industry = "Clothing Accessories Stores"
            elif object.name in educationkeyword:
                industry = "tag?collectionName=Educational%20Services"
            elif object.name in planekeyword: 
                industry = "tag?collectionName=Airlines"
        for logo in logos: 
            response = requests.get('https://cloud.iexapis.com/stable/search/' + logo.description,
            params={'token': 'sk_ac997761af19455d8588775994c0b03f'},
            )
            json_response = response.json()
            for node in json_response: 
                if node.get('exchange') == 'NAS':
                    ret.append(node)
        response = requests.get('https://cloud.iexapis.com/stable/stock/market/collection/' + industry + "&token=sk_ac997761af19455d8588775994c0b03f")
        json_response = response.json()
        res = []
        print(industry)
        if industry is not "":
            for node in json_response:
                if special == "cars":
                    if node.get('symbol') == 'TSLA' or node.get('symbol') == 'GM' or node.get('symbol') == 'F':
                        res.append(node)
                elif (node.get('primaryExchange') == 'NEW YORK STOCK EXCHANGE, INC.' or node.get('primaryExchange') == 'US OTC') and node.get('marketCap') != None:
                    res.append(node)
            res.sort(key = lambda x: int(x.get('marketCap')))
            res.reverse()
        if len(res) > 3:
            ret += res[0:3]
        else: 
            ret += res 
        response = app.response_class(response=json.dumps(ret), status=200, mimetype='application/json')
        return response


@app.route("/createchat", methods = ['POST']) #RETURNS CHATID AS RESPONSE
def createchat(): 
    user = request.form["username"]
    ticker = request.form["stockticker"]
    thisuser = User.objects(username = user).first()
    seconduser = ""
    for user in User.objects(): 
        if abs(int(user.investmenthorizon) - int(thisuser.investmenthorizon)) < 3: 
            seconduser = user.username
            break 
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k']
    id = ''.join(random.choice(letters) for i in range(7))
    newchat = Chat(chatid = id, content = {}, stock = ticker, participant1 = thisuser.username, participant2 = seconduser)
    newchat.save()
    return make_response(id, 200)


@app.route("/appendchat", methods = ["POST"]) 
def appendchat(): 
    id = request.form["chatid"]
    user = request.form["user"]
    message = request.form["message"]
    thechat = Chat.objects(chatid = id)
    ticker = thechat.stock 
    if message == "getprice":
        response = requests.get('https://cloud.iexapis.com/stable/stock/'+ ticker +'/price?token=sk_ac997761af19455d8588775994c0b03f')
        json_response = response.json()
        print(json_response[0])
    if message == "earnings": 
        print("HI")
    return 




if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(debug = True)


