from neo4j.v1 import GraphDatabase, basic_auth

try:
	import pyorient
	import pyorient.ogm
	client = pyorient.OrientDB("137.112.104.108", 2424)
	session_id = client.connect( "root", "wai3feex" )
	client.db_open( "library", "admin", "admin" )
except:
	print("Orient could not connect")
	exit()
	
session = None

def addBook(title, author, isbn, pages):
        
		books = client.command("select * from book where isbn = '" + str(isbn) + "'")
		
		for record in books:
				print('the book already exists')
				return 0
		
		books = client.command("CREATE Vertex book SET isbn = " + str(isbn))
		
		if(title != ""):
				client.command("UPDATE book SET title = '" + title + "'where isbn = " + str(isbn))
		
		if(pages != -1):
				client.command("UPDATE book SET pages = " + str(pages) + "where isbn = " + str(isbn))
			
		if(author != ''):
				#check to see if author exists, if not create the author
				result = client.command("select * from author where name = '" + author + "'")
				
				for data in result:
					auth = client.command("select * from author where name = '" + author + "'")
					client.command("CREATE Edge auth_of from " + auth[0]._rid + " to " + books[0]._rid)
					return 1
				auth = client.command("CREATE Vertex author SET name = '" + author + "'")
				
				client.command("CREATE Edge auth_of from " + auth[0]._rid + " to " + books[0]._rid)

def deleteBook(isbn):
		
		result = client.command("select * from book where isbn = " + str(isbn))
		
		for data in result:
				client.command("DELETE VERTEX book where isbn = " + str(isbn))
				print("book was deleted")
				return 1
		
		print("book does not exist")

def getBook(isbn):
		
		result = client.command("select * from book where isbn = " + str(isbn))
		for data in result:
				print(data)

def editBookAuthor(isbn):
		
		givenAnswer = raw_input('Do you want to add or remove an author (add/remove) : ')
		givenAuthor = raw_input('Input the author you want to add/remove: ')
		
		books = client.command("select * from book where isbn = " + str(isbn))
		
		for data in books:
			
			#check if an author exists
			
			if(givenAnswer == "add"):
				auth = client.command("select * from author where name = '" + givenAuthor + "'")
				#create author if auth does not exist
				for data in auth:
					client.command("CREATE Edge auth_of from " + auth[0]._rid + " to " + books[0]._rid)
					print('author added')
					return 1
				
				auth2 = client.command("Create Vertex author SET name = '" + givenAuthor + "'")
				client.command("CREATE Edge auth_of from " + auth2[0]._rid + " to " + books[0]._rid)
				print('author added')
				return 1
				
			elif(givenAnswer == 'remove'):
				auth = client.command("select * from author where name = '" + givenAuthor + "'")
				
				for data in auth:
					edges = client.command("SELECT * from auth_of where from = " + auth[0]._rid + "and to =" + books[0]._rid)
					for data in edges:
						client.command("DELETE Edge auth_of where from = " + auth[0]._rid + " and to = " + books[0]._rid)
						print("the edge has been deleted")
						return 1;
					print("the author is not currently an author of that book")
					
				print("author does not exist so cannot delete")
			else:
				print('answer not recognized')
				return 0;
			
			print('author was edited')
			return 1;
			
			
		print('book does not exist');
		
def editBookPages(isbn, newPages):
		books = client.command("select * from book where isbn = " + str(isbn));
		
		for data in books:
				client.command("UPDATE book SET pages = " + str(newPages) + "where isbn = " + str(isbn))
				print('the book has been edited')
				return 1
			
		print('the book does not exist')			
		

def editBookTitle(isbn, newTitle):
		books = client.command("select * from book where isbn = " + str(isbn))
		
		for data in books:
				client.command("UPDATE book SET title = '" + newTitle + "'where isbn = " + str(isbn))
				print('the book has been updated')
				return 1

		print('the book does not exist')
		
def sortByTitle():
		print('all books sorted by title')
		result = client.command("SELECT in() AS author, title, isbn, pages from book ORDER BY title")
		for data in result:
			print("isbn: " + str(data.isbn)),
			try:
				print(" title: " + data.title),
			except:
				#stupid errors
				print("")
			try:
				print(" pages: " + str(data.pages)),
			except:
				#stupid errors 2
				print("")
			for d in data.author:
				result2 = client.command("SELECT * from author where @rid = " + str(d))
				for data2 in result2:
					print(" author : " + result2[0].name),

def sortByAuthor():
		#####TODODODODODODODO

		print('all books sorted by author')
		result = client.command("SELECT out() AS books, name from author ORDER BY name")
		
		for data in result:
			print(" author : " + data.name),
			for d in data.books:
				result2 = client.command("SELECT * from book where @rid = " + str(d))
				for data2 in result2:
					print("isbn: " + str(data2.isbn)),
					try:
						print(" title: " + data2.title),
					except:
						#stupid errors
						print("")
					try:
						print(" pages: " + str(data2.pages)),
					except:
						#stupid errors 2
						print("")

def sortByISBN():
		print('all books sorted by isbn')
		result = client.command("SELECT in() AS author, title, isbn, pages from book ORDER BY isbn")
		
		for data in result:
			print("isbn: " + str(data.isbn)),
			try:
				print(" title: " + data.title),
			except:
				#stupid errors
				print("")
			try:
				print(" pages: " + str(data.pages)),
			except:
				#stupid errors 2
				print("")
			for d in data.author:
				result2 = client.command("SELECT * from author where @rid = " + str(d))
				for data2 in result2:
					print(" author : " + result2[0].name),
			

def sortByPages():
		print('all books sorted by number of pages')
		result = client.command("SELECT in() AS author, title, isbn, pages from book ORDER BY pages")
		
		for data in result:
			print("isbn: " + str(data.isbn)),
			try:
				print(" title: " + data.title),
			except:
				#stupid errors
				print("")
			try:
				print(" pages: " + str(data.pages)),
			except:
				#stupid errors 2
				print("")
			for d in data.author:
				result2 = client.command("SELECT * from author where @rid = " + str(d))
				for data2 in result2:
					print(" author : " + result2[0].name),

def addBorrower(name, username, phone):
		borrowers = client.command("select * from user where username = '" + username + "'")
		
		for data in borrowers:
				print('the username already exists')
				return 0;
				
		user = client.command("CREATE Vertex user Set username = '" + username + "'")
		
		if(name != ""):
				client.command("UPDATE user SET name = '" + name + "' where username = '" + username + "'")
		if(phone != ""):
				client.command("UPDATE user SET phone = '" + phone + "' where username = '" + username + "'")

def editBorrowerName(username, newName):
		borrowers = client.command("select * from user where username = '" + username + "'")
		
		for data in borrowers:
				client.command("UPDATE user SET name = '" + newName + "' where username = '" + username + "'")
				print('the borrower has been updated')
				return 1;
				
		print('the user does not exist')

def editBorrowerPhone(username, phone):
		borrowers = client.command("select * from user where username = '" + username + "'")
		
		for data in borrowers:
				client.command("UPDATE user SET phone = '" + phone + "' where username = '" + username + "'")
				print('the borrower has been updated')
				return 1;
				
		print('the user does not exist')
		
def deleteUser(username):
		borrowers = client.command("select * from user where username = '" + username + "'")
		
		for data in borrowers:
				client.command("DELETE VERTEX user where username = '" + username + "'")
				print('the borrower has been deleted')
				return 1;
				
		print('the user does not exist')

def checkoutBook(username, isbn):
		borrowers = client.command("select * from user where username = '" + username + "'")
		
		for data in borrowers:
				books = client.command("select * from book where isbn = " + str(isbn))
		
				for data2 in books:
						result3 = client.command("Select * from checked_out where out = " + books[0]._rid)
				
						for data3 in result3:
								print("The book is already checked out")
								return 0;
								
						client.command("CREATE EDGE checked_out from " + books[0]._rid + " to " + borrowers[0]._rid)
						print('book checked out by user')
						return 1;
						
				print('the book does not exist')
				return 0;
				
		print('the user does not exist')

def returnBook(username, isbn):
		borrowers = client.command("select * from user where username = '" + username + "'")
		
		for data in borrowers:
				books = client.command("select * from book where isbn = " + str(isbn))
		
				for data2 in books:
						result3 = client.command("Select * from checked_out where out = " + books[0]._rid)
				
						for data3 in result3:
								result4 = client.command("Select * from checked_out where in =" + borrowers[0]._rid + " and out = " + books[0]._rid)
								for data4 in result4:
										client.command("DELETE EDGE checked_out where in =" + borrowers[0]._rid + " and out = " + books[0]._rid)
										print("the book has been returned")
										return 1;
								print('the book is not checked out by that user')
								return 0;
								
						print("The book is not checked out")
						return 0;
				
				print('the book does not exist')
				return 0;
				
		print('the user does not exist')

def numberBooksChecked(username):
		borrowers = client.command("select * from user where username = '" + username + "'")
		
		for data in borrowers:
				result2 = client.command("select * from checked_out where in = " + borrowers[0]._rid) 
				count = 0
				for d in result2:
					count = count + 1
				print(str(count))
				return 1
				
		print('the user does not exist')	
	
def borrowerOfBook(isbn):
		books = client.command("select * from book where isbn = " + str(isbn))
		
		for data in books:
			edge = client.command("select * from checked_out where out = " + books[0]._rid)
			for d in edge:
				borrower = client.command("select * from (TRAVERSE both(checked_out) from (SELECT * from book where isbn = " + str(isbn) + ") WHILE $depth <= 2) WHERE @class = 'user'")
				#borrower = client.command("select * from user where in_checked_out = " + d._rid)
				for data2 in borrower:
					print(data2)
					return 1
					
				print(d)
				print(data)
				print('borrower not found')
				return 1
			print("no one currently has the book")
			return 1
				
		print("the book does not exist")

def getUsers():
		result = client.command("select * from user")
		for data in result:
				print(data)
				
def getAuthors():
		result = client.command("select * from author")
		for data in result:
				print(data)

def searchByTitle(title):
		result = client.command("select in() AS author, title, isbn, pages from book where title = '" + title + "'")
		for data in result:
			print("isbn: " + str(data.isbn)),
			try:
				print(" title: " + data.title),
			except:
				#stupid errors
				print("")
			try:
				print(" pages: " + str(data.pages)),
			except:
				#stupid errors 2
				print("")
			for d in data.author:
				result2 = client.command("SELECT * from author where @rid = " + str(d))
				for data2 in result2:
					print(" author : " + result2[0].name),
		
#TODODODODODOD
def searchByAuthor(author):
		#find all results with an author
		result = client.command("SELECT out() AS books, name from author WHERE name = '" + author + "' ORDER BY name")
		
		for data in result:
			print(" author : " + data.name),
			for d in data.books:
				result2 = client.command("SELECT * from book where @rid = " + str(d))
				for data2 in result2:
					print("isbn: " + str(data2.isbn)),
					try:
						print(" title: " + data2.title),
					except:
						#stupid errors
						print("")
					try:
						print(" pages: " + str(data2.pages)),
					except:
						#stupid errors 2
						print("")

def searchByIsbn(isbn):
		result = client.command("select in() AS author, title, isbn, pages from book where isbn = " + str(isbn))
		for data in result:
			print("isbn: " + str(data.isbn)),
			try:
				print(" title: " + data.title),
			except:
				#stupid errors
				print("")
			try:
				print(" pages: " + str(data.pages)),
			except:
				#stupid errors 2
				print("")
			for d in data.author:
				result2 = client.command("SELECT * from author where @rid = " + str(d))
				for data2 in result2:
					print(" author : " + result2[0].name),
				
def searchByUser(user):
		result = client.command("select * from user where username = '" + user + "'")
		for data in result:
			print(data);

def searchByName(name):
		result = client.command("select * from user where name = '" + name + "'")
		for data in result:
			print(data)

# not needed for neo4j I believe				
def removeAttribute(db, isbn, attribute):
		db.books.update({'isbn': isbn}, {'$unset': {attribute: ''}})
		print('attribute was removed')
		
def deleteAuthor(name):
		client.command("delete vertex author where name = '" + name + "'")
		
def rateBook(username, isbn, number, review):
		result = client.command("select * from user where username = '" + username + "'")
		
		for data in result:
				result2 = client.command("select * from book where isbn = " + str(isbn))
				for data2 in result2:
						result3 = client.command("select * from rate_book where out = " + result[0]._rid + " and in = " + result2[0]._rid)
						#if there is already a rating then update, else create the rating then update
						for data3 in result3:
								client.command("UPDATE rate_book SET review = '" + review + "', rate = " + str(number))
								print("the rating has been updated");
								return 1;
						client.command("CREATE EDGE rate_book from " + result[0]._rid + " to " + result2[0]._rid)
						client.command("UPDATE rate_book SET review = '" + review + "', rate = " + str(number))
						print('the rating has been created')
						return 1
				
				print('the book does not exist')
				return 0;
				
		print('user does not exist')
		return 0
		
def recommendation(username):
		#find users that have rated the same book the same
		
		result2 = client.command("Select * from (TRAVERSE out(rate_book), in(rate_book) from (SELECT * from user where username = '" + username + "') WHILE $depth <= 3) WHERE $depth = 3 and @class = 'book'")
		
		for data2 in result2:
			print(data2)
			print('recommendation complete')
		

while 1 > 0:
		givenInput = raw_input("$>:")

		if(givenInput == "help"):
				print("exit - to exit the prompt")
				print('editBook - to edit a book given an isbn')
				print('deleteBook - to delete a book given an isbn')
				print('addBook - to add a book')
				print('sort - to get a sorted list of books based on further input')
				print('checkout - to checkout a book')
				print('return - to return a book')
				print('addBorrower - to create a new user')
				print('deleteBorrower - to delete a user')
				print('editBorrower - to edit user information')
				print('checkBorrower - to find out what user has borrowed your book')
				print('checkBooksByUser - to check how many books a user currently has checked')
				print('searchBook - search for book stuff')
				print('searchUsers - search for user stuff')
				print('rateBook - rate a given book')
				print('recom - find recommendations for a user')

		elif(givenInput == 'getBook'):
				try:
					givenBook = input('input the isbn you want to get: ')
				except:
					print("given isbn is not an integer")
					
				getBook(givenBook)
					
		elif(givenInput == 'editBook'):
				try:
						givenISBN = input('select which isbn to edit: ')
				except:
						print("the given isbn must be an integer")
						continue
				
				givenString = raw_input('select one of the following to edit author, pages, title: ')

				if(givenString == 'author'):
						editBookAuthor(givenISBN)

				elif(givenString == 'pages'):
						try:
								givenPages = input('select a new number of pages: ')
						except:
								print("the pages must be an integer")
								continue
						editBookPages(givenISBN, givenPages)

				elif(givenString == 'title'):
						givenTitle = raw_input('select a new title:')
						editBookTitle(givenISBN, givenTitle)
				
				else:
						print('the given input was not recognized, editing stopped')

		elif(givenInput == 'deleteBook'):
				try:
						givenBook = input('give Book ISBN to delete: ')
					
				except:
						print("the given isbn must be an integer")
						continue
						
				deleteBook(givenBook)

		elif(givenInput == 'addBook'):
				givenTitle = raw_input("give Book Title: ")
				givenAuthor = raw_input("give Book Author: ")
				try:
						givenIsbn = input("give Book ISBN (must give): ")
				except:
						print("the given isbn must be an integer")
						continue;
				pagesBool = raw_input('do you want to provide pages (yes/no): ')
				if(pagesBool == 'no'):
						addBook(givenTitle, givenAuthor, givenIsbn, -1)
				else:
						try:
								givenPages = input("give Book Number Pages (must be an integer): ")
						except:
								print("the given input was not an integer")
								continue
						addBook(givenTitle, givenAuthor, givenIsbn, givenPages)
							
		elif(givenInput == 'sort'):
				givenSort = raw_input('sort by what? title, pages, author, or isbn: ')
				if(givenSort == 'title'):
						sortByTitle()
				elif(givenSort =='pages'):
						sortByPages()
				elif(givenSort == 'author'):
						sortByAuthor()
				elif(givenSort == 'isbn'):
						sortByISBN()

		elif(givenInput == 'addBorrower'):
				givenName = raw_input('please input your name: ')
				givenUserName = raw_input('please input a unique username: ')
				givenPhone = raw_input('please input a phone number: ')
				addBorrower(givenName, givenUserName, givenPhone)

		elif(givenInput == 'editBorrower'):
				givenUser = raw_input('please input the username to edit: ')
				givenEdit = raw_input('please select what you are editting, phone or name: ')
				if(givenEdit == 'phone'):
						givenPhone = raw_input('please input your new phone: ')
						editBorrowerPhone(givenUser, givenPhone)
				elif(givenEdit == 'name'):
						givenName = raw_input('please input your new name: ')
						editBorrowerName(givenUser, givenName)
				else:
						print('command not recognized')

		elif(givenInput == 'deleteBorrower'):
				givenUser = raw_input('please input the username to delete: ')
				deleteUser(givenUser)

		elif(givenInput == 'checkBorrower'):
				try:
						givenBook = input('please input the isbn of the book to check: ')
				except:
						print("the isbn must be an integer")
						continue
				borrowerOfBook(givenBook)
		
		elif(givenInput == 'checkBooksByUser'):
				givenuser = raw_input('please input the user to check: ')
				numberBooksChecked(givenuser)

		elif(givenInput == 'checkout'):
				try:
						givenBook = input('please input the book to checkout: ')
				except:
						print("the isbn must be an integer")
						continue
				
				givenUser = raw_input('please input the user to checkout: ')
				checkoutBook(givenUser, givenBook)

		elif(givenInput == 'return'):
				try:
						givenBook = input('please input the book to return: ')
				except:
						print("the isbn must be an integer")
						continue
				givenUser = raw_input('please input the borrower returning: ')
				returnBook(givenUser, givenBook)

		elif(givenInput == 'searchBook'):
				givenSearch = raw_input('please input your search method, isbn, title, author: ')
				if(givenSearch == 'isbn'):
						try:
								givenISBN = input('please input the isbn: ')
						except:
								print("the isbn must be an integer")
								continue
						searchByIsbn(givenISBN)
				elif(givenSearch == 'title'):
						givenTitle = raw_input('please input the title: ')
						searchByTitle(givenTitle)
				elif(givenSearch == 'author'):
						givenAuthor = raw_input('please input the author: ')
						searchByAuthor(givenAuthor)
				else:
						print('command not recognized')

		elif(givenInput == 'searchUsers'):
				givenSearch = raw_input('please input your search method, username or name: ')
				if(givenSearch == 'username'):
						givenUser = raw_input('please input the username: ')
						searchByUser(givenUser)
				elif(givenSearch == 'name'):
						givenName = raw_input('please input the name: ')
						searchByName(givenName)
				else:
						print('command not recognized')

		elif(givenInput == 'getUsers'):
				getUsers()
							
		elif(givenInput == 'rateBook'):
				try:
						givenBook = input('please select a book isbn to rate: ')
				except:
						print('the isbn must be an integer')
						continue
				givenUser = raw_input('please input a user for the rating: ')
				givenReview = raw_input('please input a review: ')
				try:
						givenRate = input('please input a rating between 1 and 5 (5 meaning great): ')
				except:
						print('the rating must be an integer')
						continue
						
				if(givenRate > 0 and givenRate < 6):
						rateBook(givenUser, givenBook, givenRate, givenReview)
						continue
				print('the number must be between 1 and 5')
				
		elif(givenInput == 'recom'):
				givenUser = raw_input('please give a user: ')
				recommendation(givenUser)

		elif(givenInput == 'getAuthors'):
				getAuthors()
				
		elif(givenInput == 'deleteAuthors'):
				givenName = raw_input('input an author to delete: ')
				deleteAuthor(givenName)

		elif(givenInput == "exit"):
				print('exiting now thank you!')
				break

		else:
				print('the given input is not a registered command')


