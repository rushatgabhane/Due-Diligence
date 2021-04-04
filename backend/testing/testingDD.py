import os
from pprint import pprint
import bson
from dotenv import load_dotenv
import pymongo
from bson.objectid import ObjectId
mongodb_pass = '4v38Z9oFAxnKm6SG'
# db_name = "Main"
# DB_URI = "mongodb+srv://s3kim2018:{}@cluster0.xfm8y.mongodb.net/{}?retryWrites=true&w=majority".format(mongodb_pass, db_name)
# load_dotenv(verbose=True)
test_id = ObjectId("6068fada8ac8540613ea288c")
friend_id = ObjectId("60690138e111b60d31e227a4")
print(type(friend_id))
email = "bob@gmail.com"
db_uri = "mongodb+srv://princetonHacker:4v38Z9oFAxnKm6SG@princetonunihack.rvwct.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"

def find_userid(email):
    print("FOUND")
    client = pymongo.MongoClient(db_uri)
    db = client["Main"]
    coll = db["user"]
    print("FOUND")
    pipeline = [
    {
            "$match": {
                "email": email,
                "username": "skyler"
            },
        },
    ]

    print("FOUND 3")
    
    fetched_record = coll.aggregate(pipeline)
    print("FOUND 3")
    for search in fetched_record:
        print("FOUND 3")
        print(search)
        dd_id = search["_id"]
        print(dd_id)
    return dd_id

def fetch_search_history():
    print("TEST 1")
    # connect to mongo cluster using pymongo
    search_history_arr = []
    client = pymongo.MongoClient("mongodb+srv://princetonHacker:4v38Z9oFAxnKm6SG@princetonunihack.rvwct.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
    db = client["Main"]
    coll = db["histories"]
    print("TEST 2")
    dd_id = find_userid(email)
    print("TEST 3")
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
    ## here we need to return rather than print
    for search in fetched_searches:
        search_history_arr.append(search)
    return search_history_arr

def find_record(record_id, db_uri):
    client = pymongo.MongoClient(db_uri)
    db = client["Main"]
    coll = db["user"]
    pipeline = [
    {
            "$match": {
                "_id": record_id
            },
        },
    ]
    fetched_records = coll.aggregate(pipeline)
    for record in fetched_records:
        dd_record = record
    return dd_record


def fetch_friends_list(user_id, db_uri):
    friendsIDs = []
    friends_list =[]
    client = pymongo.MongoClient(db_uri)
    db = client["Main"]
    coll = db["user"]
    pipeline = [
    {
            "$match": {
                "_id": user_id
            },
        },
    ]

    fetched_records = coll.aggregate(pipeline)
    for record in fetched_records:
                #check if the field friends exist first 
        if "friends" in record:
            friendsIDs = record["friends"]

    for dd_id in friendsIDs:
        friend_record = find_record(dd_id, db_uri)
        friends_list.append(friend_record)

    return friends_list
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

# When the user with user_id clicks on `add` or `connect` the list of friends is updated 
# and a new friend with id = friend_id is added to the list

def add_friend(user_id, friend_id, db_uri):
    client = pymongo.MongoClient(db_uri)
    db = client["Main"]
    coll = db["user"]
    #check type for user_id
    if type(user_id) == str:
        user_id = ObjectId(user_id)
    elif type(user_id) == bson.objectid.ObjectId: 
        user_id = user_id

    #check type for friend_id
    if type(friend_id) == str:
        friend_id = ObjectId(user_id)
    elif type(friend_id) == bson.objectid.ObjectId: 
        friend_id = user_id
    query = {"_id": user_id}
    # I use the method $addToSet rather than $push, if the id already exists it will not be added
    # to the set.
    newvalues = {"$addToSet":{ "friends": friend_id}}
    # update user record with _id =user_id with a new friend by appending
    # an dd_id = friend_id to the friends array
    coll.update_one(query, newvalues)
    #confirmation 
    for records in coll.find(query):
            if "friends" in records:
                friends = records["friends"]
                if contains(friends, friend_id) == 0:
                    print("FRIEND ADDED!")
                else: 
                    print("FRIEND ALREADY ADDED")



def contains(arr, element):
    if element in arr: 
        return 1 #true
    else:
        return 0 #false


if __name__ == "__main__":
    searches =  fetch_search_history()
    print(searches)
    print("BEFORE ADDING FRIENDS!")
    friends = fetch_friends_list(test_id, db_uri)
    add_friend(test_id, friend_id, db_uri)
    print("\n")
    print("AFTER ADDING FRIENDS!")
    friends = fetch_friends_list(test_id, db_uri)
    print("UPDATING PROFILE!")
    test_payload = {
     "_id": "6068fada8ac8540613ea288c",
     "investmentstyle": "long term"
    }
    print("\n")
    edit_profile(test_payload,db_uri)
    print("TEST DONE!!")



