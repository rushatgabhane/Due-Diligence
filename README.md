# DD - Due Diligence

## Concept 

## UI/UX 

- Sign up
- Log in 
- Give details
- Connect 
- Chat
- Snap Stock! 


## Backend 

### server.py

### Db

We used MongoDB Free Tier (520GB), and for this mobile application we made use of two collections: 

- User: identity records of the users who are using Due Diligence
- Histories: containing search history of the user 

Note to create the collection simply use the following command:

```
db.createCollection("<name collection>")

```

![Creating `histories` collections](./img/histories_collection.png)

A user will have a record of the type:


```
{
    "_id": ObjectId("1279817381941duaiuj19837"),
    "username": "Princeton Hacker",
    "email": "user@hackprinceton.com",
    "password":"£$£&£%&$&%$*$*£%"%",
    "investmentstyle": "growth", 
    "investmenthorizon": "2",
    "favourites":[
        "APPL",
        "TSL",
        "PLTR"
    ]
}
```

Whenever the user generates a serch, the history will be stored in `db.Histories` with a userid corresponding to the "_id" of the user in the `User` collection. The `timestamp` will be used to fetch the history search of the user with respect to the most recent. The record will be of the type:

```

{
    "_id": ObjectId("2193619745bdga08217"),
    "userid":  "_id": ObjectId("1279817381941duaiuj19837"),
    "timestamp": ISODate("2019-01-31T10:00:00.000Z"),
    "stockname": "APPL"
}

```
The search is limited to 3-5 most recent searches, i.e. described by the query: 

```
db.Histories.aggregate([{$sort: {"timestamp":-1}}, {$limit:3}])

```

where `-1` is used to describe sort descending, from most recent and limit correspond to the number of record returned.