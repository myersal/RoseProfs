import RoseProfFunctions
from RoseProfFunctions import *
from pprint import pprint
import sys
import re
import readline


COMMANDS = []
command = 0
RE_SPACE = re.compile('.*\s+$', re.M)

class Completer(object):
	def complete(self, text, state):
		"Generic readline completion entry point."
		#bufferr = readline.get_line_buffer()
		#line = readline.get_line_buffer().split()
		# show all commands
		#if not line:
		#	return [c + '' for c in COMMANDS][state]
		# account for last argument ending in a space
		#if RE_SPACE.match(bufferr):
		#	line.append('')
		# resolve command to the implementation function
		#cmd = line[0].strip()
		#if bufferr in COMMANDS:
			##impl = getattr(self, 'complete_%s' % cmd)
			##args = line[1:]
			##if args:
			##	return (impl(args) + [None])[state]
			#return [bufferr + '']#[state]
		

		#results = [c + '' for c in COMMANDS if c.startswith(bufferr)] + [None]
		#return results[state]
		bufferr = readline.get_line_buffer()
		line = readline.get_line_buffer().split()

		if not line or not bufferr:
			if command == 1:
				list = conn.zrange('professors', 0, -1)
				return list[state]
			if command == 2:
				list = conn.zrange('classes', 0, -1)
				return list[state]
			list = [bufferr] + [None]
			return list[state]

		if command == 0:
			list = [bufferr] + [None]
			return list[state]
		if command == 1:
			pos = conn.zrank('auto_professors', bufferr)
			list = conn.zrange('auto_professors', pos + 1, pos + 50)
			for entry in list:
				if entry[len(entry) - 1] == '*':
					result = [entry[:-1]] + [None]
					return result[state]
		if command == 2:
			pos = conn.zrank('auto_classes', bufferr)
			list = conn.zrange('auto_classes', pos + 1, pos + 50)
			for entry in list:
				if entry[len(entry) - 1] == '*':
					result = [entry[:-1]] + [None]
					return result[state]
		list = [bufferr] + [None]
		return list[state]


comp = Completer()
readline.set_completer_delims('\t\n;')
readline.parse_and_bind("tab: complete")
readline.set_completer(comp.complete)

print("Welcome to Rose Profs!!!!\n")
print("\n")
print("Please type your username to log in.\n  Or type new to make a new user")



while True:
	username = raw_input(':')
	if username == "new":
		print("What would you like your username to be?")
		username = raw_input(':')
		try:
			alreadyTaken = students.count({"Username": username})
		except:
			print("Rose Profs is currently unavailable")
			exit()
		if username == "" or username.find("\"") != -1 or username.find("\'") != -1:
			print ("Username cannot be empty or contain quotations")
		elif alreadyTaken != 0:
			print("Username is already taken")
		else:
			print("What would you like to be your password?")
			pwd = raw_input(':')
			print("What is your year?")
			year = raw_input(':')
			print("What is your primary major?")
			major = raw_input(':')
			
			points = 8;
			print(
				"You have 8 points to distribute among these four catagories"
				"for your ideal class: "
				"Amount of Work\nDifficulty\nFunness\nKnowledge of Prof"
			)
			print(
				"On a scale from 0-4 with 4 being the most positive, \n"
				"how do you rank your ideal class's amount of work?  \n"
				"You have " + str(points) + " points left!"
			)
			work = raw_input(':')
			try:
				work = int(work)
			except:
				print("That is not a integer between 0 and 4")
				continue
			points = points - work
			if points < 0:
				print("You have distributed too many points!")
				continue
			if work > 4 or work < 0:
				print("The max rating is 4.  The min rating is 0")
				continue
			print(
				"On a scale from 0-4 with 4 being the most positive, \n"
				"how do you rank your ideal classes technical difficulty?  \n"
				"You have " + str(points) + " points left!"
			)
			diff = raw_input(':')
			try:
				diff = int(diff)
			except:
				print("That is not a integer between 0 and 4")
				continue
			points = points - diff
			if points < 0:
				print("You have distributed too many points!")
				continue
			if diff > 4 or diff < 0:
				print("The max rating is 4.  The min rating is 0")
				continue
			print(
				"On a scale from 0-4 with 4 being the most positive, \n"
				"how do you rank how much fun your ideal class would be?  \n"
				"You have " + str(points) + " points left!"
			)
			fun = raw_input(':')
			try:
				fun = int(fun)
			except:
				print("That is not a integer between 0 and 4")
				continue
			points = points - fun
			if points < 0:
				print("You have distributed too many points!")
				continue
			if fun > 4 or fun < 0:
				print("The max rating is 4.  The min rating is 0")
				continue
			know = points
			print("That leaves " + str(points) + " points for the knowledge of prof rating!")		
			try:
				add_student(username, pwd, year, major, work, diff, fun, know)
			except:
				print("Rose Profs is currently unavailable")
				exit()
			print("User added")
			break		

	else: 
		try:
			curs = students.find_one({"Username": username})
		except:
			print("Rose Profs is currently unavailable")
			exit()
		if curs != None:
			print("What is your password?")
			pwd = raw_input(':')
			if pwd == curs["Password"]:
				print("Welcome " + username)
				break
			else:
				print("Not a valid password. Please try again")

		else:
			print("Not a valid username. Please try again")
#try:
if databaseOpen:
	while True:
		if logs.count({'redis': 0}) == 0:
			redisDead = False
			print("Quick Search Online")
		if logs.count({'orient': 0}) == 0:
			orientDead = False
			print("Recommendations Online")
		print("What would you like to do?")
		cmd = ""
		while cmd == "":
			cmd = raw_input(':')

		if cmd.lower() == "rate prof":
			print("What professor would you like to rate?")
			command = 1
			prof = raw_input(':')
			command = 0
			boolP = checkIfProfessorExists(prof)
			if(not boolP):
				print('The professor does not exist')
				continue
			points = 8;
			print(
				"You have 8 points to distribute among these four categories: "
				"Communication\nGrading\nHelpfulness\nCoolness"
			)
			print(
				"On a scale from 0-4 with 4 being the most positive, \n"
				"how do you rank this professors Communication?  \n"
				"You have " + str(points) + " points left!"
			)
			comm = raw_input(':')
			try:
				comm = int(comm)
			except:
				print("That is not a integer between 0 and 4")
				continue
			points = points - comm
			if points < 0:
				print("You have distributed too many points!")
				continue
			if comm > 4 or comm < 0:
				print("The max rating is 4.  The min rating is 0")
				continue
			print(
				"On a scale from 0-4 with 4 being the most positive, \n"
				"how do you rank this professors Grading?  \n"
				"You have " + str(points) + " points left!"
			)
			grade = raw_input(':')
			try:
				grade = int(grade)
			except:
				print("That is not a integer between 0 and 4")
				continue
			points = points - grade
			if points < 0:
				print("You have distributed too many points!")
				continue
			if grade > 4 or grade < 0:
				print("The max rating is 4. The min rating is 0")
				continue
			print(
				"On a scale from 0-4 with 4 being the most positive, \n"
				"how do you rank this professors Helpfulness?  \n"
				"You have " + str(points) + " points left!"
			)
			helpp = raw_input(':')
			try:
				helpp = int(helpp)
			except:
				print("That is not a integer between 0 and 4")
				continue
			points = points - helpp
			if points < 0:
				print("You have distributed too many points!")
				continue
			if helpp > 4 or helpp < 0:
				print("The max rating is 4.  The min rating is 0")
				continue
			cool = points
			print("That leaves " + str(points) + " points for the coolness rating!")
			rateProf(username, prof, comm, grade, helpp, cool)

		elif cmd.lower() == "rate class":
			print("What professor teaches this class?")
			command = 1
			prof = raw_input(':')
			command = 0
			boolP = checkIfProfessorExists(prof)
			if(not boolP):
				print('The professor does not exist')
				continue
			print("What is the class number?")
			command = 2
			classToRate = raw_input(':')
			command = 0
			try:
				numOfClasses = professors.count({"Name":prof, "Classes.Number": classToRate})
			except:
				print("That is not a class taught by that professor")
				continue
			points = 8;
			print(
				"You have 8 points to distribute among these four catagories: "
				"Amount of Work\nDifficulty\nFunness\nKnowledge of Prof"
			)
			print(
				"On a scale from 0-4 with 4 being the most positive, \n"
				"how do you rank this class's amount of work?  \n"
				"You have " + str(points) + " points left!"
			)
			work = raw_input(':')
			try:
				work = int(work)
			except:
				print("That is not a integer between 0 and 4")
				continue
			points = points - work
			if points < 0:
				print("You have distributed too many points!")
				continue
			if work > 4 or work < 0:
				print("The max rating is 4.  The min rating is 0")
				continue
			print(
				"On a scale from 0-4 with 4 being the most positive, \n"
				"how do you rank this classes technical difficulty?  \n"
				"You have " + str(points) + " points left!"
			)
			diff = raw_input(':')
			try:
				diff = int(diff)
			except:
				print("That is not a integer between 0 and 4")
				continue
			points = points - diff
			if points < 0:
				print("You have distributed too many points!")
				continue
			if diff > 4 or diff < 0:
				print("The max rating is 4.  The min rating is 0")
				continue
			print(
				"On a scale from 0-4 with 4 being the most positive, \n"
				"how do you rank how much fun this class is?  \n"
				"You have " + str(points) + " points left!"
			)
			fun = raw_input(':')
			try:
				fun = int(fun)
			except:
				print("That is not a integer between 0 and 4")
				continue
			points = points - fun
			if points < 0:
				print("You have distributed too many points!")
				continue
			if fun > 4 or fun < 0:
				print("The max rating is 4 and the min rating is 0")
				continue
			know = points
			print("That leaves " + str(points) + " points for the knowledge of prof rating!")
			rateClass(username, prof, classToRate, work, diff, fun, know)

		elif cmd.lower() == "edit major" or cmd.lower() == "editmajor":
			print("What is your new major?")
			maj = raw_input(':')
			edit_student_major(username, maj)
			print("Major changed!")
	
		elif cmd.lower() == "edit year" or cmd.lower() == "edityear":
			print("What is your new year?")
			year = raw_input(':')
			edit_student_year(username, year)
			print("Year changed!")
		
		elif cmd.lower() == "edit password" or cmd.lower() == "editpassword":
			print("What is your new password?")
			pwd = raw_input(':')
			edit_student_password(username, pwd)
			print("Password changed!")

		elif cmd.lower() == "add prof" or cmd.lower() == "addprof" or cmd.lower() == "add professor" or cmd.lower() == "addprofessor":
			print("Who is the new Professor?")
			name = raw_input(':')
			boolP = checkIfProfessorExists(name)
			if(boolP):
				print('The professor already exists')
				continue
				
			if name.find("\'") != -1 or name.find("\"") != -1:
				print("Name can't contain quotations!  You trying to sql inject me buddy????")
				continue
			print("What is his/her department")
			dept = raw_input(':')
			add_prof(name, dept)
			print("Prof added!")

		elif cmd.lower() == "edit department" or cmd.lower() == "editdepartment":
			print("Who is the Professor?")
			command = 1
			name = raw_input(':')
			command = 0
			print("What is his/her new department")
			dept = raw_input(':')
			edit_prof_dept(name, dept)
			print("Department changed!")

		elif cmd.lower() == "delete professor" or cmd.lower() == "deleteprofessor" or cmd.lower() == "delete prof" or cmd.lower() == "deleteprof":
			print("Who is the Professor to be deleted?")
			command = 1
			name = raw_input(':')
			command = 0
			boolP = checkIfProfessorExists(name)
			if not boolP:
				print('The professor does not exist')
				continue
			del_prof(name)
			print("Professor deleted")

		elif cmd.lower() == "help":
			print("rate prof - allows you to rate a professor")
			print("rate class - allows you to rate a class")
			print("edit major - allows you to edit your major")
			print("edit year - allows you to edit your year")
			print("edit password - allows you to edit your password")
			print("add prof - allows you to add a professor")
			print("edit department - allows you to change a professor's department")
			print("delete professor - allows you to delete a professor")
			print("new class - allows you to create a new class")
			print("delete class - allows you to delete a class")
			print("create forum - allows you to create a forum")
			print("delete profile - allows you to permanently delete your profile")
			print("check - forces the program to check if the other systems are up")
			print("recommend prof - recommends a professor for a given class")
			print("search prof - search for a professor in the databases")
			print("search class - search for a class in the database")
			print("end/logout - quits the program")
			
		elif cmd.lower() == "search professor" or cmd.lower() == "searchprofessor" or cmd.lower() == "search prof" or cmd.lower() == "searhprof":
			if redisDead:
				print("This is down sorry bro!!")
				continue
			print("Who is the Professor you want to search for?  Hit TAB to see sorted list of professors")
			command = 1
			name = raw_input(':')
			command = 0
			boolP = checkIfProfessorExists(name)
			if not boolP:
				print('The professor does not exist')
				continue
			print(search_professors(name))

		elif cmd.lower() == "search class" or cmd.lower() == "searchclass" or cmd.lower() == "search class" or cmd.lower() == "searhclass":
			if redisDead:
				print("This is down sorry bro!!")
				continue
			print("Who is the Professor that teaches this class?  Hit TAB to see sorted list of professors")
			command = 1
			name = raw_input(':')
			command = 0
			boolP = checkIfProfessorExists(name)
			if not boolP:
				print('The professor does not exist')
				continue
			print("What class do you want to search?")
			command = 2
			classNum = raw_input(':')
			command = 0
			try:
				numOfClasses = professors.count({"Name":name, "Classes.Number": classNum})
			except:
				print("That is not a class taught by that professor")
				continue
			
			print(search_class_prof(name, classNum))

		elif cmd.lower() == "edit class name" or cmd.lower() == "editclassname":
			if not redisDead:
				print("Who is the Professor that teaches this class?  Hit TAB to see sorted list of professors")
			else:
				print("Who is the Professor that teaches this class?")
			command = 1
			name = raw_input(':')
			command = 0
			boolP = checkIfProfessorExists(name)
			if not boolP:
				print('The professor does not exist')
				continue
			print("What class do you want to edit?")
			command = 2
			classNum = raw_input(':')
			command = 0
			try:
				numOfClasses = professors.count({"Name":name, "Classes.Number": classNum})
			except:
				print("That is not a class taught by that professor")
				continue
			print(search_class_prof(name, classNum))
			print("What should the new name be?")
			newName = raw_input(':')
			edit_class_name(name, classNum, newName)
			
		elif cmd.lower().replace(' ', '') == "editclassdept" or cmd.lower().replace(' ', '') == "editclassdepartment":
			if not redisDead:
				print("Who is the Professor that teaches this class?  Hit TAB to see sorted list of professors")
			else:
				print("Who is the Professor that teaches this class?")
			command = 1
			name = raw_input(':')
			command = 0
			boolP = checkIfProfessorExists(name)
			if not boolP:
				print('The professor does not exist')
				continue
			print("What class do you want to edit?")
			command = 2
			classNum = raw_input(':')
			command = 0
			try:
				numOfClasses = professors.count({"Name":name, "Classes.Number": classNum})
			except:
				print("That is not a class taught by that professor")
				continue
			print(search_class_prof(name, classNum))
			print("What should the new department be?")
			newDept = raw_input(':')
			edit_class_dept(name, classNum, newDept)

		elif cmd.lower().replace(' ', '') == "editclassaltdept" or cmd.lower().replace(' ', '') == "editclassalternatedepartment":
			if not redisDead:
				print("Who is the Professor that teaches this class?  Hit TAB to see sorted list of professors")
			else:
				print("Who is the Professor that teaches this class?")
			command = 1
			name = raw_input(':')
			command = 0
			boolP = checkIfProfessorExists(name)
			if not boolP:
				print('The professor does not exist')
				continue
			print("What class do you want to edit?")
			command = 2
			classNum = raw_input(':')
			command = 1
			try:
				numOfClasses = professors.count({"Name":name, "Classes.Number": classNum})
			except:
				print("That is not a class taught by that professor")
				continue
			print(search_class_prof(name, classNum))
			print("What should the new alternate department be?")
			newAltDept = raw_input(':')
			edit_class_alt_dept(name, classNum, newAltDept)
			
		elif cmd.lower().replace(' ', '') == "editclassgen" or cmd.lower().replace(' ', '') == "editclassgeneral":
			if not redisDead:
				print("Who is the Professor that teaches this class?  Hit TAB to see sorted list of professors")
			else:
				print("Who is the Professor that teaches this class?")
			command = 1
			name = raw_input(':')
			command = 0
			boolP = checkIfProfessorExists(name)
			if not boolP:
				print('The professor does not exist')
				continue
			print("What class do you want to edit?")
			command = 2
			classNum = raw_input(':')
			command = 0
			try:
				numOfClasses = professors.count({"Name":name, "Classes.Number": classNum})
			except:
				print("That is not a class taught by that professor")
				continue
			print(search_class_prof(name, classNum))
			print("Is this a general class? \"yes\" or \"no\"")
			gen = raw_input(':')
			if gen.lower() == "yes" or gen.lower == "y":
				gen = "True"
			if gen.lower() == "no" or gen.lower == "n":
				gen = "False"
			if gen != "False" and gen != "True":
				print("Invalid input. Make sure it is yes or no")
				continue
			edit_class_gen(name, classNum, gen)

		elif cmd.lower() == "get professors" or cmd.lower() == "getprofesors" or cmd.lower() == "get profs" or cmd.lower() == "getprofs":
			if redisDead:
				print("This is down sorry bro!!")
				continue
			print("For what class do you want profesors for?  Hit TAB to see sorted list of classes")
			command = 2
			classNum = raw_input(':')
			command = 0
			print conn.zrange(classNum, 0, -1)

		elif cmd.lower() == "end" or cmd.lower() == "End" or cmd.lower() == "END" or cmd.lower() == "quit":
				break

		elif cmd.lower() == "new class" or cmd.lower() == "new class":
			print("Who is the Professor who teaches the class?")
			command = 1
			professor = raw_input(':')
			command = 0
			boolP = checkIfProfessorExists(professor)
			if not boolP:
				print('The professor does not exist')
				continue
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
			if gen.lower() == "yes" or gen.lower == "y":
				gen = "True"
			if gen.lower() == "no" or gen.lower == "n":
				gen = "False"
			if gen != "False" and gen != "True":
				print("Invalid input. Make sure it is yes or no")
				continue
			add_class_to_prof(professor, name, num, dept, alt_dept, gen)

		elif cmd.lower() == "delete class" or cmd.lower() == "deleteclass":
			print("Who is the Professor who teaches the class?")
			command = 1
			professor = raw_input(':')
			command = 0
			boolP = checkIfProfessorExists(professor)
			if not boolP:
				print('The professor does not exist')
				continue
			print("What is the number of the class?")
			command = 2
			num = raw_input(':')
			command = 0
			try:
				int(conn.zrank("classes", num))
			except:
				print("Not a valid class number")
				continue
			del_class_from_prof(professor, num)

		elif cmd.lower() == "create forum" or cmd.lower() == "createforum":
			prof = ""
			subject = raw_input('what is your subject: ')
			boolProfessor = raw_input('do you want to list what professor yes/no (if neither is input no is assumed): ')
			if boolProfessor.lower() == 'yes':
				command = 1
				prof = raw_input('please input the professor\'s name: ')
				command = 0
				numOfProfs = -1
				boolP = checkIfProfessorExists(name)
				if not boolP:
					print('The professor does not exist')
					continue
			message = raw_input('please type your message for the forum: ')
			#Now for the important part, the above may change when the application is actually in user
			answer = raw_input('is the given information correct yes/no (no if yes is not input): ')
			if answer.lower() == 'yes':
				time = strftime('%Y-%j-%d %H:%M:%S', gmtime())
				createForum(username, subject, boolProfessor, prof, message, time)

		elif cmd.lower() == "log out" or cmd.lower() == "logout":
			print("You just logged out!!!!! Bye!")	
			break

		elif cmd.lower() == "delete profile" or cmd.lower() == "deleteprofile":
			print("Are you sure you want to PERMANENTLY delete your profile? Type yes if you do.")
			ans = raw_input(":")
			if ans.lower() == "yes":
				del_student(username)
				break

		elif cmd.lower() == "check" or cmd.lower() == "check!":
			continue
		
		elif cmd.lower() == "see classes" or cmd.lower() == "seeclasses":
			if redisDead:
				print("Sorry that service is unavailable")
				continue
			print conn.zrange("classes", 0, -1)
			
		elif cmd.lower() == "recommend prof":
			if orientDead:
				print("recommendations are currently offline, please wait until the service is back up")
				continue
			print("Please input the class you want to get a recommended professor for")
			command = 2
			given_class = raw_input(":")	
			command = 0
			currentStud = students.find_one({"Username": username})
			#DEBUG PRINT
			print("got student")
			recomProfForClass(given_class, currentStud['DesWork'], currentStud['DesDiff'], currentStud['DesFun'], currentStud['DesKnow'])

		else:
			print("invalid command")

print("Exiting Rose Profs...")
#except:
#	print("The Database is currently not working, try again later please, ERROR_666")