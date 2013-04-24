from Trait import Trait
from Character import Character
import re
from pprint import pprint

class Node(object):
	def __init__(self, data):
		self.data = data
		self.children = []

	def add_child(self, object):
		self.children.append(object)

	def add_child_front(self, object):
		self.children.insert(0, object)

	def get_children(self):
		return self.children

def debug(node, tabs_count = 0):
	"""Prints out all of the children of a Node."""
	text = ""
	tabs = " "
	for i in range(tabs_count):
		tabs = tabs + "\t"

	for n in node.get_children():
		if type(n) is Node:
			text = text + tabs + debug(n, tabs_count + 1)
			text = text + "\n"
		else:
			text = text + "\n" + tabs + n

	return text


def code_generator(node):
	if node.get_children()[0] == "":
		return trait_generator(node)



def construct_tree(data):
	"""Create a tree based on the input from the parser."""
	root = Node("root")
	current_parent = root
	stack = []

	for token in data:
		# push tokens unto stack until ")" is detected
		# when ")" is detected, pop the stack and create children to be inserted
		if token == ")":
			n = Node("")

			symbol = stack.pop()

			while (symbol) != "(":
				n.add_child_front(symbol)
				symbol = stack.pop()

			# semantic analyzer can be implemented here

			#n = code_generator(n)

			stack.append(n)

		else:
			stack.append(token)

	return stack.pop()

def traverse_tree(file, tree):
	"""Traverse through the tree in a DFS format to generate code"""

	for node in tree.get_children():
		pass

def main():

    # set up the header
    file = open("output.py", 'w')

    # cleanse input from the tree
    data = open("tree1.txt").read()
    data = re.split("(\(|\)|,+\s)", data)
    data = filter(lambda a: a != ", ", data) 
    data = filter(lambda a: a != "", data)

    for i in data:
    	print "*" + i + "*"

    tree = construct_tree(data)

    print "The tree is: "
    print debug(tree)

    #traverse_tree(file, tree)

#   health = Trait()
#	health.setValue('current', 50)

#	health.setValue('current', 100)

#	player = Character()
#	player.setValue("health", health)

# 	print "Hello, I am a character"

if __name__ == '__main__':
    main()















