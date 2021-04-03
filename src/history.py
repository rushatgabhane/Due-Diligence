import os
from pprint import pprint
import bson
from dotenv import load_dotenv
import pymongo




def fetch_search_history(db_uri, email):
    search_history_arr =[]
    dd_id = find_userid(email, db_uri) #to be added 
    # connect to mongo cluster using pymongo
    client = pymongo.MongoClient(db_uri)
    db = client["Main"]
    coll = db["Histories"]

    pipeline = [
    {
            "$match": dd_id,
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

