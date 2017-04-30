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


def mongoRateProf(record):
	if students.count({"Username": record["Username"]} == 0):
		return
	if professors.count({"Name": record["Name"]} == 0):
		return
	res = students.update_one(
					{'Username': record["Username"]},
					{'$addToSet': {
						'ProfRating': 
						{
							'Name': record["Name"],
							'Communication': record["Communication"],
							'Grading': record["Grading"],
							'Helpfulness': record["Helpfulness"],
							'Coolness': record["Coolness"]
						}
				
					}}
				)	
	
print("Data is being brought up to date!")
while True:
	time.sleep(5)
	try:
		logs.remove({"mongo": -1, "redis": -1, "orient": -1})
	except:
		print("Mongo Down 1")
		continue
		
	try:
		mongoLogsTodo = logs.find({"mongo": 0}).sort("$natural", 1)
		for record in mongoLogsTodo:
			if record["type"] == "rateProf":
				mongoRateProf(record)
				logs.update_one({'_id': record["_id"]}, {'$set' : {'mongo': -1}})
			
	except Exception as e:
		print str(e)
		print("Mongo Down 2")
		continue

