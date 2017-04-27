#Give profs a rating


import RoseProfFunctions
from RoseProfFunctions import *
from pprint import pprint
import sys







print("Welcome to Rose Profs!!!!\n")
print("\n")
print("Please type your username to log in.\n  Or type new to make a new user")

while (True):
	username = raw_input(':')
	if username == "new":
		print("What would you like your username to be?")
		username = raw_input(':')
		if username == "" or username.find("\"") != -1 or username.find("\'") != -1:
			print ("Username cannot be empty or contain quotations")
		elif students.count({"Username": username}) != 0:
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
		curs = students.find_one({"Username": username})
		print("What is your password?")
		pwd =  raw_input(':')
		if (pwd == curs["Password"]):
			print("Welcome " + username)
			break
		else:
			print("Not a valid password. Please try again")

	else:
		print("Not a valid username. Please try again")

if databaseOpen:
	while (True):
		print("What would you like to do?")
		cmd = ""
		while cmd == "":
			cmd = raw_input(':')

		if cmd.lower() == "rate":
			print("What professor would you like to rate?")
			prof = raw_input(':')
			try:
				int(conn.zscore("professors", prof))
			except:
				print("That is not a prof")
				continue
			points = 8;
			print("You have 8 points to distribute among these four catagories: Communication\nGrading\nHelpfulness\nCoolness")
			print("On a scale from 0-4 with 4 being the most positive, \nhow do you rank this professors Communication?  \nYou have " + str(points) + " points left!")
			comm = raw_input(':')
			try:
				comm = int(comm)
			except:
				print("That is not a integer between 0 and 4")
				continue
			points = points - comm
			if (points < 0):
				print("You have distributed too many points!")
				continue
			if (comm > 4):
				print("The max rating is 4")
				continue
				
				
			print("On a scale from 0-4 with 4 being the most positive, \nhow do you rank this professors Grading?  \nYou have " + str(points) + " points left!")
			grade = raw_input(':')
			try:
				grade = int(grade)
			except:
				print("That is not a integer between 0 and 4")
				continue
			points = points - grade
			if (points < 0):
				print("You have distributed too many points!")
				continue
			if (grade > 4):
				print("The max rating is 4")
				continue
				
				
			print("On a scale from 0-4 with 4 being the most positive, \nhow do you rank this professors Helpfulness?  \nYou have " + str(points) + " points left!")
			helpp = raw_input(':')
			try:
				helpp = int(helpp)
			except:
				print("That is not a integer between 0 and 4")
				continue
			points = points - helpp
			if (points < 0):
				print("You have distributed too many points!")
				continue
			if (helpp > 4):
				print("The max rating is 4")
				continue
			
			cool = points
			print("That leaves " + str(points) + " points for the coolness rating!")
			
			
			students.update({"Username": username}, {"$addToSet": {"ProfRatings": {'Professor': prof,'Communication':comm, "Grading": grade, "Helpfulness" : helpp, "Coolness" : cool}}})
			
			try:
				rateProf(username, prof, comm, grade, helpp, cool)
			except:
				print("FAIL OF ORIENT to rate")
				continue

		
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
			if students.count({"Username": username}) == 0:
				edit_student_password(username, pwd)
				print("Username changed!")
			else:
				print("Username exists!")
				continue
			
		elif(cmd.lower() == "add prof" or cmd.lower() == "addprof" or cmd.lower() == "add professor" or cmd.lower() == "addprofessor"):
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
			
			if professors.count({"Name": newname}) == 0:
				edit_prof_name(name, newname)
				print("Professor name changed!")
			else:
				print("Professor name exists!")
				continue
				
		
			
		elif(cmd.lower() == "delete professor" or cmd.lower() == "deleteprofessor" or cmd.lower() == "delete prof" or cmd.lower() == "deleteprof"):
			print("Who is the Professor to be deleted?")
			name = raw_input(':')
			
			if professors.count({"Name": name}) > 0:
				del_prof(name)
				print("Professor deleted")
			else:
				print("Professor does not exist!")
				continue
	
		elif(cmd.lower() == "end" or cmd.lower() == "End" or cmd.lower() == "END" or cmd.lower() == "quit"):
				pizza = 8 / 0
	
		elif(cmd.lower() == "new class" or cmd.lower() == "new class"):
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
			if (gen.lower() == "yes" or gen.lower == "y"):
				gen = "True"
			if (gen.lower() == "no" or gen.lower == "n"):
				gen = "False"
			if (gen != "False" or gen != "True"):
				print("Invalid input. Make sure it is yes or no")
				continue
			add_class_to_prof(professor, name, num, dept, alt_dept, gen)

			
			
			
			
	
		#elif(cmd.lower() = "edit class name" or cmd.lower() = "edit classname" or cmd.lower() = "editclassname" or cmd.lower() = "editclass name"):
			#print("What is the professor of the class to be edited?")
			#professor = raw_input(':')
			#if profs.count({"Name": professor} == 0):
				#print("Professor does not exist")
				#continue
			#print("What is the number of the class to be edited?")
			#num = raw_input(':')
			#try:
				#int(conn.zrank("classes", num))
			#except:
				#print("Not a valid class number")
				#continue
				
			#print("What is the new name?")
			#new_name = raw_input(':')
			
			
			#edit_class_name(professor, num, new_name)


				


		elif(cmd.lower() == "delete class" or cmd.lower() == "deleteclass"):
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

				
		elif(cmd.lower() == "create forum" or cmd.lower() == "createforum"):
			createForum(username)
		elif(cmd.lower() == "log out" or cmd.lower() == "logout"):
			print("You just logged out!!!!! Bye!")	
			break
		else:
			print("invalid command")

		


	
	

