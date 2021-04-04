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



def add_friend(user_id, friend_id, db_uri):
    client = pymongo.MongoClient(db_uri)
    db = client["Main"]
    coll = db["user"]
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

import pygame
import pygame.camera


def image_capture2():

    pygame.camera.init()
    cam = pygame.camera.Camera(0,(640,480))
    cam.start()
    img = cam.get_image()
    pygame.image.save(img,"filename.jpg")


if __name__ == "__main__":
    searches =  fetch_search_history()
    print(searches)
    print("BEFORE ADDING FRIENDS!")
    friends = fetch_friends_list(test_id, db_uri)
    add_friend(test_id, friend_id, db_uri)
    print("AFTER ADDING FRIENDS!")
    friends = fetch_friends_list(test_id, db_uri)
    print(friends)
    image_capture2()
