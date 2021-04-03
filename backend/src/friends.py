import os
from pprint import pprint
import bson
from dotenv import load_dotenv

import pymongo

def find_record(ID, db_uri):
    client = pymongo.MongoClient(db_uri)
    db = client["Main"]
    coll = db["User"]
    pipeline = [
    {
            "$match": {
                "_id": ID
            },
        },
    ]
    fetched_records = coll.aggregate(pipeline)
    for record in fetched_records:
        dd_record = record
    return dd_record


def fetch_friends(user_id, db_uri):
    friendsIDs = []
    friends_list =[]
    client = pymongo.MongoClient(db_uri)
    db = client["Main"]
    coll = db["User"]
    pipeline = [
    {
            "$match": {
                "_id": user_id
            },
        },
    ]

    fetched_records = coll.aggregate(pipeline)
    for record in fetched_records:
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

def add_dd_friend(user_id, friend_id, db_uri):
    client = pymongo.MongoClient(db_uri)
    db = client["Main"]
    coll = db["User"]
    query = {"_id": user_id}
    # I use the method $addToSet rather than $push, if the id already exist it will not be added
    newvalues = {"$addToSet":{ "friends": friend_id}}
    # update user record with _id =user_id with a new friend by appending
    # an dd_id = friend_id to the friends array
    coll.update_one(query, newvalues)
    #confirmation 
    for records in coll.find(query):
        for record in records:
            friends = record["friends"]
            if contains(friends, friend_id) == 0:
                print("FRIEND ADDED!")
            else: 
             print("FRIEND ALREADY ADDED")

