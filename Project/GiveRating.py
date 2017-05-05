import RoseProfFunctions
from RoseProfFunctions import *
from pprint import pprint
import sys
import re


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
			try:
				add_student(username, pwd, year, major)
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
			prof = raw_input(':')
			try:
				if not redisDead:
					try:
						numOfProfs = conn.zscore("professors", prof)
					except:
						print("Some functionality may be slower and/or limited due to problems outside of your control")
						redisDead = True
				if redisDead:
					try:
						numOfProfs = professors.count({"Name": prof})
						if numOfProfs == 0:
							print("That is not a prof")
							continue
					except:
						print("Sorry, but Rose Profs is currently down.  Please try again later")
						exit()
				int(numOfProfs)
			except:
				print("That is not a prof")
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
			if comm > 4:
				print("The max rating is 4")
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
			if grade > 4:
				print("The max rating is 4")
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
			if helpp > 4:
				print("The max rating is 4")
				continue
			cool = points
			print("That leaves " + str(points) + " points for the coolness rating!")
			rateProf(username, prof, comm, grade, helpp, cool)

		elif cmd.lower() == "rate class":
			print("What professor teaches this class?")
			prof = raw_input(':')
			try:
				int(conn.zscore("professors", prof))
			except:
				print("That is not a prof")
				continue
			print("What is the class number?")
			classToRate = raw_input(':')
			try:
				int(conn.zscore("classes", classToRate))
			except:
				print("That is not a class")
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
			if work > 4:
				print("The max rating is 4")
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
			if diff > 4:
				print("The max rating is 4")
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
			if fun > 4:
				print("The max rating is 4")
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
	
		elif cmd.lower() == "edit username" or cmd.lower() == "editusername":
			print("What is your new username?")
			pwd = raw_input(':')
			if students.count({"Username": username}) == 0:
				edit_student_password(username, pwd)
				print("Username changed!")
			else:
				print("Username exists!")
				continue
			
		elif cmd.lower() == "add prof" or cmd.lower() == "addprof" or cmd.lower() == "add professor" or cmd.lower() == "addprofessor":
			print("Who is the new Professor?")
			name = raw_input(':')
			if professors.count({"Name": name}) != 0: 
				print("Professor exists already")
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
			name = raw_input(':')
			print("What is his/her new department")
			dept = raw_input(':')
			edit_prof_dept(name, dept)
			print("Department changed!")

		elif cmd.lower() == "edit professor name" or cmd.lower() == "editprofessorname" or cmd.lower() == "edit prof name" or cmd.lower() == "editprofname":
			print("Who is the Professor?")
			name = raw_input(':')
			print("What is his/her new name?")
			newname = raw_input(':')
			
			if professors.count({"Name": newname}) == 0:
				edit_prof_name(name, newname)
				print("Professor name changed!")
			else:
				print("Professor name exists!")
				continue

		elif cmd.lower() == "delete professor" or cmd.lower() == "deleteprofessor" or cmd.lower() == "delete prof" or cmd.lower() == "deleteprof":
			print("Who is the Professor to be deleted?")
			name = raw_input(':')
			if professors.count({"Name": name}) > 0:
				del_prof(name)
				print("Professor deleted")
			else:
				print("Professor does not exist!")
				continue
		elif cmd.lower() == "end" or cmd.lower() == "End" or cmd.lower() == "END" or cmd.lower() == "quit":
				break

		elif cmd.lower() == "new class" or cmd.lower() == "new class":
			print("Who is the Professor who teaches the class?")
			professor = raw_input(':')
			if professors.count({"Name": professor}) == 0:
				print("Professor does not exist")
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
			professor = raw_input(':')
			if professors.count({"Name": professor}) == 0:
				print("Professor does not exist")
				continue
			print("What is the number of the class?")
			num = raw_input(':')
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
				createForum(username, boolProfessor, prof, message, time)







		elif cmd.lower() == "log out" or cmd.lower() == "logout":
			print("You just logged out!!!!! Bye!")	
			break

		elif cmd.lower() == "delete profile" or cmd.lower() == "deleteprofile":
			print("Are you sure you want to PERMANENTLY delete your profile? Type yes if you do.")
			ans = raw_input(":")
			if ans.lower() == "yes":
				del_student(username)
				break

		else:
			print("invalid command")

print("Exiting Rose Profs...")