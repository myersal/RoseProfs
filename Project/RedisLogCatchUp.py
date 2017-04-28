'''
Created on Apr 27, 2017

@author: goebel
'''

import time
import re

try:
	import pymongo
	from pymongo import MongoClient
	mongoClient = MongoClient('mongodb://csse:Poos4iko@137.112.104.109')
	db = mongoClient['rose-profs']
	students = db.students
	professors = db.professors
	logs = db.logs
except:
	print("Could not connect to Mongo")
	
	
try:
	import redis
	POOL = redis.ConnectionPool(host='137.112.104.109', port=6379, db=0)
	conn = redis.Redis(connection_pool = POOL)
except:
	print("Could not connect to Redis")
	redisDead = True
	
def redisRateProf(record):
	return
	
print("Data is being brought up to date!")
while True:
	time.sleep(5)
	try:
		logs.remove({"mongo": -1, "redis": -1, "orient": -1})
	except:
		print("Mongo Down")
		continue
		
	try:
		redisLogsTodo = logs.find({"redis": 0}).sort("$natural", 1)
		for record in redisLogsTodo:
			if (record["type"] == "rateProf"):
				try:
					redisRateProf(record)
				except:
					print("Redis down")
					continue
			
	except Exception as e:
		#print str(e)
		print("Mongo Down")
		continue