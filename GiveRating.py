#Give profs a rating

import pymongo
from pymongo import MongoClient
import redis
from pprint import pprint
import sys

try:
	import pyorient
	import pyorient.ogm

	client = pyorient.OrientDB("localhost", 2424);
	session_id = client.connect( "root", "wai3feex" );
	client.db_open( "DB_Demo", "root", "wai3feex" );
except:
	print("Orient DB not working")

conn = redis.Redis()
mongoClient = MongoClient()
db = mongoClient['rose-profs']
students = db.students
professors = db.professors
print("GO")



def add_prof(name, dept):
	cursor = professors.find({'Name': str(name)})
	if cursor:
		return 0
	res = professors.insert_one(
		{
			'Name': str(name),
			'Department': str(dept)
		}
	)
	conn.zadd("professors", name, 0)
	return res


def edit_prof_name(name, new_name):
	res = professors.update_one(
		{'Name': str(name)},
		{'$set': {'Name': str(new_name)}}
	)
	conn.zrem("professors", name)
	conn.zadd("professors", new_name, 0)
	classes = conn.zmembers("classes")
	for c in classes:
		if conn.zrem(c, name):
			conn.zadd(c, new_name)
	return res


def edit_prof_dept(name, new_dept):
	res = professors.update_one(
		{'Name': str(name)},
		{'$set': {'Department': str(new_dept)}}
	)
	return res


def del_prof(name):
	res = professors.delete_one({'Name': str(name)})
	conn.zrem("professors", name)
	classes = conn.zmembers("classes")
	for c in classes:
		conn.zrem(c, name)
	return res


def add_class_to_prof(professor, name, number, dept, alt_dept, gen):
	res = professors.update_one(
		{'Name': str(professor)},
		{'$addToSet':{
			'Classes:'
			[
				'Name': str(name),
				'Number': str(number),
				'Department': str(dept),
				'Cross-list-Department': str(alt_dept),
				'Generic': str(gen)
			]
		}}
	)
	conn.zadd("classes", number)
	conn.zadd(number, professor)
	return res


def edit_class_name(professor, number, new_name):
	res = professors.update_one(
		{
			'Name': str(professor),
			'Classes.Number': str(number)
		},
		{'$set': {
			'Classes.$.Name': str(new_name)
		}}
	)
	return res


def edit_class_number(professor, number, new_number):
	res = professors.update_one(
		{
			'Name': str(professor),
			'Classes.Number': str(number)
		},
		{'$set': {
			'Classes.$.Number': str(new_number)
		}}
	)
	return res


def edit_class_dept(professor, number, new_dept):
	res = professors.update_one(
		{
			'Name': str(professor),
			'Classes.Number': str(number)
		},
		{'$set': {
			'Classes.$.Department': str(new_dept)
		}}
	)
	return res


def edit_class_alt_dept(professor, number, new_alt_dept):
	res = professors.update_one(
		{
			'Name': str(professor),
			'Classes.Number': str(number)
		},
		{'$set': {
			'Classes.$.Cross-list-Department': str(new_alt_dept)
		}}
	)
	return res


def edit_class_gen(professor, number, new_gen):
	res = professors.update_one(
		{
			'Name': str(professor),
			'Classes.Number': str(number)
		},
		{'$set': {
			'Classes.$.Generic': str(new_gen)
		}}
	)
	return res


def del_class_from_prof(professor, number):
	res = professors.update_one(
		{'Name': str(professor)},
		{'$pull': {
			'Classes': {
				'Number': str(number)
			}
		}}
	)
	conn.zrem(number, professor)
	if not conn.zmembers(number):
		conn.zrem("classes", number)
		conn.delete(number)
	return res


def add_student(username, password, year, major):
	cursor = students.find({'Username': str(username)})
	if cursor:
		return 0
	res = students.insert_one(
		{
			'Username': str(username),
			'Password': str(password),
			'Year': str(year),
			'Major': str(major)
		}
	)
	return res


def edit_student_username(username, new_username):
	res = students.update_one(
		{'Username': str(username)},
		{'$set': {'Username': str(new_username)}}
	)
	return res


def edit_student_password(username, new_password):
	res = students.update_one(
		{'Username': str(username)},
		{'$set': {'Password': str(new_password)}}
	)
	return res


def edit_student_year(username, new_year):
	res = students.update_one(
		{'Username': str(username)},
		{'$set': {'Year': str(new_year)}}
	)
	return res


def edit_student_major(username, new_major):
	res = students.update_one(
		{'Username': str(username)},
		{'$set': {'Major': str(new_major)}}
	)
	return res

def del_student(username):
	res = students.delete_one({'Username': str(username)})
	return res

print("WELCOME TO THE Rose Profs")
print("\n")
print("Please type your username to log in.\n  Or type new to make a new user")

while (True):
	username = raw_input(':')
	if username == "new":
		print("What would you like your username to be?")
		username = raw_input(':')
		if (username == ""):
			print ("Username cannot be empty")
                elif students.count({"Username": username} != 0):
                        print("Username is already taken")
		else:
			print("What would you like to be your password?")
			pwd = raw_input(':')
			print("What is your year?")
			year = raw_input(':')
			print("What is your primary major?")
			major = raw_input(':')
			add_student(username, pwd, year, major)
			print("User added")
			break		
			
			
			
	elif students.count({"Username": username}) != 0:
                curs = students.find({"Username": username}, {"Name" : True})
                for c in curs:
                        print("Welcome ")
                        pprint(c)
		break
	else:
		print("Not a valid username. Please try again")

while (True):
	print("What would you like to do?")
	cmd = raw_input(':')
	while (True):
		if cmd.lower() == "rate":
			print("What professor would you like to rate?")
			prof = raw_input(':')
			try:
				int(conn.zscore("professors", prof))
			except:
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
			if (points < 0):
				print("You have distributed too many points!")
				break
			if (comm > 4):
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
			if (points < 0):
				print("You have distributed too many points!")
				break
			if (grade > 4):
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
			if (points < 0):
				print("You have distributed too many points!")
				break
			if (help > 4):
				print("The max rating is 4")
				break
			
			cool = points
			print("That leaves " + points + " points for the coolness rating!")
			
			
			students.update({"Username": username}, {"$addToSet": {"ProfRatings": {'Professor': prof,'Communication':comm, "Grading": grade, "Helpfulness" : help, "Coolness" : cool}}})
			
			try:
				edgeName = username + prof
				client.command("INSERT INTO " + edgeName +" ( 'comm','grad','help','cool' ) VALUES(" + comm + ", " + grade + ", "+ help +", "+ cool +")");
			except:
				print("FAIL OF ORIENT")
				break;

		
		elif(cmd.lower() == "edit major" or cmd.lower() == "editmajor"):
			print("What is your new major?")
			maj = raw_input(':')
			edit_student_major(username, maj)
			print("Major changed!")
	
		elif(cmd.lower() == "edit year" or cmd.lower() == "edityear"):
			print("What is your new year?")
			year = raw_input(':')
			edit_student_year(username, year)
			print("Year changed!")
		
		elif(cmd.lower() == "edit password" or cmd.lower() == "editpassword"):
			print("What is your new password?")
			pwd = raw_input(':')
			edit_student_password(username, pwd)
			print("Password changed!")
	
		elif(cmd.lower() == "edit username" or cmd.lower() == "editusername"):
			print("What is your new username?")
			pwd = raw_input(':')
			if students.count({"Username": username} == 0):
				edit_student_password(username, pwd)
				print("Username changed!")
			else:
				print("Username exists!")
				break
			
		elif(cmd.lower() == "add prof" or cmd.lower() == "addprof" or cmd.lower() == "add professor" or cmd.lower() == "addprofessor"):
			print("Who is the new Professor?")
			name = raw_input(':')
                        if professors.count({"Name": name} != 0):
				print("Professor exists already")
                                break
			print("What is his/her department")
			dept = raw_input(':')
			add_prof(name, dept)
			print("Prof added!")
			
		
		elif(cmd.lower() == "edit department" or cmd.lower() == "editdepartment"):
			print("Who is the Professor?")
			name = raw_input(':')
			print("What is his/her new department")
			dept = raw_input(':')
			edit_prof_dept(name, dept)
			print("Department changed!")
			
		
		elif(cmd.lower() == "edit professor name" or cmd.lower() == "editprofessorname" or cmd.lower() == "edit prof name" or cmd.lower() == "editprofname"):
			print("Who is the Professor?")
			name = raw_input(':')
			print("What is his/her new name?")
			newname = raw_input(':')
			
			if professors.count({"Name": newname} == 0):
				edit_prof_name(name, newname)
				print("Professor name changed!")
			else:
				print("Professor name exists!")
				break
				
		
			
		elif(cmd.lower() == "delete professor" or cmd.lower() == "deleteprofessor" or cmd.lower() == "delete prof" or cmd.lower() == "deleteprof"):
			print("Who is the Professor to be deleted?")
			name = raw_input(':')
			
			if professors.count({"Name": name} > 0):
				del_prof(name)
				print("Professor deleted")
			else:
				print("Professor does not exist!")
				break
	
                elif(cmd.lower() == "end" or cmd.lower() == "End" or cmd.lower() == "END" or cmd.lower() == "quit"):
			pizza = 8 / 0
	
		elif(cmd.lower() == "new class" or cmd.lower() == "new class"):
			print("Who is the Professor who teaches the class?")
			professor = raw_input(':')
			if professors.count({"Name": professor} == 0):
				print("Professor does not exist")
				break
			print("What is the name of the class?")
			name = raw_input(':')
			print("What is the number of the class?")
			num = raw_input(':')
			print("What is the department of the class?")
			dept = raw_input(':')
			print("What is the cross-list department of the class?")
			alt_dept = raw_input(':')
			print("Is this a general class? \"yes\" or \"no\"")
			gen = raw_input(':')
			if (gen.lower() == "yes" or gen.lower == "y"):
				gen = "True"
			if (gen.lower() == "no" or gen.lower == "n"):
				gen = "False"
			if (gen != "False" or gen != "True"):
				print("Invalid input. Make sure it is yes or no")
				break
			add_class_to_prof(professor, name, num, dept, alt_dept, gen)

			
			
			
			
	
		#elif(cmd.lower() = "edit class name" or cmd.lower() = "edit classname" or cmd.lower() = "editclassname" or cmd.lower() = "editclass name"):
			#print("What is the professor of the class to be edited?")
			#professor = raw_input(':')
			#if profs.count({"Name": professor} == 0):
				#print("Professor does not exist")
				#break
			#print("What is the number of the class to be edited?")
			#num = raw_input(':')
			#try:
				#int(conn.zrank("classes", num))
			#except:
				#print("Not a valid class number")
				#break
				
			#print("What is the new name?")
			#new_name = raw_input(':')
			
			
			#edit_class_name(professor, num, new_name)


				


		elif(cmd.lower() == "delete class" or cmd.lower() == "deleteclass"):
			print("Who is the Professor who teaches the class?")
			professor = raw_input(':')
			if professors.count({"Name": professor} == 0):
				print("Professor does not exist")
				break
			print("What is the number of the class?")
			num = raw_input(':')
			try:
				int(conn.zrank("classes", num))
			except:
				print("Not a valid class number")
				break
			del_class_from_prof(professor, num)

                else:
                        print("Invalid command")
                        break
                break
		


	
	


