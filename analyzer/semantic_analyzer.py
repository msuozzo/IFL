from parser import ifl_yacc, ifl
from nodes import Node

l = ifl.generate_lexer()
lexer = l[0]
tokens = l[1]
parser = ifl_yacc.generate_parser(lexer, tokens)

def debug(node, tabs_count = 0):
	"""Prints out all of the children of a Node."""
	text = ""
	tabs = " "
	for i in range(tabs_count):
		tabs = tabs + "\t"

	for n in node.get_children():
		print "n is "
		print n
		if type(n) is Node:
			text = text + tabs + debug(n, tabs_count + 1)
			text = text + "\n"
		elif n is None:
			text = text + "\n" + tabs + "None"
		else:
			text = text + "\n" + tabs + n

	return text

def construct_tree(data):
	"""Create a tree based on the input from the parser."""
	current_parent = Node("parent")

	for token in data:
		if type(token) is tuple:
			n = construct_tree(token)
			current_parent.add_child(n)
		else:
			current_parent.add_child(token)

	return current_parent