# -*- coding: utf-8 -*-
"""
Grupo al007
Student id #92446
Student id #92498
"""

import numpy as np
from math import log
import copy
#c = 0

def createdecisiontree(D, Y, noise = False):
	examples = []
	attributes = []
	num_attributes = len(D[0])

#	global c
#	f = open('tests/log.txt', 'a')
#	f.write(f'Teste {c}\n\n')
#	f.write(f'D = {D}')
#	f.write(f'Y = {Y}\n\n')
#	f.close()
#	c+= 1

	for i in range(0, len(D)):
		d = []
		for j in range(0, num_attributes):
			d.append(D[i][j])

		examples.append([d,Y[i]])

	for j in range(0, num_attributes):
		a = []
		for i in range(0, len(D)):
			a.append(D[i][j])
		
		attributes.append(a)

	return decisiontreelearning(examples, attributes, examples)


def decisiontreelearning(examples, attributes, parent_examples):
	if examples == []:
		return plurality_value(parent_examples)
	elif same_classification(examples) and parent_examples != examples:
		return int(examples[0][1])
	elif attributes == []:
		return plurality_value(examples)
	else:
		importances = importance(attributes, examples)
		max_importance = max(importances)
		for i in range(0, len(importances)):
			if importances[i] == max_importance:
				tree = [i,] 
				break # TODO: heuristica
		
		i = tree[0]
		unique_attribute_values = np.unique(np.array(attributes[i]))
		for vk in unique_attribute_values:
			exs = []
			attrs = []

			for j in range(0, len(examples[0][0])):
				attrs.append([])

			for e in examples:
				if int(e[0][i]) == int(vk):
					exs.append(e)

					for j in range(0, len(e[0])):
						attrs[j].append(int(e[0][j]))

			subtree = decisiontreelearning(exs, attrs, examples)
			tree.append(subtree)

		return tree

def same_classification(examples):
	value = int(examples[0][1])
	for i in range(1, len(examples)):
		if value != int(examples[i][1]):
			return False
	
	return True

def plurality_value(examples):
	n_zero = 0
	n_ones = 0

	for i in range(0, len(examples)):
		if int(examples[i][1]) == 0:
			n_zero += 1
		else:
			n_ones += 1

	# TODO: heuristica
	if n_zero == n_ones:
		return 0

	return 0 if n_zero > n_ones else 1


''' list(Gain(A))
Gain de todos os atributos [G(a1), G(a2),... G(an)]
'''
def importance(attributes, examples):
	result = []
	p = 0
	n = 0

	for i in range(0, len(examples)):
		if int(examples[i][1]) == 0:
			n += 1
		else:
			p += 1

	B = entropy(p/(p+n))
	
	for attr in attributes:
		result.append(B - remainder(attr, examples, p+n))	
	return result

''' B(p)
entropy(p):
	p: valor a calcular a entropia
'''
def entropy(p):
	if p == 0 or p == 1:
		return 0
	
	n = 1 - p
	return -(p * log(p, 2) + n * log(n, 2))

''' --Remainder(A)--
remainder(attribute_values, classifcation, pn) :-
	attributes: valores da coluna do atributo
	examples: exemplos
	pn: p + n = numero de entradas na tabela 
'''
def remainder(attributes, examples, pn):
	uniques = np.unique(np.array(attributes))
	a = []

	for u in uniques:
		nk = 0
		pk = 0
		for i in range(0, len(attributes)):
			if int(attributes[i]) == u:
				if int(examples[i][1]) == 0:
					nk += 1
				else:
					pk += 1

		a.append(((pk + nk)/pn) * entropy(pk/(pk + nk)))


	return sum(a)


#D = [[0, 0, 0], [0, 0, 1], [0, 1, 0], [0, 1, 1], [1, 0, 0], [1, 0, 1], [1, 1, 0], [1, 1, 1]]
#Y = [0, 1, 1, 0, 0, 1, 1, 0]
#D = [[0, 0], [0, 1], [1, 0], [1, 1]]
#Y = [1, 1, 1, 0]

#print(createdecisiontree(D, Y))