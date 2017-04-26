'''
Created on Apr 26, 2017

@author: goebel
'''
import RoseProfConnections
from RoseProfConnections import *
from time import gmtime, strftime;


def rateProf(username, professor, comm, grade, helpp, cool):
        professors = client.command("select * from prof where name = '" + professor + "'");
        students = client.command("select * from stud where username = '" + username  + "'");

        if(len(professors) != 0 and len(students) != 0):
                currentEdges = client.command("select * from prof_rate where out = " + students[0]._rid + " and in = " + professors[0]._rid);

                if(len(currentEdges) == 0):
                        #insert edge
                        new_edge = client.command("create edge prof_rate from " + students[0]._rid + " to " + professors[0]._rid + " set cool = " + str(cool) + ", help = " + str(helpp) + ", comm = " + str(comm) + ", grad = " + str(grade));
        
                else:
                        print("the user has already rated the professor");

def add_prof(name, dept):
    if professors.count({'Name': str(name)}) != 0:
        return 0
    res = professors.insert_one(
        {
            'Name': str(name),
            'Department': str(dept)
        }
    )
    conn.zadd("professors", name, "0")
    try:
        addProf(name)
    except:
        print("Orient Failed to add prof")
    return res
    
def createForum(username):
    subject = raw_input('what is your subject: ');

    boolProffessor = raw_input('do you want to list what professor yes/no (if neither is input no is assumed): ');

    if(boolProffessor.lower() == 'yes'):
        prof = raw_input('please input the professor\'s name: ');
        
    message = raw_input('please type your message for the forum: ');

    #Now for the important part, the above may change when the application is actually in user

    answer = raw_input('is the given information correct yes/no (no if yes is not input): ');

    if(answer.lower() == 'yes'):
        time = strftime('%Y-%j-%d %H:%M:%S', gmtime());

        pointer = db.forums.insert(
            {
                'subject': subject,
                'message':
                    {
                        'username': username,
                        'content': message,
                        'date': time
                    }
            }
        );
        
        if(boolProffessor.lower() == 'yes'):
            print(pointer);
            print('attempting');
            db.forums.update({'_id': pointer}, {'$set': {'proffessor': prof}});
        
        print('forum created');

def addStudent(username):

        students = client.command("select * from stud where username = '" + username + "'");



        if(len(students) == 0):
                new_edge = client.command("create vertex stud set username = '" + username + "'");
        
        else:
                print("the user already exists");



def addProf(name):

        professors = client.command("select * from prof where name = '" + name + "'");



        if(len(professors) == 0):
                new_vertex = client.command("create vertex prof set name = '" + name + "'");
        
        else:
                print("the professor already exists");



def edit_prof_name(name, new_name):
    res = professors.update_one(
        {'Name': str(name)},
        {'$set': {'Name': str(new_name)}}
    )
    conn.zrem("professors", name)
    conn.zadd("professors", new_name, "0")
    classes = conn.zrangebyscore("classes", 0, -1)
    for c in classes:
        if conn.zrem(c, name):
            conn.zadd(c, new_name, "0")
    return res


def edit_prof_dept(name, new_dept):
    res = professors.update_one(
        {'Name': str(name)},
        {'$set': {'Department': str(new_dept)}}
    )
    return res


def del_prof(name):
    res = professors.delete_one({'Name': str(name)})
    conn.zrem("professors", name)
    classes = conn.zrangebyscore("classes", 0, -1)
    for c in classes:
        conn.zrem(c, name)
    return res


def add_class_to_prof(professor, name, number, dept, alt_dept, gen):
    res = professors.update_one(
        {'Name': str(professor)},
        {'$addToSet':{
            'Classes:'
            [
                'Name': str(name),
                'Number': str(number),
                'Department': str(dept),
                'Cross-list-Department': str(alt_dept),
                'Generic': str(gen)
            ]
        }}
    )
    conn.zadd("classes", number, "0")
    conn.zadd(number, professor, "0")
    return res


def edit_class_name(professor, number, new_name):
    res = professors.update_one(
        {
            'Name': str(professor),
            'Classes.Number': str(number)
        },
        {'$set': {
            'Classes.$.Name': str(new_name)
        }}
    )
    return res


def edit_class_number(professor, number, new_number):
    res = professors.update_one(
        {
            'Name': str(professor),
            'Classes.Number': str(number)
        },
        {'$set': {
            'Classes.$.Number': str(new_number)
        }}
    )
    return res


def edit_class_dept(professor, number, new_dept):
    res = professors.update_one(
        {
            'Name': str(professor),
            'Classes.Number': str(number)
        },
        {'$set': {
            'Classes.$.Department': str(new_dept)
        }}
    )
    return res


def edit_class_alt_dept(professor, number, new_alt_dept):
    res = professors.update_one(
        {
            'Name': str(professor),
            'Classes.Number': str(number)
        },
        {'$set': {
            'Classes.$.Cross-list-Department': str(new_alt_dept)
        }}
    )
    return res


def edit_class_gen(professor, number, new_gen):
    res = professors.update_one(
        {
            'Name': str(professor),
            'Classes.Number': str(number)
        },
        {'$set': {
            'Classes.$.Generic': str(new_gen)
        }}
    )
    return res


def del_class_from_prof(professor, number):
    res = professors.update_one(
        {'Name': str(professor)},
        {'$pull': {
            'Classes': {
                'Number': str(number)
            }
        }}
    )
    conn.zrem(number, professor)
    if not conn.zrangebyscore(number, 0, -1):
        conn.zrem("classes", number)
        conn.delete(number)
    return res


def add_student(username, password, year, major):
    if students.count({'Username': str(username)}) != 0:
        return 0
    res = students.insert_one(
        {
                'Username': str(username),
                'Password': str(password),
                'Year': str(year),
                'Major': str(major)
        }
    )
    try:
        addStudent(username)
    except:
        print("Orient fail 230")
    return res


def edit_student_username(username, new_username):
    res = students.update_one(
        {'Username': str(username)},
        {'$set': {'Username': str(new_username)}}
    )
    return res


def edit_student_password(username, new_password):
    res = students.update_one(
        {'Username': str(username)},
        {'$set': {'Password': str(new_password)}}
    )
    return res


def edit_student_year(username, new_year):
    res = students.update_one(
        {'Username': str(username)},
        {'$set': {'Year': str(new_year)}}
    )
    return res


def edit_student_major(username, new_major):
    res = students.update_one(
        {'Username': str(username)},
        {'$set': {'Major': str(new_major)}}
    )
    return res

def del_student(username):
    res = students.delete_one({'Username': str(username)})
    return res