'''
Created on Apr 26, 2017

@author: goebel
'''

import pymongo
from pymongo import MongoClient
import redis


databaseOpen = True

import pyorient
import pyorient.ogm

client = pyorient.OrientDB("137.112.104.108", 2424);
session_id = client.connect( "root", "wai3feex" );
client.db_open( "roseprofs", "admin", "admin" );

POOL = redis.ConnectionPool(host='137.112.104.109', port=6379, db=0)
conn = redis.Redis(connection_pool = POOL)
mongoClient = MongoClient('mongodb://csse:Poos4iko@137.112.104.109')
db = mongoClient['rose-profs']
students = db.students
professors = db.professors
print("GO")