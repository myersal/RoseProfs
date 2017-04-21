#insert a new student into the database and check for errors
import pyorient
import pyorient.ogm

#create connection
client = pyorient.OrientDB("localhost", 2424);
session_id = client.connect( "root", "wai3feex" );

#open databse 
client.db_open("roseprofs", "admin", "admin" );

#find proffessor and student, then create edge

name = raw_input("insert a student to add to the database: ");

students = client.command("select * from stud where name = '" + name + "'");



if(len(professors) == 0):
	new_edge = client.command("create vertex prof set name = '" + name + "'");
	print(client.command("select * from prof"));
		
else:
	print("the user already exists");