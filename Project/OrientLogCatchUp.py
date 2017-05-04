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
	#TODO check to ensure the variables are the same
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

def orientRateClass(record):

	professor = record['Name']
	username = record['Username']
	clas = record['Class']
	diff = record['Difficulty']
	
	#TODO need to finish variables and check to see if above are correct
	
	classes = client.command("select * from prof_class where name = '" + professor + "' and number = '" + clas + "'");
	studs = client.command("select * from stud where username = '" + username + "'");

	if (len(classes) != 0 and len(studs) != 0):
		currentEdges = client.command(
			"select * from class_rate where out = " + studs[0]._rid + " and in = " + classes[0]._rid);

		if (len(currentEdges) == 0):
			# insert edge
			new_edge = client.command(
				"create edge class_rate from " + studs[0]._rid + " to " + classes[0]._rid + " set work = " + str(
					work) + ", diff = " + str(diff) + ", fun = " + str(fun) + ", know = " + str(know));

		else:
			return 0
	else:
		return 0
		
def orientAddProf(record):
	#TODO need to add variables in
	
	
	profs = client.command("select * from prof where name = '" + name + "'")
	if(len(profs) == 0):
		new_vertex = client.command("create vertex prof set name = '" + name + "'")
	else:
		print("the professor already exists")

def orientDelProf(record):
	#TODO need to add variables in
	
	#don't need to check inputs since the sql check has already been done an if it doesn't exist then nothing occurs
	
	client.command("delete vertex prof where name = '" + name + "'")

def orientAddClassToProf(record):

	#TODO need to add variables in

	checkClass = client.command("select * from class where number = '" + number +"'");
	classes = [];
	if len(checkClass) == 0:
		classes = client.command("create vertex class set number = '" + number + "'")
	else:
		classes = client.command("select * from class where number = '" + number + "'")
	
	profs = client.command("select * from prof where name = '" + professor + "'")
	if len(classes) > 0 and len(profs) > 0:
		newVars = client.command("SELECT * FROM prof_class WHERE number = '" + number + "' AND name = '" + professor + "'")
		if (len(newVars) > 0):
			return 0
		new_vertex = client.command("create vertex prof_class set number = '" + number + "', name = '" + professor + "'")
		new_edge = client.command("create edge teaches from " + profs[0]._rid + " to " + new_vertex[0]._rid)
		new_edge2 = client.command("create edge class_of from " + new_vertex[0]._rid + " to " + classes[0]._rid)
	else:
		return 0

	return 1
	
def orientDelClassFromProf(record):

	#TODO need to add variables in
	
	#don't need to check inputs since the sql check has already been done an if it doesn't exist then nothing occurs

	client.command("delete vertex prof_class where name = '" + professor + "' and number = '" + number + "'")
	

def orientAddStudent(record):
	#TODO need to add variables in

	studs = client.command("select * from stud where username = '" + username + "'")
	if(len(studs) == 0):
		new_edge = client.command("create vertex stud set username = '" + username + "'")
	
def orientDeleteStudent(record):
	#TODO need to add variables in
	
	#if the student doesn't exist then nothing occurs

	client.command("delete vertex stud where username = '" + username + "'")

		
def updateLog(record):
	logs.update_one({'_id': record["_id"]}, {'$set' : {'orient': -1}})
	
	
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
				
			elif:
				
				
			else:
				try:
					updateLog(record)
					
			
	except Exception as e:
		#print str(e)
		print("Mongo Down")
		continue
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	