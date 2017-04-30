'''
Created on Apr 27, 2017

@author: goebel
'''
import time
import re

try:
	import pyorient
	import pyorient.ogm
	client = pyorient.OrientDB("137.112.104.108", 2424)
	session_id = client.connect( "root", "wai3feex" )
	client.db_open("roseprofs", "admin", "admin")
except:
	print("Could Not Connect to Orient")

try:
	import pymongo
	from pymongo import MongoClient
	mongoClient = MongoClient('mongodb://csse:Poos4iko@137.112.104.109')
	db = mongoClient['rose-profs']
	logs = db.logs
except:
	print("Could not connect to Mongo")

def orientRateProf(record):
	professor = record['Name']
	student = record['Username']
	comm = record['Communication']
	grade = record['Grading']
	helpp = record['Helpfulness']
	cool = record['Coolness']
	
	profs = client.command("select * from prof where name = '" + professor + "'")
	studs = client.command("select * from stud where username = '" + student + "'")
	
	#findUp = client.command("select * from prof_rate where out = " + studs[0]._rid + " and in = " + profs[0]._rid + " and cool = " + str(cool) + " and help = " + str(helpp) + "and comm = " + str(comm) + " and grad = " + str(grade))
	
	if(len(profs) != 0 and len(studs) != 0):
		currentEdges = client.command("select * from prof_rate where out = " + studs[0]._rid + " and in = " + profs[0]._rid);
		if(len(currentEdges) == 0):
			client.command("create edge prof_rate from " + studs[0]._rid + " to " + profs[0]._rid + " set cool = " + str(cool) + ", help = " + str(helpp) + ", comm = " + str(comm) + ", grad = " + str(grade));

	return 1;	
	
print("Data is being brought up to date!")
while True:
	time.sleep(5)
	try:
		logs.remove({"mongo": -1, "redis": -1, "orient": -1})
	except:
		print("Mongo Down")
		continue
		
	try:
		orientLogsTodo = logs.find({"orient": 0}).sort("$natural", 1)
		for record in orientLogsTodo:
			if (record["type"] == "rateProf"):
				try:
					orientRateProf(record)
				except:
					print("Orient Down")
					continue
				logs.update_one({'_id': record["_id"]}, {'$set' : {'orient': -1}})
					
			
	except Exception as e:
		#print str(e)
		print("Mongo Down")
		continue
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	