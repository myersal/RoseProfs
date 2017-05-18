'''
Created on Apr 27, 2017

@author: goebel
'''
import time

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
	mongoClient = MongoClient('mongodb://137.112.104.109', 40000)
	db = mongoClient['roseprofs']
	logs = db.logs
except:
	print("Could not connect to Mongo")

def orientRateProf(record):
	#TODO check to ensure the variables are the same
	professor = record['Professor']
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

	professor = record['Professor']
	username = record['Username']
	clas = record['Class_Number']
	diff = record['Difficulty']
	fun = record['Fun']
	know = record['Knowledge']
	work = record['Workload']
	
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
	
	name = record['Name']
	
	profs = client.command("select * from prof where name = '" + name + "'")
	if(len(profs) == 0):
		new_vertex = client.command("create vertex prof set name = '" + name + "'")
	else:
		print("the professor already exists")

def orientDelProf(record):
	name = record['Name']
	
	#don't need to check inputs since the sql check has already been done an if it doesn't exist then nothing occurs
	
	client.command("delete vertex prof where name = '" + name + "'")
	client.command("delete vertex prof_class where name = '" + name + "'")
	
def orientAddClassToProf(record):

	number = record['Number']
	professor = record['Professor']

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

	professor = record['Professor']
	number = record['Number']
	
	#don't need to check inputs since the sql check has already been done an if it doesn't exist then nothing occurs

	client.command("delete vertex prof_class where name = '" + professor + "' and number = '" + number + "'")
	

def orientAddStudent(record):
	username = record['Username']

	studs = client.command("select * from stud where username = '" + username + "'")
	if(len(studs) == 0):
		new_edge = client.command("create vertex stud set username = '" + username + "'")
	
def orientDeleteStudent(record):
	username = record['Username']
	
	#if the student doesn't exist then nothing occurs

	client.command("delete vertex stud where username = '" + username + "'")

		
def updateLog(record):
	logs.update_one({'_id': record["_id"]}, {'$set' : {'orient': -1}})
	
conn = True
print("Data is being brought up to date!")
while True:
	time.sleep(1)
	try:
		logs.remove({"mongo": -1, "redis": -1, "orient": -1})
	except:
		print("Mongo Down")
		continue
		
	try:
		orientLogsTodo = logs.find({"orient": 0}).sort("$natural", 1)
		#found one huge error in current logs!!! if it doesnt go through the first time then we need to continue the while loop, not continue the for loop
		if conn == False:
			try:
				client = pyorient.OrientDB("137.112.104.108", 2424)
				session_id = client.connect( "root", "wai3feex" )
				client.db_open("roseprofs", "admin", "admin")
				conn = True
			except:
				print("Orient Down Bro!")
				continue
		
		for record in orientLogsTodo:
			
				
				if (record["type"] == "rate_prof"):
					try:
						orientRateProf(record)
					except:
						print("Orient Down")
						conn = False
						break
					
				elif (record["type"] == "rate_class"):
					try:
						orientRateClass(record)
					except:
						print("Orient Down")
						conn = False
						break
					
				elif (record["type"] == "add_prof"):
					try:
						orientAddProf(record)
					except:
						print("Orient Down")
						conn = False
						break
					
				elif (record["type"] == "del_prof"):
					try:
						orientDelProf(record)
					except:
						print("Orient Down")
						conn = False
						break
				
				elif (record["type"] == "add_class_to_prof"):
					try:
						orientAddClassToProf(record)
					except:
						print("Orient Down")
						conn = False
						break
					
				elif (record["type"] == "del_class_from_prof"):
					try:
						orientDelClassFromProf(record)
					except Exception as e:
						print(str(e))
						print("Orient Down")
						conn = False
						break
				
				elif (record["type"] == "add_student"):
					try:
						orientAddStudent(record)
					except:
						print("Orient Down")
						conn = False
						break
				
				elif (record["type"] == "del_student"):
					try:
						orientDeleteStudent(record)
					except:
						print("Orient Down")
						conn = False
						break
				
				print(record['type'] + " was executed!")
				updateLog(record)
					
			
	except Exception as e:
		#print str(e)
		print("Mongo Down")
		continue
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	