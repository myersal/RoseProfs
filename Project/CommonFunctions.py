'''
Created on Apr 26, 2017

@author: goebel
'''

import string

def SQLInjectionCheck(word):
	invalidChars = set(string.punctuation.replace("_", "").replace("@", ""))
	if any(char in invalidChars for char in word):
		return False
	else:
		return True