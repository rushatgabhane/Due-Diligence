import os
from pprint import pprint
import bson
from dotenv import load_dotenv
import pymongo
from bson.objectid import ObjectId
import datetime

def find_userid(email, db_uri):
    client = pymongo.MongoClient(db_uri)
    db = client["Main"]
    coll = db["user"]

    pipeline = [
    {
            "$match": {
                "email": email
            },
        },
    ]
    
    fetched_records = coll.aggregate(pipeline)
    for record in fetched_records:
        dd_id = record["_id"]
        if dd_id != None:
            return dd_id
        else: 
            return "400, USER NOT FOUND"



def recent_search_history(db_uri, email):
    search_history_arr =[]
    dd_id = find_userid(email, db_uri) #to be added 
    # connect to mongo cluster using pymongo
    client = pymongo.MongoClient(db_uri)
    db = client["Main"]
    coll = db["histories"]
    pipeline = [
    {
            "$match": {
                "dd_id": dd_id
            },
        },
    {
        "$sort": {
            "timestamp":-1
            }
    }, 
    {
        "$limit":3
        }, 
    ]
    fetched_searches = coll.aggregate(pipeline)
    for search in fetched_searches:
        search_history_arr.append(search)
    return search_history_arr



def create_history(payload, db_uri):
        ## passing the stock payload
        # if type(payload) == list():
        #     # do
        client = pymongo.MongoClient(db_uri)
        db = client["Main"]
        coll = db["histories"]
        if type(payload) == dict:
            payload["timestamp"] = datetime.datetime.now()
            if "_id" in payload: 
                dd_id = payload["_id"]
                del payload["_id"]
            elif "id" in payload: 
                dd_id = payload["id"]
                del payload["id"]
            if type(dd_id) == str:
                dd_id = ObjectId(dd_id)
            elif type(dd_id) == bson.objectid.ObjectId: 
                dd_id = dd_id
            payload["dd_id"] = dd_id
            insert_search_id = coll.insert(payload)
            if insert_search_id != None:
                print("SEARCH SUCCESSFULLY SAVED")
                print(insert_search_id)
                return insert_search_id
            else:
                # print('STATUS 400, RECORD NOT FOUND')
                return  'HISTORY RECORD NOT SAVED'