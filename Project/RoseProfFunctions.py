'''
Created on Apr 26, 2017

@author: goebel
'''
import RoseProfConnections
import CommonFunctions
from CommonFunctions import *
from RoseProfConnections import *
from time import gmtime, strftime;


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
	if SQLInjectionCheck(help):
		print("Helpful score cannot contain special characters")
		return
	if SQLInjectionCheck(cool):
		print("Coolness score cannot contain special characters")
		return
	
	profs = client.command("select * from prof where name = '" + professor + "'");
	studs = client.command("select * from stud where username = '" + username  + "'");

	if(len(profs) != 0 and len(studs) != 0):
		currentEdges = client.command("select * from prof_rate where out = " + studs[0]._rid + " and in = " + profs[0]._rid);

		if(len(currentEdges) == 0):
			#insert edge
			new_edge = client.command("create edge prof_rate from " + studs[0]._rid + " to " + profs[0]._rid + " set cool = " + str(cool) + ", help = " + str(helpp) + ", comm = " + str(comm) + ", grad = " + str(grade));
		
		else:
			print("the user has already rated the professor");
			return 0;
	else:
		print("the professor does not exist")
		return 0

	res = students.update_one(
		{'Username': username},
		{'$addToSet': {
			'ProfRating': {
				{
					'Name': professor,
					'Communication': comm,
					'Grading': grade,
					'Helpfulness': helpp,
					'Coolness': cool
				}
			}
		}}
	)
	return res


def rateClass(username, professor, clas, work, diff, fun, know):
	if (SQLInjectionCheck(username)):
		print("Username cannot contain special characters")
		return
	if (SQLInjectionCheck(professor)):
		print("Professor cannot contain special characters")
		return
	if (SQLInjectionCheck(clas)):
		print("Class Number cannot contain special characters")
		return
	if (SQLInjectionCheck(work)):
		print("Workload score cannot contain special characters")
		return
	if (SQLInjectionCheck(diff)):
		print("Difficulty score cannot contain special characters")
		return
	if (SQLInjectionCheck(fun)):
		print("Fun score cannot contain special characters")
		return
	if (SQLInjectionCheck(know)):
		print("Knowledge score cannot contain special characters")
		return

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
			print("the user has already rated the professor")
			return 0
	else:
		print("class does not exist")
		return 0

	res = students.update_one(
		{'Username': username},
		{'$addToSet': {
			'ClassRating': {
				{
					'Professor': professor,
					'Class_Number': clas,
					'Workload': work,
					'Difficulty': diff,
					'Fun': fun,
					'Professor_Knowledge': know
				}
			}
		}}
	)
	return res


def add_prof(name, dept):
	if professors.count({'Name': str(name)}) != 0:
		return 0
	
	if (SQLInjectionCheck(name)):
		print("Professor cannot contain special characters")
		return
		
	if (SQLInjectionCheck(dept)):
		print("Department cannot contain special characters")
		return
	
	res = professors.insert_one(
		{
			'Name': str(name),
			'Department': str(dept)
		}
	)
	conn.zadd("professors", name, "0")
	try:
		addProf(name)
	except:
		print("Orient Failed to add prof")
	return res
	
def addProf(name):
	profs = client.command("select * from prof where name = '" + name + "'")
	if(len(profs) == 0):
		new_vertex = client.command("create vertex prof set name = '" + name + "'")
	else:
		print("the professor already exists")
	

	
def createForum(username):
	if (SQLInjectionCheck(username)):
		print("Username cannot contain special characters")
		return
	subject = raw_input('what is your subject: ')
	if (SQLInjectionCheck(subject)):
		print("Subject cannot contain special characters")
		return

	boolProffessor = raw_input('do you want to list what professor yes/no (if neither is input no is assumed): ')


	if(boolProffessor.lower() == 'yes'):
		prof = raw_input('please input the professor\'s name: ')
		if (SQLInjectionCheck(prof)):
			print("Professor name cannot contain special characters")
			return
		
	message = raw_input('please type your message for the forum: ')

	#Now for the important part, the above may change when the application is actually in user

	answer = raw_input('is the given information correct yes/no (no if yes is not input): ');

	if(answer.lower() == 'yes'):
		time = strftime('%Y-%j-%d %H:%M:%S', gmtime());

		pointer = db.forums.insert(
			{
				'subject': subject,
				'message':
					{
						'username': username,
						'content': message,
						'date': time
					}
			}
		);
		
		if(boolProffessor.lower() == 'yes'):
			print(pointer);
			print('attempting');
			db.forums.update({'_id': pointer}, {'$set': {'proffessor': prof}});
		
		print('forum created');

#never called
def edit_prof_name(name, new_name):
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
	res = professors.update_one(
		{'Name': str(name)},
		{'$set': {'Department': str(new_dept)}}
	)
	return res


def del_prof(name):

	if (SQLInjectionCheck(name)):
		print("professor cannot contain special characters")
		return

	res = professors.delete_one({'Name': str(name)})
	conn.zrem("professors", name)
	classes = conn.zrangebyscore("classes", 0, -1)
	for c in classes:
		conn.zrem(c, name)
		
	client.command("delete vertex prof where name = '" + name + "'")
	
	return res


def add_class_to_prof(professor, name, number, dept, alt_dept, gen):
	
	if (SQLInjectionCheck(professor)):
		print("professor cannot contain special characters")
		return
	if (SQLInjectionCheck(name)):
		print("Username cannot contain special characters")
		return
	if (SQLInjectionCheck(number)):
		print("Number cannot contain special characters")
		return
	if (SQLInjectionCheck(dept)):
		print("Dept cannot contain special characters")
		return
	if (SQLInjectionCheck(alt_dept)):
		print("alt_dept cannot contain special characters")
		return
	if (SQLInjectionCheck(gen)):
		print("gen cannot contain special characters")
		return

	if 1 == professors.count({'Name': professor, 'Classes': {'Number' : number}}):
		print("class pair already exists");
		return 0
	
	res = professors.update_one(
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
	
	conn.zadd("classes", number, "0")
	conn.zadd(number, professor, "0")

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
			print("Professor already has the class")
			return 0
		new_vertex = client.command("create vertex prof_class set number = '" + number + "', name = '" + professor + "'")
		new_edge = client.command("create edge teaches from " + profs[0]._rid + " to " + new_vertex[0]._rid)
		new_edge2 = client.command("create edge class_of from " + new_vertex[0]._rid + " to " + classes[0]._rid)
	else:
		print("the class and/or the professor does not exist")
		return 0

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
	if (SQLInjectionCheck(professor)):
		print("Professor cannot contain special characters")
		return
	if (SQLInjectionCheck(number)):
		print("Number cannot contain special characters")
		return
		
	res = professors.update_one(
		{'Name': str(professor)},
		{'$pull': {
			'Classes': {
				'Number': str(number)
			}
		}}
	)
	
	client.command("delete vertex prof_class where name = '" + professor + "' and number = '" + number + "'")
	
	conn.zrem(number, professor)
	if not conn.zrangebyscore(number, 0, -1):
		conn.zrem("classes", number)
		conn.delete(number)
	return res


def add_student(username, password, year, major):
	if students.count({'Username': str(username)}) != 0:
		return 0
		
	if (SQLInjectionCheck(username)):
		print("usernames cannot contain special characters")
		return
	
	res = students.insert_one(
		{
				'Username': str(username),
				'Password': str(password),
				'Year': str(year),
				'Major': str(major)
		}
	)
	try:
		addStudent(username)
	except:
		print("Orient fail 230")
	return res
	
def addStudent(username):
	studs = client.command("select * from stud where username = '" + username + "'")
	if(len(studs) == 0):
		new_edge = client.command("create vertex stud set username = '" + username + "'")
	else:
		print("the user already exists")

# is never called, don't worry about it
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

	if (SQLInjectionCheck(username)):
		print("Number cannot contain special characters")
		return 
	#not sure if this delete is correct, but it is what I'm using
	client.command("delete vertex stud where username = '" + username + "'")
		
	res = students.delete_one({'Username': str(username)})
	return res