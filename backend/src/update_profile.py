import os
from pprint import pprint
import bson
from dotenv import load_dotenv
import pymongo
from bson.objectid import ObjectId


# when updating profile, the front end should send a payload containing all the fields that have been filled
# it must have an _id!
def edit_profile(payload, db_uri):
    client = pymongo.MongoClient(db_uri)
    db = client["Main"]
    coll = db["user"]
    if "_id" in payload:
        user_id = payload["_id"]    
        if type(user_id) == str:
            user_id = ObjectId(payload["_id"])
        elif type(user_id) == bson.objectid.ObjectId: 
            user_id = payload["_id"]
        query = {"_id": user_id}
        chck_existance = check_record_exist(query, db_uri)
        if chck_existance == "exists":
            test_query = coll.find(query)
            if "favourites" in payload:
                favourites = payload["favourites"]
                newvalues = {"$set":{ "favourites": favourites}}
                coll.update_one(query, newvalues)
                check_status(test_query, "favourites", favourites)
            if "investmenthorizon" in payload: 
                horizon = payload["investmenthorizon"]
                newvalues = {"$set":{ "investmenthorizon": horizon}}
                coll.update_one(query, newvalues)
                check_status(test_query, "investmenthorizon", horizon)
            if  "investmentstyle" in payload:
                style = payload["investmentstyle"]
                newvalues = {"$set":{ "investmentstyle": style}}
                coll.update_one(query, newvalues)
                check_status(test_query, "investmentstyle", style)
            else: 
                print("ERR!! NO _id in the payload!")
        else:
            print("RECORD DOES NOT EXIST!")


def check_status(db_query, key, value ):
    for records in db_query:
        if key  in records:
            field = records[key]
            if field == value:
                print("RECORD UPDATED!")
            else: 
                print("RECORD NOT UPDATED")

def check_record_exist(query, db_uri):
    client = pymongo.MongoClient(db_uri)
    db = client["Main"]
    coll = db["user"]
    fetched_records = coll.find(query)
    for record in fetched_records:
        dd_record = record
        if dd_record != None: 
            return "exists"
        else:
            return "does not exist"