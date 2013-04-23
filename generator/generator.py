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

def debug(node, tabs_count = 0):
	text = ""

	tabs = " "
	for i in range(tabs_count):
		tabs = tabs + "\t"

	for n in node.children:
		if type(n) is Node:
			text = text + tabs + debug(n, tabs_count + 1)
			text = text + "\n"
		else:
			text = text + "\n" + tabs + n

	return text


def construct_tree(data):
	
	root = Node("root")
	current_parent = root
	stack = []

	for token in data:
		# push tokens unto stack until ")" is detected
		# when ")" is detected, pop the stack and create children to be inserted
		if token == ")":
			n = Node("parent")

			symbol = stack.pop()
			while (symbol) != "(":
				n.add_child_front(symbol)
				symbol = stack.pop()

			stack.append(n)

		else:
			stack.append(token)

	return stack.pop()


def main():

    # set up the header
    file = open("output.py", 'w')
    file.write('from Trait import Trait\n')
    file.write('from Character import Character\n')
   
    data = open("tree1.txt").read()
    data = re.split("(\(|\)|,+\s)", data)
    data = filter(lambda a: a != ", ", data) 
    data = filter(lambda a: a != "", data)

  #   for item in data:
		# print "*" + item + "*"

    t = construct_tree(data)

    print debug(t)

#    health = Trait()
#	health.setValue('current', 50)

#	health.setValue('current', 100)

#	player = Character()
#	player.setValue("health", health)

# 	print "Hello, I am a character"

if __name__ == '__main__':
    main()















