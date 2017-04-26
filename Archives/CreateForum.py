import pymongo;
from pymongo import MongoClient;
from time import gmtime, strftime;

client = MongoClient();

db = client['rose-profs'];

username = raw_input('what user is currently using this: ');

subject = raw_input('what is your subject: ');

boolProffessor = raw_input('do you want to list what professor yes/no (if neither is input no is assumed): ');

if(boolProffessor == 'yes'):
	prof = raw_input('please input the proffessor\'s name: ');
	
message = raw_input('please type your message for the forum: ');

#Now for the important part, the above may change when the application is actually in user

answer = raw_input('is the given information correct yes/no (no if yes is not input): ');

if(answer == 'yes'):
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
	
	if(boolProffessor == 'yes'):
		print(pointer);
		print('attempting');
		db.forums.update({'_id': pointer}, {'$set': {'proffessor': prof}});
	
	print('forum created');