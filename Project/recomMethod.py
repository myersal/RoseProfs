def recomProfForClass(given_class, desWork, desDiff, desFun, desKnow):
	#assumes the method is given a class, and the desired rating for the individual student
	
	#gives the potential prof_class pairs of the class

	initialClassConns = client.command("SELECT * from (TRAVERSE both(class_of) from (Select * from class WHERE class = '" + given_class + "') WHILE $ depth <= 2) WHERE @class = 'prof_class'")

	highestRate = None
	lowestDif = 50 #not possible to have this large of difference so can use it as a max

	#must traverse the prof_class pairs and find all the class ratings from users

	for pairs in initialClassConns:
		ratings = client.command("SELECT * from (TRAVERSE both(class_rate) from (Select * from prof_class WHERE class = " + pairs._rid + ") WHILE $depth <= 2) WHERE @class = 'class_rate'")
		# Must traverse the ratings for each class and find the highest match to the users desired rating
		for rates in ratings:
			difference = math.abs(desWork - rates.work) + math.abs(desDiff - rates.diff) + math.abs(desFun - rates.fun) + math.abs(desKnow - rates.know)
			if difference < lowestDif: #checks to see if the difference is lower than the current match
				lowestDif = difference #sets the lowestDif
				highestRate = pairs #assigns highest rating to the prof_class pair
	
	if highestRate is None:
		print('the class does not exist or does not currently have any ratings')
		return
	
	#prints out the name of the prof that this recom recommends for the given inputs
	print("The recommended prof for the given class is: " + highestRate.name)
		