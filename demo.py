import pyorient
import pyorient.ogm

#create connection
client = pyorient.OrientDB("localhost", 2424);
session_id = client.connect( "root", "wai3feex" );

#open databse 
client.db_open("roseprofs", "admin", "admin" );

#find proffessor and student, then create edge

proffessors = client.command("select * from prof where name = " + "'Goebel'");
students = client.command("select * from stud where username = " + "'suckup'");

print(students[0]);

#insert edge

new_edge = client.command("create edge prof_rate from " + students[0]._rid + " to " + proffessors[0]._rid + " set cool = " + "1" + ", help = " + "2" + ", comm = " + "3" + ", grad = " + "4");

print(client.command("select * from prof_rate")); 