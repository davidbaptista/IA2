# -*- coding: utf-8 -*-
"""
Grupo al007
Student id #92446
Student id #92498
"""

import numpy as np
from math import log
from scipy import stats
import copy
c = 0

#chi_sq_table_5 = [3.841, 5.991, 7.815, 9.488, 11.070, 12.592, 14.067, 15.507, 16.919, 18.307, 19.675, 21.026, 22.362, 23.685, 24.996, 26.296, 27.587, 28.869, 30.144, 31.410, 32.671, 33.924, 35.172, 36.415, 37.652, 38.885, 40.113, 41.337, 42.557, 43.773, 44.985, 46.194, 47.400, 48.602, 49.802, 50.998, 52.192, 53.384, 54.572, 55.758, 56.942, 58.124, 59.304, 60.481, 61.656, 62.830, 64.001, 65.171, 66.339, 67.505]

def createdecisiontree(D, Y, noise = False):
	examples = []
	attributes = []
	num_attributes = len(D[0])

	for i in range(0, len(D)):
		d = []
		for j in range(0, num_attributes):
			d.append(D[i][j])

		examples.append([d,Y[i]])

	for j in range(0, num_attributes):
		a = [j, []]
		for i in range(0, len(D)):
			a[1].append(D[i][j])
		
		attributes.append(a)

	tree = decisiontreelearning(examples, attributes, examples)

	n = 0
	p = 0

	for e in Y:
		if e == 0:
			n += 1
		else:
			p += 1

	'''t = tree_pruning(tree, p, n)'''
	#print(f't={t}')
	return tree

'''pruning del ghetto

def tree_pruning(node):
	print(f'node: {node}')
	if isinstance(node, list):
		if node[1] == node[2]:
			node = node[1]
		elif isinstance(node[1], list):
			tree_pruning(node[1])
		elif isinstance(node[2], list):
			tree_pruning(node[2])
	return node'''
'''
def tree_pruning(node, p, n):
	#print(f'node={node}')
	all_leaves = True
	for i in range(1, len(node)):
		if isinstance(node[i], list):
			node = tree_pruning(node[i], p, n)
			all_leaves = False
	
	if all_leaves:
		delta = []
		for i in range(1, len(node)):
			#print(f'iteracao {i}')
			nk = 0
			pk = 0
			if int(node[i]) == 0:
				nk += 1
			else:
				pk += 1
		
			#print(f'p{p} n{n} pk{pk} nk{nk}')
			dp = p * ((pk + nk) / (p + n))
			dn = n * ((pk + nk) / (p + n))
			if dp == 0 or dn == 0:
				#print('return')
				continue
			#print(f'dp {dp} dn {dn}')
			delta.append((((pk - dp)**2) / dp) + (((nk - dn)**2) / dn))
		
		deviation = sum(delta)
		#print(f'deviation:{deviation} d:{p+n-1}')
		chi_sq = chi_sq_table_5[p+n]
		if deviation > chi_sq:
			print(f'deviation = {deviation} chi_sq = {chi_sq}')
			node = node[1] #TODO: heuristica
	return node'''



			


def decisiontreelearning(examples, attributes, parent_examples):
	global c
	c+= 1

	if examples == []:
		return plurality_value(parent_examples)
	elif same_classification(examples) and parent_examples != examples:
		return int(examples[0][1])
	elif attributes_empty(attributes):
		return plurality_value(examples)
	else:
		importances = importance(attributes, examples)
		max_importance = importances[0][1]
		

		for imp in importances:
			if imp[1] > max_importance:
				max_importance = imp[1]
		
		subtrees = []
		
		for i in range(0, len(importances)):
			if importances[i][1] == max_importance:
				tree = [importances[i][0],]
				subtrees.append(create_subtree(examples, attributes, tree, i))

		min_subtree = subtrees[0]
		for sub in subtrees[1:]:
			if len(str(sub)) < len(str(min_subtree)):
				min_subtree = sub
				
		return min_subtree


def create_subtree(examples, attributes, tree, i):
	unique_attribute_values = np.unique(np.array(attributes[i][1]))
	for vk in unique_attribute_values:
		exs = []
		attrs = []

		for j in range(0, len(attributes)):
			attrs.append([attributes[j][0], []])

		for e in examples:
			if int(e[0][i]) == int(vk):
				for j in range(0, len(e[0])):
					attrs[j][1].append(int(e[0][j]))

				# remover a coluna analisada
				en = copy.deepcopy(e)
				en[0].pop(i)
				exs.append(en)

		# remover atributo ja analisado
		attrs.pop(i)

		subtree = decisiontreelearning(exs, attrs, examples)
		tree.append(subtree)

	return tree

def attributes_empty(attributes):
	for attr in attributes:
		if attr[1] == []:
			return True
	return False

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
		result.append([attr[0], B - remainder(attr[1], examples, p+n)])	
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

D = [[1, 0, 0, 0,], [0, 0, 0, 1,], [1, 0, 1, 0,], [0, 0, 1, 1,], [1, 1, 0, 0,],[0, 1, 0, 1,], [1, 1, 1, 0,], [0, 1, 1, 1,]]
Y = [1, 1, 1, 1, 1, 1, 0, 1,]

createdecisiontree(D,Y,False)