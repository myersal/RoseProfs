#Give profs a rating

import pymongo
import redis
import sys

try:
	import pyorient
	import pyorient.ogm

	client = pyorient.OrientDB("localhost", 2424);
	session_id = client.connect( "root", "wai3feex" );
	client.db_open( DB_Demo, "admin", "admin" );
except:
	print("Orient DB not working")

conn = redis.Redis()

mongClient = MongoClient()
db = mongClient['rose-profs']
students = db.Students
profs = db.Professors


print("WELCOME TO THE Rose Profs")
print("\n")
print("Please type your username to log in.\n")

while (True):
	username = raw_input(':')
	if (students.count({"Username": username} != 0):
		print("Welcome" + students.find({"Username": username}, {"Name" : True})
		break
	else
		print("Not a valid username. Please try again")

while (True):
	print("What would you like to do?")
	cmd = raw_input(':')
	while (True):
		if (cmd.lower() == "rate")
			print("What professor would you like to rate?")
			prof = raw_input(':')
			if (profs.count({"Name" : prof} == 0)
				print("That is not a prof")
				break
			points = 8;
			print("You have 8 points to distribute among these four catagories: Communication\nGrading\nHelpfulness\nCoolness")
			print("On a scale from 0-4 with 4 being the most positive, \nhow do you rank this professors Communication?  \nYou have " + points + " points left!")
			comm = raw_input(':')
			try:
				comm = int(comm)
			except:
				print("That is not a integer between 0 and 4")
				break
			points = points - comm
			if (points < 0)
				print("You have distributed too many points!")
				break
			if (comm > 4)
				print("The max rating is 4")
				break
				
				
			print("On a scale from 0-4 with 4 being the most positive, \nhow do you rank this professors Grading?  \nYou have " + points + " points left!")
			grade = raw_input(':')
			try:
				grade = int(grade)
			except:
				print("That is not a integer between 0 and 4")
				break
			points = points - grade
			if (points < 0)
				print("You have distributed too many points!")
				break
			if (grade > 4)
				print("The max rating is 4")
				break
				
				
			print("On a scale from 0-4 with 4 being the most positive, \nhow do you rank this professors Helpfulness?  \nYou have " + points + " points left!")
			help = raw_input(':')
			try:
				help = int(help)
			except:
				print("That is not a integer between 0 and 4")
				break
			points = points - help
			if (points < 0)
				print("You have distributed too many points!")
				break
			if (help > 4)
				print("The max rating is 4")
				break
			
			cool = points
			print("That leaves " + points + " points for the coolness rating!")
			
			
			
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	


