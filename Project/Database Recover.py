def bringOrientUp():
	uporient = logs.find({'orient': {'$not': -1}})
	
	for record in uporient:
		if record['type'] == 'rateProf':
			ret = RateProf(record)
			#need to now update orient to be -1
			if ret == 1:
				#update here
			
def orientRateProf(record):
	professor = record['Name']
	student = record['Username']
	comm = record['Communication']
	grade = record['Grading']
	helpp = record['Helpfulness']
	cool = record['Coolness']
	
	profs = client.command("select * from prof where name = '" + professor + "'");
	studs = client.command("select * from stud where username = '" + username  + "'");	
	
	findUp = client.command("select * from prof_rate where out = " + studs[0]._rid + " and in = " + profs[0]._rid + " and cool = " + str(cool) + " and help = " + str(helpp) + "and comm = " + str(comm) + " and grad = " + str(grade))
	
	if(len(profs) != 0 and len(studs) != 0 and findUp < 1):
		currentEdges = client.command("select * from prof_rate where out = " + studs[0]._rid + " and in = " + profs[0]._rid);
		if(len(currentEdges) == 0):
			#insert edge
			new_edge = client.command("create edge prof_rate from " + studs[0]._rid + " to " + profs[0]._rid + " set cool = " + str(cool) + ", help = " + str(helpp) + ", comm = " + str(comm) + ", grad = " + str(grade));
			
			
	return 1;
		