import os
from pprint import pprint
import bson
from dotenv import load_dotenv
import pymongo
from bson.objectid import ObjectId

def find_record(record_id, db_uri):
    client = pymongo.MongoClient(db_uri)
    db = client["Main"]
    coll = db["user"]
    if type(record_id) == str:
        record_id = ObjectId(record_id)
    elif type(record_id) == bson.objectid.ObjectId: 
        record_id = record_id
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
    if type(user_id) == str:
        user_id = ObjectId(user_id)
    elif type(user_id) == bson.objectid.ObjectId: 
        user_id = user_id
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

def contains(arr, element):
    if element in arr: 
        return 1 #true
    else:
        return 0 #false


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
                    return friend_id
                else: 
                    return "FRIEND ALREADY EXIST IN THE LIST"

