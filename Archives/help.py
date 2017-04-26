import pymongo;
from pymongo import MongoClient;
from time import gmtime, strftime;

client = MongoClient();

db = client['rose-profs'];

pointer = db.forums.find();

for data in pointer:
	print(data);

db.forums.remove({});

print('everything removed from forums');