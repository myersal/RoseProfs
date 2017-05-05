'''
Created on Apr 26, 2017

@author: goebel
'''
import RoseProfConnections
import CommonFunctions
from CommonFunctions import *
from RoseProfConnections import *
from time import gmtime, strftime;
from datetime import datetime


def rateProf(username, professor, comm, grade, helpp, cool):
	if SQLInjectionCheck(username):
		print("Username cannot contain special characters")
		return
	if SQLInjectionCheck(professor):
		print("Professor cannot contain special characters")
		return
	if SQLInjectionCheck(comm):
		print("Communication score cannot contain special characters")
		return
	if SQLInjectionCheck(grade):
		print("Grading score cannot contain special characters")
		return
	if SQLInjectionCheck(helpp):
		print("Helpful score cannot contain special characters")
		return
	if SQLInjectionCheck(cool):
		print("Coolness score cannot contain special characters")
		return
	if students.count({"Username": username} == 0):
		return
	if not conn.zscore('professors', professor) > 0:
		return

	try:
		log = logs.insert_one({
			'mongo': 0, 'redis': 0, 'orient': 0, 'type': 'rate_prof', 'Username': username, 'Professor': professor,
			'Communication': comm, 'Grading': grade, 'Helpfulness': helpp, 'Coolness': cool})
	except:
		print("Sorry but Rose Profs is down.  Please try again later.")
		exit()
	return log


def rateClass(username, professor, clas, work, diff, fun, know):
	if SQLInjectionCheck(username):
		print("Username cannot contain special characters")
		return
	if SQLInjectionCheck(professor):
		print("Professor cannot contain special characters")
		return
	if SQLInjectionCheck(clas):
		print("Class Number cannot contain special characters")
		return
	if SQLInjectionCheck(work):
		print("Workload score cannot contain special characters")
		return
	if SQLInjectionCheck(diff):
		print("Difficulty score cannot contain special characters")
		return
	if SQLInjectionCheck(fun):
		print("Fun score cannot contain special characters")
		return
	if SQLInjectionCheck(know):
		print("Knowledge score cannot contain special characters")
		return
	if students.count({"Username": username} == 0):
		return
	if not conn.zscore('professors', professor) > 0:
		return
	if not conn.zscore(clas, professor) > 0:
		return

	log = logs.insert_one({
		'mongo': 0, 'redis': 0, 'orient': 0, 'type': 'rate_class', 'Username': username, 'Professor': professor,
		'Class_Number': clas, 'Workload': work, 'Difficulty': diff, 'Fun': fun, 'Knowledge': know})
	return log


def add_prof(name, dept):
	if SQLInjectionCheck(name):
		print("Professor cannot contain special characters")
		return
	if SQLInjectionCheck(dept):
		print("Department cannot contain special characters")
		return
	if conn.zscore('professors', name) > 0:
		return

	log = logs.insert_one({
		'mongo': 0, 'redis': 0, 'orient': 0, 'type': 'add_prof', 'Name': name, 'Department': dept})

	return log

def addProf(name):
	profs = client.command("select * from prof where name = '" + name + "'")
	if len(profs) == 0:
		new_vertex = client.command("create vertex prof set name = '" + name + "'")
	else:
		print("the professor already exists")

	
def createForum(username):

	subject = raw_input('what is your subject: ')


	boolProffessor = raw_input('do you want to list what professor yes/no (if neither is input no is assumed): ')


	if boolProffessor.lower() == 'yes':
		prof = raw_input('please input the professor\'s name: ')
		numOfProfs = -1
		if not RoseProfConnections.redisDead:
			try:
				numOfProfs = conn.zscore("professors", prof)
			except:
				print("Some functionality may be slower and/or limited due to problems outside of your control")
				RoseProfConnections.redisDead = True
		if RoseProfConnections.redisDead:
			try:
				numOfProfs = professors.count({"Name": prof})
				if numOfProfs == 0:
					print("That is not a prof")
					return
			except:
				print("Sorry, but Rose Profs is currently down.  Please try again later")
				exit()
		try:
			int(numOfProfs)
		except:
			print("That is not a prof")
			return
			
		
	message = raw_input('please type your message for the forum: ')

	#Now for the important part, the above may change when the application is actually in user

	answer = raw_input('is the given information correct yes/no (no if yes is not input): ')

	if(answer.lower() == 'yes'):
		time = strftime('%Y-%j-%d %H:%M:%S', gmtime())

		mongLog = logs.insert_one({
			'mongo': 0, 'redis': 0, 'orient': 0, 'type': 'create_forum', 'Subject': subject,
			'Username': username, 'Content': message, 'Date': time})

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
		
		if(boolProffessor.lower() == 'yes'):
			print(pointer)
			print('attempting')
			db.forums.update({'_id': pointer}, {'$set': {'professor': prof}})
		
		print('forum created')


#never called
def edit_prof_name(name, new_name):
	if not conn.zscore('professors', name) > 0:
		return
	log = logs.insert_one({
		'mongo': 0, 'redis': 0, 'orient': 0, 'type': 'edit_prof_name', 'Name': name, 'New_Name': new_name})

	res = professors.update_one(
		{'Name': str(name)},
		{'$set': {'Name': str(new_name)}}
	)
	conn.zrem("professors", name)
	conn.zadd("professors", new_name, "0")
	classes = conn.zrangebyscore("classes", 0, -1)
	for c in classes:
		if conn.zrem(c, name):
			conn.zadd(c, new_name, "0")
	return res


def edit_prof_dept(name, new_dept):
	if not conn.zscore('professors', name) > 0:
		return
	log = logs.insert_one({
		'mongo': 0, 'redis': 0, 'orient': 0, 'type': 'edit_prof_dept', 'Name': name, 'Department': new_dept})
	return log


def del_prof(name):
	if (SQLInjectionCheck(name)):
		print("professor cannot contain special characters")
		return
	if not conn.zscore('professors', name) > 0:
		return

	log = logs.insert_one({
		'mongo': 0, 'redis': 0, 'orient': 0, 'type': 'del_prof', 'Name': name})

	return log


def add_class_to_prof(professor, name, number, dept, alt_dept, gen):
	
	if SQLInjectionCheck(professor):
		print("professor cannot contain special characters")
		return
	if SQLInjectionCheck(name):
		print("Username cannot contain special characters")
		return
	if SQLInjectionCheck(number):
		print("Number cannot contain special characters")
		return
	if SQLInjectionCheck(dept):
		print("Dept cannot contain special characters")
		return
	if SQLInjectionCheck(alt_dept):
		print("alt_dept cannot contain special characters")
		return
	if SQLInjectionCheck(gen):
		print("gen cannot contain special characters")
		return
	if not conn.zscore('professors', professor) > 0:
		return
	if conn.zscore(number, professor) > 0:
		return

	log = logs.insert_one({
		'mongo': 0, 'redis': 0, 'orient': 0, 'type': 'add_class_to_prof', 'Professor':professor, 'Name': name,
		'Number': str(number), 'Department': str(dept), 'Cross-list-Department': str(alt_dept), 'Generic': str(gen)})

	return log


def edit_class_name(professor, number, new_name):
	if not conn.zscore('professors', professor) > 0:
		return
	if not conn.zscore(number, professor) > 0:
		return

	log = logs.insert_one({
		'mongo': 0, 'redis': -1, 'orient': -1, 'type': 'edit_class_name', 'Professor': professor, 'Number': number,
		'Name': new_name})

	return log


def edit_class_number(professor, number, new_number):
	if not conn.zscore('professors', professor) > 0:
		return
	if not conn.zscore(number, professor) > 0:
		return

	log = logs.insert_one({
		'mongo': 0, 'redis': 0, 'orient': 0, 'type': 'edit_class_number', 'Professor': professor, 'Number': number,
		'New_Number': new_number})

	return log


def edit_class_dept(professor, number, new_dept):
	if not conn.zscore('professors', professor) > 0:
		return
	if not conn.zscore(number, professor) > 0:
		return

	log = logs.insert_one({
		'mongo': 0, 'redis': 0, 'orient': 0, 'type': 'edit_class_dept', 'Professor': professor,
		'Number': number, 'Department': new_dept})

	return log


def edit_class_alt_dept(professor, number, new_alt_dept):
	if not conn.zscore('professors', professor) > 0:
		return
	if not conn.zscore(number, professor) > 0:
		return

	log = logs.insert_one({
		'mongo': 0, 'redis': 0, 'orient': 0, 'type': 'edit_class_alt_dept', 'Professor': professor,
		'Number': number, 'Alt_Department': new_alt_dept})

	return log


def edit_class_gen(professor, number, new_gen):
	if not conn.zscore('professors', professor) > 0:
		return
	if not conn.zscore(number, professor) > 0:
		return

	log = logs.insert_one({
		'mongo': 0, 'redis': 0, 'orient': 0, 'type': 'edit_class_gen', 'Professor': professor,
		'Number': number, 'Generic': new_gen})
	return log


def del_class_from_prof(professor, number):
	if SQLInjectionCheck(professor):
		print("Professor cannot contain special characters")
		return
	if SQLInjectionCheck(number):
		print("Number cannot contain special characters")
		return
	if not conn.zscore('professors', professor) > 0:
		return
	if conn.zscore(number, professor) > 0:
		return

	log = logs.insert_one({
		'mongo': 0, 'redis': 0, 'orient': 0, 'type': 'del_class_from_prof', 'Professor': professor,
		'Number': number})
	return log


def add_student(username, password, year, major):
	if SQLInjectionCheck(username):
		print("usernames cannot contain special characters")
		return
	if students.count({'Username': username}) != 0:
		return

	log = logs.insert_one({
		'mongo': 0, 'redis': 0, 'orient': 0, 'type': 'add_student', 'Username': str(username),
		'Password': str(password), 'Year': str(year), 'Major': str(major)})

	return log


def addStudent(username):
	studs = client.command("select * from stud where username = '" + username + "'")
	if(len(studs) == 0):
		new_edge = client.command("create vertex stud set username = '" + username + "'")
	else:
		print("the user already exists")


# is never called, don't worry about it
def edit_student_username(username, new_username):
	if students.count({'Username': username}) <= 0:
		return
	if students.count({'Username': new_username}) != 0:
		return
	log = logs.insert_one({
		'mongo': 0, 'redis': 0, 'orient': 0, 'type': 'edit_student_username', 'Username': username,
		'New_Username': new_username})

	return log


def edit_student_password(username, new_password):
	if students.count({'Username': username}) <= 0:
		return

	log = logs.insert_one({
		'mongo': 0, 'redis': 0, 'orient': 0, 'type': 'edit_student_password', 'Username': username,
		'Password': str(new_password)})

	return log


def edit_student_year(username, new_year):
	if students.count({'Username': username}) <= 0:
		return

	log = logs.insert_one({
		'mongo': 0, 'redis': 0, 'orient': 0, 'type': 'edit_student_year', 'Username': username,
		'Year': str(new_year)})

	return log


def edit_student_major(username, new_major):
	if students.count({'Username': username}) <= 0:
		return

	log = logs.insert_one({
		'mongo': 0, 'redis': 0, 'orient': 0, 'type': 'edit_student_major', 'Username': username,
		'Major': str(new_major)})

	return log


def del_student(username):
	if SQLInjectionCheck(username):
		print("Number cannot contain special characters")
		return
	if students.count({'Username': username}) != 0:
		return

	log = logs.insert_one({
		'mongo': 0, 'redis': 0, 'orient': 0, 'type': 'del_student', 'Username': username})

	return log
