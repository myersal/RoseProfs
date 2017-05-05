'''
Created on Apr 27, 2017

@author: goebel
'''
import time

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














def rate_prof(r):
	
	username = r["Username"]
	professor = r["Professor"]
	comm = r["Communication"]
	grade = r["Grading"]
	helpp = r["Helpfulness"]
	cool = r["Coolness"]
	
	print("RATING PROF")
	if students.count({"Username": username} == 0):
		return
	if professors.count({"Name": professor} == 0):
		return
	students.update_one(
				{'Username': username},
				{'$addToSet': {
					'ProfRating':
						{
							'Name': professor,
							'Communication': comm,
							'Grading': grade,
							'Helpfulness': helpp,
							'Coolness': cool
						}
	
				}}
			)
		



def rate_class(r):

	username = r["Username"]
	professor = r["Professor"]
	clas = r["Class_Number"]
	work = r["Workload"]
	diff = r["Difficulty"]
	fun = r["Fun"]
	know = r["Professor_Knowledge"]

	print("RATING CLASS")
	if students.count({"Username": username} == 0):
		return
	if professors.count({"Name": professor} == 0):
		return

	students.update_one(
		{'Username': username},
		{'$addToSet': {
			'ClassRating': 
				{
					'Professor': professor,
					'Class_Number': clas,
					'Workload': work,
					'Difficulty': diff,
					'Fun': fun,
					'Professor_Knowledge': know
				}
		}}
	)



def add_prof(r):
	
	name = r["Name"]
	dept = r["Department"]

	if professors.count({"Name": name} != 0):
		return

	professors.insert_one(
		{
			'Name': name,
			'Department': dept
		}
	)

	
def create_forum(r):


	
	username = r["Username"]	
	message = r["Content"]
	time = r["Date"]
	subject = r["Subject"]
	boolProfessor = r["bool"]
	prof = r["Name"]
	
	if students.count({"Username": username} == 0):
		return


	pointer = db.forums.insert(
			{
				'Subject': subject,
				'Message':
					[
						{
							'Username': username,
							'Content': message,
							'Date': time
						}
					]
			}
		)
	
	if(boolProfessor.lower() == 'yes'):
			db.forums.update({'_id': pointer}, {'$set': {'professor': prof}})




#never called
def edit_prof_name(r):

	name = r["Name"]
	new_name = r["New_Name"]

	if professors.count({"Name": name} == 0):
		return

	professors.update_one(
		{'Name': str(name)},
		{'$set': {'Name': str(new_name)}}
	)


def edit_prof_dept(r):
	
	name = r["Name"]
	new_dept = r["Department"]
	
	if professors.count({"Name": name} == 0):
		return

	professors.update_one(
		{'Name': str(name)},
		{'$set': {'Department': str(new_dept)}}
	)


def del_prof(r):
	
	name = r["Name"]

	if professors.count({"Name": name} == 0):
		return

	professors.delete_one({'Name': str(name)})



def add_class_to_prof(r):
	
	professor = r["Name"]
	name = r["Name"]
	number = r["Number"]
	dept = r["Department"]
	alt_dept = r["Cross-list-Department"]
	gen = r["Generic"]

	if professors.count({"Name": professor} == 0):
		return
	
	if 1 == professors.count({'Name': professor, 'Classes': {'Number' : number}}):
		return


	professors.update_one(
		{'Name': str(professor)},
		{'$addToSet':{
			'Classes':
			{
				'Name': str(name),
				'Number': str(number),
				'Department': str(dept),
				'Cross-list-Department': str(alt_dept),
				'Generic': str(gen)
			}
		}}
	)
	
	


def edit_class_name(r):


	professor = r["Professor"]
	new_name = r["Name"]
	number = r["Number"]


	if professors.count({"Name": professor} == 0):
		return
	if 0 == professors.count({'Name': professor, 'Classes': {'Number' : number}}):
		return

	professors.update_one(
		{
			'Name': str(professor),
			'Classes.Number': str(number)
		},
		{'$set': {
			'Classes.$.Name': str(new_name)
		}}
	)


def edit_class_number(r):
	
	
	
	professor = r["Professor"]
	number = r["Number"]
	new_number = r["New_Number"]


	if professors.count({"Name": professor} == 0):
		return
	
	if 0 == professors.count({'Name': professor, 'Classes': {'Number' : number}}):
		return

	professors.update_one(
		{
			'Name': str(professor),
			'Classes.Number': str(number)
		},
		{'$set': {
			'Classes.$.Number': str(new_number)
		}}
	)



def edit_class_dept(r):

	professor = r["Professor"]
	number = r["Number"]
	new_dept = r["Department"]


	if professors.count({"Name": professor} == 0):
		return
	
	if 0 == professors.count({'Name': professor, 'Classes': {'Number' : number}}):
		return

	professors.update_one(
		{
			'Name': str(professor),
			'Classes.Number': str(number)
		},
		{'$set': {
			'Classes.$.Department': str(new_dept)
		}}
	)


def edit_class_alt_dept(r):
	
	professor = r["Professor"]

	number = r["Number"]

	new_alt_dept = r["Alt_Department"]


	if professors.count({"Name": professor} == 0):
		return
	
	if 0 == professors.count({'Name': professor, 'Classes': {'Number' : number}}):
		return

	professors.update_one(
		{
			'Name': str(professor),
			'Classes.Number': str(number)
		},
		{'$set': {
			'Classes.$.Cross-list-Department': str(new_alt_dept)
		}}
	)


def edit_class_gen(r):
	

	professor = r["Professor"]
	number = r["Number"]
	new_gen = r["Generic"]


	if professors.count({"Name": professor} == 0):
		return
	
	if 0 == professors.count({'Name': professor, 'Classes': {'Number' : number}}):
		return

	professors.update_one(
		{
			'Name': str(professor),
			'Classes.Number': str(number)
		},
		{'$set': {
			'Classes.$.Generic': str(new_gen)
		}}
	)



def del_class_from_prof(r):
	
	professor = r["Professor"]
	number = r["Number"]
	

	if professors.count({"Name": professor} == 0):
		return
	
	if 0 == professors.count({'Name': professor, 'Classes': {'Number' : number}}):
		return

	professors.update_one(
		{'Name': str(professor)},
		{'$pull': {
			'Classes': {
				'Number': str(number)
			}
		}}
	)
	



def add_student(r):
	
	
	username = r["Username"]
	password = r["Password"]
	year = r["Year"]
	major = r["Major"]

	if students.count({'Username': username}) != 0:
		return


	students.insert_one(
		{
				'Username': str(username),
				'Password': str(password),
				'Year': str(year),
				'Major': str(major)
		}
	)





# is never called, don't worry about it
def edit_student_username(r):
	
	username = r["Username"]
	new_username = r["New_Username"]
	
	if students.count({"Username": username} == 0):
		return


	students.update_one(
		{'Username': str(username)},
		{'$set': {'Username': str(new_username)}}
	)



def edit_student_password(r):
	
	username = r["Username"]
	new_password = r["New_Password"]
	
	if students.count({"Username": username} == 0):
		return

	students.update_one(
		{'Username': str(username)},
		{'$set': {'Password': str(new_password)}}
	)



def edit_student_year(r):
	
	
	
	username = r["Username"]
	new_year = r["New_Year"]
	
	if students.count({"Username": username} == 0):
		return

	students.update_one(
		{'Username': str(username)},
		{'$set': {'Year': str(new_year)}}
	)



def edit_student_major(r):
	
	username = r["Username"]

	new_major = r["New_Major"]
	
	if students.count({"Username": username} == 0):
		return

	students.update_one(
		{'Username': str(username)},
		{'$set': {'Major': str(new_major)}}
	)


def del_student(r):
	
	username = r["Username"]
	if students.count({"Username": username} == 0):
		return
	students.delete_one({'Username': str(username)})













































	
print("Data is being brought up to date!")
while True:
	time.sleep(1)
	try:
		logs.remove({"mongo": -1, "redis": -1, "orient": -1})
	except:
		print("Mongo Down to remove logs")
		continue
		
	try:
		mongoLogsTodo = logs.find({"mongo": 0}).sort("$natural", 1)
	except: 
		print("Mongo Down to get logs")
	try:
		for record in mongoLogsTodo:
			if record["type"] == "rate_prof":
				rate_prof(record)
			elif record["type"] == "rate_class":
				rate_class(record)
			elif record["type"] == "add_prof":
				add_prof(record)
			elif record["type"] == "create_forum":
				create_forum(record)
			elif record["type"] == "edit_prof_name":
				edit_prof_name(record)
			elif record["type"] == "edit_prof_dept":
				edit_prof_dept(record)
			elif record["type"] == "del_prof":
				del_prof(record)
			elif record["type"] == "add_class_to_prof":
				add_class_to_prof(record)
			elif record["type"] == "edit_class_name":
				edit_class_name(record)
			elif record["type"] == "edit_class_number":
				edit_class_number(record)
			elif record["type"] == "edit_class_dept":
				edit_class_dept(record)
			elif record["type"] == "edit_class_alt_dept":
				edit_class_alt_dept(record)
			elif record["type"] == "edit_class_gen":
				edit_class_gen(record)
			elif record["type"] == "del_class_from_prof":
				del_class_from_prof(record)
			elif record["type"] == "add_student":
				add_student(record)
			elif record["type"] == "edit_student_username":
				edit_student_username(record)
			elif record["type"] == "edit_student_password":
				edit_student_password(record)
			elif record["type"] == "edit_student_year":
				edit_student_year(record)
			elif record["type"] == "edit_student_major":
				edit_student_major(record)
			elif record["type"] == "del_student":
				del_student(record)
			logs.update_one({'_id': record["_id"]}, {'$set' : {'mongo': -1}})
			print(record["type"] + " was executed!")
			
			
	except Exception as e:
		print str(e)
		print("Mongo Down to execute logs")
		continue
	
	
	
	
	
	
	
	

