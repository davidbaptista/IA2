# -*- coding: utf-8 -*-
"""
Grupo al007
Student id #92446
Student id #92498
"""

import copy
import numpy as np
from math import log

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

	if noise:
		tree = topdown_pruning(tree, tree, examples)
		print(tree)
	'''if noise:
		tree_index = tree[0]
		tree_aux = tree
		tree = shorten(tree)

		if not isinstance(tree, list):
			tree = [tree_index, tree, tree]
		if not classify(tree, examples):
			tree = tree_aux

		tree = pruning(tree, tree, examples)
		print(f'tree after={tree}')'''
	return tree


def topdown_pruning(node, tree, examples):
	if isinstance(node, list):
		if isinstance(node[1], list):
			aux = node[1]
			node[1] = False
			if not classify(tree, examples):
				node[1] = True
				if not classify(tree, examples):
					node[1] = aux
					topdown_pruning(node[1], tree, examples)
		
		if isinstance(node[2], list):
			aux = node[2]
			node[2] = False
			if not classify(tree, examples):
				node[2] = True
				if not classify(tree, examples):
					node[2] = aux	
					topdown_pruning(node[2], tree, examples)
	return node


def shorten(node):
	if isinstance(node, list):
		node[1] = shorten(node[1])
		node[2] = shorten(node[2])

		if node[1] == node[2]:
			return node[1]
		else:
			return node
	else:
		return node

def pruning(node, tree, examples):
	if isinstance(node, list):
		node1_aux = node[1]
		node[1] = pruning(node[1], tree, examples)
		if not isinstance(node[1], list) and not classify(tree, examples):
			if node[1] == True:
				node[1] = False
			elif node[1] == False:
				node[1] = True
			if not classify(tree, examples):
				#print(f'mayaste com tree = {tree}')
				node[1] = node1_aux

		node2_aux = node[2]
		node[2] = pruning(node[2], tree, examples)

		if not isinstance(node[2], list) and not classify(tree, examples):
			if node[2] == True:
				node[2] = False
			elif node[2] == False:
				node[2] = True
			if not classify(tree, examples):
			#	print(f'mayaste 2x com tree = {tree}')
				node[2] = node2_aux

		if node[1] == node[2]:
			return node[1]
		elif not isinstance(node[1], list) and not isinstance(node[2], list):
			return 1
		else:
			return node
	else:
		return node


def decisiontreelearning(examples, attributes, parent_examples):
	if examples_empty(examples):
		return plurality_value(parent_examples)
	elif same_classification(examples) and parent_examples != examples:
		return int(examples[0][1])
	elif attributes_empty(attributes):
		return plurality_value(examples, parent_examples)
	else:
		subtrees = []

		if  examples == parent_examples:
			for i in range(0, len(attributes)):
				tree = [i,]
				subtrees.append(create_subtree(examples, attributes, tree, i))
		else:
			
			importances = importance(attributes, examples)
	
			max_importance = importances[0][1]
			for imp in importances:
				if imp[1] > max_importance:
					max_importance = imp[1]
			
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
	for vk in (False, True):
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

def classify(tree, examples):
	classifications = []
	
	for example in examples:
		wT = tree

		for i in range(len(example[0])):
			if example[0][wT[0]] == 0:
				if not isinstance(wT[1], list):
					classifications.append(wT[1])
					break
				else:
					wT = wT[1]
			else:
				if not isinstance(wT[2], list):
					classifications.append(wT[2])
					break
				else:
					wT = wT[2]
	
	i = 0
	for example in examples:
		if example[1] != classifications[i]:
			return False
		i+=1

	return True

def attributes_empty(attributes):
	if attributes == []:
		return True
	for attr in attributes:
		if attr[1] == []:
			return True
	return False

def examples_empty(examples):
	if examples == []:
		return True
	for ex in examples:
		if ex[1] == []:
			return True
	return False

def same_classification(examples):
	value = int(examples[0][1])
	for i in range(1, len(examples)):
		if value != int(examples[i][1]):
			return False
	
	return True

def plurality_value(examples, parent_examples=None):
	n_zero = 0
	n_ones = 0

	for i in range(0, len(examples)):
		if int(examples[i][1]) == 0:
			n_zero += 1
		else:
			n_ones += 1

	if n_zero == n_ones:
		n_zero = 0
		n_ones = 0
		
		if parent_examples:
			for i in range(0, len(parent_examples)):
				if int(parent_examples[i][1]) == 0:
					n_zero += 1
				else:
					n_ones += 1

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
	##print(f'examples_imp= {examples}, att_imp = {attributes}')

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

