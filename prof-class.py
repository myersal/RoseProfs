import pymongo
from pymongo import MongoClient


client = MongoClient()
db = client['rose-profs']


def add_prof(name, dept):
    cursor = db.professors.find({'Name': str(name)})
    if cursor:
        return 0
    res = db.professors.insert_one(
        {
            'Name': str(name),
            'Department': str(dept)
        }
    )
    return res


def edit_prof_name(name, new_name):
    res = db.professors.update_one(
        {'Name': str(name)},
        {'$set': {'Name': str(new_name)}}
    )
    return res


def edit_prof_dept(name, new_dept):
    res = db.professors.update_one(
        {'Name': str(name)},
        {'$set': {'Department': str(new_dept)}}
    )
    return res


def del_prof(name):
    res = db.professors.delete_one({'Name': str(name)})
    return res


def add_class_to_prof(professor, name, number, dept, alt_dept, gen):
    res = db.professors.update_one(
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
    return res


def edit_class_name(professor, number, new_name):
    res = db.professors.update_one(
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
    res = db.professors.update_one(
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
    res = db.professors.update_one(
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
    res = db.professors.update_one(
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
    res = db.professors.update_one(
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
    res = db.professors.update_one(
        {'Name': str(professor)},
        {'$pull': {
            'Classes': {
                'Number': str(number)
            }
        }}
    )
    return res


def add_student(username, password, year, major):
    cursor = db.students.find({'Username': str(username)})
    if cursor:
        return 0
    res = db.insert_one(
        {
            'Username': str(username),
            'Password': str(password),
            'Year': str(year),
            'Major': str(major)
        }
    )
    return res


def edit_student_username(username, new_username):
    res = db.students.update_one(
        {'Username': str(username)},
        {'$set': {'Username': str(new_username)}}
    )
    return res


def edit_student_password(username, new_password):
    res = db.students.update_one(
        {'Username': str(username)},
        {'$set': {'Password': str(new_password)}}
    )
    return res


def edit_student_year(username, new_year):
    res = db.students.update_one(
        {'Username': str(username)},
        {'$set': {'Year': str(new_year)}}
    )
    return res


def edit_student_major(username, new_major):
    res = db.students.update_one(
        {'Username': str(username)},
        {'$set': {'Major': str(new_major)}}
    )
    return res


def del_student(username):
    res = db.students.delete_one({'Username': str(username)})
    return res
