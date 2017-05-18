'''
Created on Apr 27, 2017

@author: goebel
'''

import time
import re

try:
	import pymongo
	from pymongo import MongoClient
	#mongoClient = MongoClient('mongodb://csse:Poos4iko@137.112.104.109', 40000)
	mongoClient = MongoClient('mongodb://137.112.104.109', 40000)
	db = mongoClient['roseprofs']
	students = db.students
	professors = db.professors
	print("hello?")
	logs = db.logs
except:
	print("Could not connect to Mongo")
	
	
try:
	import redis
	POOL = redis.ConnectionPool(host='137.112.104.109', port=6379, db=0, socket_timeout=5)
	conn = redis.Redis(connection_pool=POOL)
except:
	print("Could not connect to Redis")
	redisDead = True


def add_prof(record):
	name = record['Name']
	if not conn.zscore('professors', name) is None:
		return
	conn.zadd('professors', name, 0)
	for i in range(1, len(name)):
		conn.zadd('auto_professors', name[:i], 0)
	conn.zadd('auto_professors', name + "*", 0)


def del_prof(record):
	name = record['Name']
	if conn.zscore('professors', name) is None:
		return
	conn.zrem('professors', name)
	conn.zrem('auto_professors', name + "*")


def add_class_to_prof(record):
	prof = record['Professor']
	number = record['Number']
	if conn.zscore('professors', prof) is None:
		return
	if not conn.zscore(number, prof) is None:
		return
	conn.zadd('classes', number, 0)
	conn.zadd(number, prof, 0)
	for i in range(1, len(number)):
		conn.zadd('auto_classes', number[:i], 0)
	conn.zadd('auto_classes', number + "*", 0)


def del_class_from_prof(record):
	if conn.zscore('professors', record['Professor']) is None:
		return
	if conn.zscore(record['Number'], record['Professor']) is None:
		return
	conn.zrem(record['Number'], record['Professor'])
	if conn.zcount(record['Number'], 0, -1) == 0:
		conn.zrem('classes', record['Number'])
	conn.zrem('auto_classes', record['Number'] + "*")

	
print("Data is being brought up to date!")
while True:
	time.sleep(1)
	#try:
	logs.remove({"mongo": -1, "redis": -1, "orient": -1})
	#except:
		#print("Mongo Down 1")
		#continue
		
	try:
		redisLogsTodo = logs.find({"redis": 0}).sort("$natural", 1)
		for record in redisLogsTodo:
			if record["type"] == "add_prof":
				try:
					add_prof(record)
				except:
					print("Redis down 1")
					break
			elif record["type"] == "del_prof":
				try:
					del_prof(record)
				except:
					print("Redis down 2")
					break
			elif record["type"] == "add_class_to_prof":
				try:
					add_class_to_prof(record)
				except:
					print("Redis down 3")
					break
			elif record["type"] == "del_class_from_prof":
				conn = None
				try:
					del_class_from_prof(record)
				except Exception as e:
					print(str(e))
					print("Redis down 4")
					break
			logs.update_one({'_id': record["_id"]}, {'$set': {'redis': -1}})
			print(record["type"] + " was executed!")

	except Exception as e:
		#print str(e)
		print("Mongo Down 2")
		continue