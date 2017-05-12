'''
Created on Apr 26, 2017

@author: goebel
'''

redisDead = False
orientDead = False
databaseOpen = True

#MongoDB
try:
	import pymongo
	from pymongo import MongoClient
	mongoClient = MongoClient('mongodb://137.112.104.109', 40000)
	db = mongoClient['roseprofs']
	students = db.students
	professors = db.professors
	logs = db.logs
except:
	print("Sorry, but Rose Profs is currently down.  Please try again later")
	databaseOpen = False
	exit()


try:
	import redis
	POOL = redis.ConnectionPool(host='137.112.104.109', port=6379, db=0, socket_timeout=5)
	conn = redis.Redis(connection_pool = POOL)
except:
	print("Some functionality may be slower and/or limited due to problems outside of your control")
	redisDead = True

try:
	import pyorient
	import pyorient.ogm
	client = pyorient.OrientDB("137.112.104.108", 2424);
	session_id = client.connect( "root", "wai3feex" );
	client.db_open( "roseprofs", "admin", "admin" );
except:
	print("Some functionality may be slower and/or limited due to problems outside of your control")
	orientDead = True


print("CONNECTED TO ROSE PROFS!!!!")