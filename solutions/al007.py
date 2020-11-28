# -*- coding: utf-8 -*-
"""
Grupo al007
Student id #92446
Student id #92498
"""

import numpy as np
from math import log


def createdecisiontree(D, Y, noise = False):
	pass

def decisiontreelearning(examples, atributes, parent_examples):
	if examples is []:
		return plurality_value(parent_examples)
	else:
		for i in range(0, len(atributes)):
			imp = importance(atributes, examples)
			if imp[i] == max(imp):
				tree = [i, 0, 0]
		
		

def plurality_value(arr):
	counter = 0
	num = arr[0]

	for i in arr:
		current = arr.count(i)
		if(current > counter):
			counter = current
			num = i

	return num

''' list(Gain(A))
Gain de todos os atributos [G(a1), G(a2),... G(an)]
'''
def importance(atributes, examples):
	result = []

	p = examples.count(1)
	n = examples.count(0)

	B = entropy(p/(p+n))
	
	for attr in atributes:
		result.append(B - remainder(attr, examples, p+n))	
	return result

''' B(p)
entropy(p):
	p: valor a calcular a entropia
'''
def entropy(p):
	n = 1 - p
	return -p * log(p, 2) + n * log(n, 2)

''' --Remainder(A)--
remainder(attribute_values, classifcation, pn) :-
	attribute_values: valores da coluna do atributo
	classification_values: valor da classificacao correspondente ao valor do atributo
	pn: p + n = numero de entradas na tabela 
'''
def remainder(attribute_values, classification_values, pn):
	uniques = np.unique(attribute_values)
	nk = 0
	pk = 0
	a = []

	for u in uniques:
		for i in range(0, len(attribute_values)):
			if attribute_values[i] == u:
				if classification_values[i] == 0:
					nk += 1
				else:
					pk += 1
					
		a.append(((pk + nk)/pn) * entropy(pk/(pk + nk)))

	return sum(a)

def classify(T, data):
	pass