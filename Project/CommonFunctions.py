'''
Created on Apr 26, 2017

@author: goebel
'''

import string

def SQLInjectionCheck(word):
	if (isinstance(word, int)):
		return False
	invalidChars = set(string.punctuation.replace("_", "").replace("@", ""))
	if any(char in invalidChars for char in word):
		return True
	else:
		return False