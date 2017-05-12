'''
Created on Apr 27, 2017

@author: goebel
'''

import time
import re

try:
	import pymongo
	from pymongo import MongoClient
	mongoClient = MongoClient('mongodb://csse:Poos4iko@137.112.104.109', 40000)
	db = mongoClient['rose-profs']
	students = db.students
	professors = db.professors
	logs = db.logs
except:
	print("Could not connect to Mongo")
	
	
try:
	import redis
	POOL = redis.ConnectionPool(host='137.112.104.109', port=6379, db=0)
	conn = redis.Redis(connection_pool=POOL)
except:
	print("Could not connect to Redis")
	redisDead = True


def add_prof(record):
	if not conn.zscore('professors', record['Name']) is None:
		return
	conn.zadd('professors', record['Name'], 0)


def del_prof(record):
	if conn.zscore('professors', record['Name']) is None:
		return
	conn.zrem('professors', record['Name'])


def add_class_to_prof(record):
	if conn.zscore('professors', record['Professor']) is None:
		return
	if not conn.zscore(record['Number'], record['Professor']) is None:
		return
	
	conn.zadd('classes', record['Number'], 0)
	conn.zadd(record['Number'], record['Professor'], 0)


def del_class_from_prof(record):
	if conn.zscore('professors', record['Professor']) is None:
		return
	if conn.zscore(record['Number'], record['Professor']) is None:
		return
	conn.zrem(record['Number'], record['Professor'])
	if conn.zcount(record['Number'], 0, -1) == 0:
		conn.zrem('classes', record['Number'])

	
print("Data is being brought up to date!")
while True:
	time.sleep(1)
	try:
		logs.remove({"mongo": -1, "redis": -1, "orient": -1})
	except:
		print("Mongo Down")
		continue
		
	try:
		redisLogsTodo = logs.find({"redis": 0}).sort("$natural", 1)
		for record in redisLogsTodo:
			if record["type"] == "add_prof":
				try:
					add_prof(record)
				except:
					print("Redis down 1")
					continue
			elif record["type"] == "del_prof":
				try:
					del_prof(record)
				except:
					print("Redis down 2")
					continue
			elif record["type"] == "add_class_to_prof":
				try:
					add_class_to_prof(record)
				except:
					print("Redis down 3")
					continue
			elif record["type"] == "del_class_from_prof":
				try:
					del_class_from_prof(record)
				except:
					print("Redis down 4")
					continue
			logs.update_one({'_id': record["_id"]}, {'$set': {'redis': -1}})
			print(record["type"] + " was executed!")

	except Exception as e:
		#print str(e)
		print("Mongo Down")
		continue