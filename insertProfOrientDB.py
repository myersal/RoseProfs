#insert a new student into the database and check for errors
import pyorient
import pyorient.ogm

#create connection
client = pyorient.OrientDB("localhost", 2424);
session_id = client.connect( "root", "wai3feex" );

#open databse 
client.db_open("roseprofs", "admin", "admin" );

#find proffessor and student, then create edge

username = raw_input("insert a student to add to the database: ");

professors = client.command("select * from prof where name = '%s'" % username);

if(len(professors) != 0):
	new_edge = client.command("create vertex stud set name = %s" % username);
	print(client.command("select * from prof_rate"));
		
else:
	print("the user has already rated the professor");