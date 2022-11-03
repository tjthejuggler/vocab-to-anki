import os
from os import path
from pathlib import Path
import sys, getopt
from random import randint
import argparse
import math

home = str(Path.home())
cwd = os.getcwd()

#todo
#make a min and max for either digit (so we can make a bunch of X*11 questions)
#make an audio deck in english for X*11 questions

def get_args():
	language, operation = '',''
	problem_count, minnumber1, maxnumber1, minnumber2, maxnumber2 = 10, 0, 100, 0, 100
	parser = argparse.ArgumentParser()
	parser.add_argument("language", help="language code (en = english)")
	parser.add_argument("operation", help="operation type: Add, Subtract, Multiply, Divide")
	parser.add_argument("-p", "--problems", type = int, help="the nuumber of problems")
	parser.add_argument("-n1", "--minnumber1", type = int, help="minimum number to use for first num")
	parser.add_argument("-x1", "--maxnumber1", type = int, help="maximum number to use for first num")
	parser.add_argument("-n2", "--minnumber2", type = int, help="minimum number to use for second num")
	parser.add_argument("-x2", "--maxnumber2", type = int, help="maximum number to use for second num")	
	args = parser.parse_args()
	language = args.language
	operation = args.operation
	if args.problems:
		problem_count = args.problems
	if args.minnumber1:
		minnumber1 = args.minnumber1
		minnumber2 = args.minnumber1
	if args.maxnumber1:
		maxnumber1 = args.maxnumber1
		maxnumber2 = args.maxnumber1	
	if args.minnumber2:
		minnumber2 = args.minnumber2
	if args.maxnumber2:
		maxnumber2 = args.maxnumber2	
	return (language, operation, problem_count, minnumber1, maxnumber1, minnumber2, maxnumber2)

def get_rounded_up_number(num_to_round):
	number_of_digits = len(str(num_to_round))
	round_to_nearest_5 = False
	if number_of_digits>1:
		second_digit = num_to_round // 10**2 % 10
		if second_digit < 5:
			round_to_nearest_5 = True
	round_unit = 10**(number_of_digits-1)
	print(num_to_round, round_unit)
	if round_to_nearest_5:
		round_unit = int(round_unit / 2)
	return int(math.ceil(num_to_round / round_unit)) * round_unit

def main():
	(language, operation, problem_count, minnumber1, maxnumber1, minnumber2, maxnumber2) = get_args()
	print(language, operation, problem_count, minnumber1, maxnumber1, minnumber2, maxnumber2)
	questions = []
	for problem in range(problem_count):
		first_num = randint(minnumber1, maxnumber1)
		second_num = randint(minnumber2, maxnumber2)
		answer = 0
		operation_word = ''
		if operation == 'a':
			answer = first_num + second_num
		elif operation == 's':
			if second_num > first_num:
				temp = first_num
				first_num = second_num
				second_num = temp
			answer = first_num - second_num
		elif operation == 'm':
			answer = first_num * second_num
		elif operation == 'd':
			product = first_num * second_num
			answer = first_num
			first_num = product
		elif operation == 'r':
			print(first_num, second_num)
			first_num = get_rounded_up_number(second_num)
			answer = first_num - second_num
		if language == 'en':
			if operation == 'a':
				operation_word = 'plus'
			elif operation == 's' or operation == 'r':
				operation_word = 'minus'
			elif operation == 'm':
				operation_word = 'times'
			elif operation == 'd':
				operation_word = 'divided by'
			question = 'what is '+str(first_num)+' '+operation_word+' '+str(second_num)+' - '+str(answer)
		elif language == 'tr':
			if operation == 'a':
				operation_word = 'artı'
			elif operation == 's' or operation == 'r':
				operation_word = 'eksi'
			elif operation == 'm':
				operation_word = 'kere'
			elif operation == 'd':
				operation_word = 'bölü'
			question = str(first_num)+' '+operation_word+' '+str(second_num)+' nedir - '+str(answer)
			question = question.replace(' 10', ' on')
		elif language == 'es':
			if operation == 'a':
				operation_word = 'más'
			elif operation == 's' or operation == 'r':
				operation_word = 'menos'
			elif operation == 'm':
				operation_word = 'por'
			elif operation == 'd':
				operation_word = 'dividido por'
			question = 'cuanto es ' + str(first_num)+' '+operation_word+' '+str(second_num)+' - '+str(answer)
		elif language == 'de':
			if operation == 'a':
				operation_word = 'plus'
			elif operation == 's' or operation == 'r':
				operation_word = 'minus'
			elif operation == 'm':
				operation_word = 'mal'
			elif operation == 'd':
				operation_word = 'geteilt durch'
			question = 'was ist ' + str(first_num)+' '+operation_word+' '+str(second_num)+' - '+str(answer)

		questions.append(question)

	print(questions)
	with open('new_source.txt', 'w') as f:
		for item in questions:
			f.write("%s" % item+'\n')

main()