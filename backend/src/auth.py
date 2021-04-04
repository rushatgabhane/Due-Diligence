import os
from pprint import pprint
import bson
from dotenv import load_dotenv
import pymongo
from bson.objectid import ObjectId

# at log in 
def check_user_credentials(payload, db_uri):
    client = pymongo.MongoClient(db_uri)
    db = client["Main"]
    coll = db["user"]
    # print("TEST CHECK")
    if "_id" in payload and "username" in payload and "password" in payload:
        print("TEST CHECK")
        user_id = payload["_id"]    
        if type(user_id) == str:
            user_id = ObjectId(payload["_id"])
        elif type(user_id) == bson.objectid.ObjectId: 
            user_id = payload["_id"]
        username = payload["username"]
        password = payload["password"]
        query = {"_id": user_id, "password": password, "username": username}
        fetched_records = coll.find(query)
        # print("RECORD FETCHED")
        for record in fetched_records:
            dd_record = record
            if dd_record != None: 
                # print(dd_record["_id"])
                return dd_record["_id"]
            else:
                # print('STATUS 400, RECORD NOT FOUND')
                return  'STATUS 400, RECORD NOT FOUND'
    else: 
        # print('STATUS 400, PROVIDE BOTH USERNAME, PASSWORD')
        return 'STATUS 400, PROVIDE BOTH USERNAME, PASSWORD'



# insert user at sign up
# username and email must be unique
def create_user(payload, db_uri):
    client = pymongo.MongoClient(db_uri)
    non_unique_rec_arr = []
    db = client["Main"]
    coll = db["user"]
    if "email" in payload and "username" in payload and "password" in payload:
        # check if email is unique 
        email = payload["email"]
        pipeline_1 =  [{
                "$match": {
                    "email":  email
                },
        }]
        fetched_records = coll.aggregate(pipeline_1)
        for search in fetched_records:
            non_unique_rec_arr.append(search)
        if non_unique_rec_arr != []: 
                return "Email or Username already used. Sign Up with a different email or Log In"
        else: 
            print("INSERTING NEW USER")
            query = {"email": payload["email"], "username": payload["username"], "password": payload["password"]}
            insert_record = coll.insert(query)
            print("INSERTION SUCCESSFUL")
            print(insert_record)
            return insert_record

    
        
            
