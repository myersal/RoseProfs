#insert a new professor into the database and check for errors
import pyorient
import pyorient.ogm

#create connection
client = pyorient.OrientDB("localhost", 2424);
session_id = client.connect( "root", "wai3feex" );

#open databse 
client.db_open("roseprofs", "admin", "admin" );

username = raw_input("insert a student to add to the database: ");

professors = client.command("select * from stud where username = '" + username + "'");



if(len(professors) == 0):
	new_edge = client.command("create vertex stud set username = '" + username + "'");
	print(client.command("select * from stud"));
		
else:
	print("the user already exists");