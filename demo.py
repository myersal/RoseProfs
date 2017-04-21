import pyorient
import pyorient.ogm

#create connection
client = pyorient.OrientDB("localhost", 2424);
session_id = client.connect( "root", "wai3feex" );

#open databse 
client.db_open( roseprofs, "root", "wai3feex" );

#create new proffessor and student, then edge

proffessor = client.command("select * from prof where name = " + "Goebel";
student = client.command("select * from stud where username = " + "suckup");

#insert edge

new_edge = client.command("create edge prof_rate from " + student + " to " + proffessor + " set cool = " + 1 + ", help = " + 2 + ", comm = " + 3 + "grad = " + 4);

print(client.command("select * from prof_rate"); 