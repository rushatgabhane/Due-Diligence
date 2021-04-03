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