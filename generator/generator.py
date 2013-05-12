from generator_functions import FunctionGenerator
import os

def generate_classes(tree):
	"""Traverse through the tlts in the tree to generate code for classes"""

	# loop through all of the Definition Nodes in the tlts
	for node in tree.tlts:

		# create the file, ex: /game/PLAYER.py
		file = open("./game/" + node.id_ + ".py", 'w')

		# add the appropriate imports by looping through all of the definition nodes in tlts
		import_string = ""
		for element in tree.tlts:
			if node.id_ != element.id_:
				import_string += "from %s import *\n" % element.id_

		# class declaration begins here
		class_string = "\nclass %s:" % node.id_.title() + "\n"

		# constructor begins here
		constructor_string = "\tdef __init__(self):\n"

		# set the initial location and items of Characters and Settings to empty
		if node.type_ == "CHARACTER" or node.type_ == "SETTING":
			constructor_string += "\t\tself.location = None\n"
			constructor_string += "\t\tself.items = {}\n"


		# add the description if it has any
		if node.desc is not None:
			constructor_string += "\t\tself.description = '%s'\n" % node.desc


		# iterate through each statement in start and add it to constructor
		for statement in node.start:
			# get the code, add the appropriate tabs, and write to file
			# (Note that the code might be multi-lined)
			FG = FunctionGenerator(node.id_, tree)
			s = FG.generate_statement(statement)
			for line in s.splitlines():
				constructor_string += "\t\t" + line + "\n"


		# create a list of actions if there is any and append them to the action_list
		if node.type_ != "TRAIT":
			constructor_string += "\t\tself.default_action_list = []\n"

		action_string = ""
		if len(node.actions) > 0:
			FG = FunctionGenerator(node.id_, tree)
			for a in node.actions:
				s = FG.generate_action(a.action_phrase, a.statements)
				for line in s.splitlines():
					action_string += "\t" + line + "\n"
				constructor_string += "\t\tself.default_action_list.append('%s %s')\n" % (a.action_phrase, node.id_)


		# create a list of functions if there is any
		function_string = ""
		if len(node.functions) > 0:
			FG = FunctionGenerator(node.id_, tree)
			for f in node.functions:
				s = FG.generate_function(f)
				for line in s.splitlines():
					function_string += "\t" + line + "\n"


		# create a list of dialogues if there is any
		dialogue_string = ""
		if len(node.dialogues) > 0:
			FG = FunctionGenerator(node.id_, tree)
			s = FG.generate_dialogue(node.dialogues)
			dialogue_string += s
			# for line in s.splitlines():
			#     dialogue_string += "\t" + line + "\n"

		# add a characters dictionary to SETTING
		if node.type_ == "SETTING":
			constructor_string += "\t\tself.characters = {}\n"

		# create the _update_() method that updates all of the action_lists
		if node.type_ != "TRAIT":
			constructor_string += "\t\tself._update_()\n"

			function_string += """
	def _update_(self):
		self.action_list = []
		self.action_list.extend(self.default_action_list)
		for attribute in vars(self):
			n = getattr(self, attribute)
			if hasattr(n, "action_list"):
				for a in n.action_list:
					if a not in self.action_list:
						self.action_list.append(a)
"""
		# allow characters and settings to update their items as well
		if node.type_ == "SETTING" or node.type_ == "CHARACTER":
			function_string += """
		for v in self.items.values():
			for a in v[0].action_list:
				if a not in self.action_list:
					self.action_list.append(a)
"""
		file.write(import_string)
		file.write(class_string)
		file.write(constructor_string)
		file.write(action_string)
		file.write(function_string)
		file.write(dialogue_string)

		file.close()

	# end of the for loop here

def generate_game(tree):
	"""Generate the main class file for the game"""

	# create the file
	file = open("./game/game.py", 'w')

	# loop through all of the Definition Nodes in the tlts and add the appropriate imports
	# also initialize any settings that are available and add them to a dictionary called settings

	# loop through all of the definition nodes and add the appropriate imports, initialize settings
	# and characters, and create a list of all the traits and characters
	traits = []
	characters = []
	settings = []

	for node in tree.tlts:
		file.write("from %s import *\n" % node.id_)
		if node.type_ == "SETTING":
			settings.append(node.id_)
		if node.type_ == "TRAIT":
			traits.append(node.id_)
		if node.type_ == "CHARACTER":
			characters.append(node.id_.lower())

	settings_string = "\nsettings = {}\n"
	for s in settings:
		# ex: settings['house'] = House()
		settings_string += "settings['%s'] = %s()\n" %(s, s.title())

	traits_string = "traits = ["
	for t in traits:
		traits_string += "\"" + t + "\","
	traits_string += "]\n"

	characters_string = "characters = ["
	character_initialization = ""
	for c in characters:
		characters_string += "\"" + c + "\","
		character_initialization += "%s = %s()\n" %(c, c.title())
		character_initialization += "settings[%s.location].characters['%s'] = %s\n" %(c, c, c)
	characters_string += "]\n"

	file.write(settings_string)
	file.write(traits_string)
	file.write(characters_string)
	file.write(character_initialization)

	# main body of the game file begins here
	main = """

for k, v in settings.iteritems():
	v._update_()

while True:
	if player.location is not None:
		print "\\nYou are at a " + settings[player.location].description

	print "What would you like to do? (Enter 'help' for more):"
	input = raw_input(">>")

	if input == "help":
		help_string = "The following basic commands are supported: 'help'; 'inventory'; 'traits'; 'inspect'; 'quit';\\n"
		help_string += "You can also type 'inspect item' to inspect a particular item.\\n"

		if player.location in settings:
			help_string += "The following actions are available: "
			for action in settings[player.location].action_list:
				help_string += "'" + action.split()[0] + "'; "

		print help_string

	elif input == "inventory":
		inventory_string = "The following items are in your inventory:\\n"
		for k, v in player.items.iteritems():
			# ex: "3 apples"
			inventory_string += "\\t" + str(v[1]) + " " + k

		print inventory_string

	elif input == "traits":
		traits_string = "You have the following traits:\\n"

		attributes = vars(player)
		for a in attributes:
			if a in traits:
				traits_string += a

				b = getattr(player,a)
				c = vars(b)
				count = 0
				for d in c:
					if count == 0:
						traits_string += ": "
					else:
						traits_string += ", "

					val = c[d]
					traits_string += d + " = {val}".format(val=val)
					count+=1

				traits_string += "\\n"

		print traits_string

	elif input == "inspect":
		if player.location is None or player.location not in settings:
			inspect_string = "You are nowhere!"
		else:
			inspect_string = "You see the following items in the %s: " % player.location
			for k, v in settings[player.location].items.iteritems():
				inspect_string += k + " "

			inspect_string += "\\nYou see the following characters in the %s: " % player.location
			for k, v in settings[player.location].characters.iteritems():
				if k != "player":
					inspect_string += k + " "

		print inspect_string

	elif input == "quit":
		print "Game Over"
		quit()

	elif " " in input:

		# searches through all of the available actions in items
		# searches through the player first, then the setting

		tmp = input.split()
		action = tmp[0]
		noun = tmp[1]

        if action == "inspect":
            for k, v in settings[player.location].characters.iteritems():
                if k == noun:
                    print k.description
            for k, v in settings[player.location].items.iteritems():
                if k == noun:
                    print k.description
		elif input in player.action_list:

			print "in player.action_list!"

			# check if it is an action in player
			attributes = dir(player)
			if noun in attributes:
				getattr(player, action)(settings, player)

			# check if it is an action in one of player's items
			elif noun in player.items:
				getattr(player.items[noun][0], action)(settings, player)



		elif input in settings[player.location].action_list:

			# check if nonu is an item in current setting
			if noun in settings[player.location].items:
				getattr(settings[player.location].items[noun][0], action)(settings, player)
			else:
				# check if noun is an action in one of the characters in the current setting
				for k, v in settings[player.location].characters.iteritems():
					if k == noun:
						getattr(v, action)(settings, player)
					elif k != "player" and noun in v.items:
						getattr(v.items[noun][0], action)(settings, player)

		else:
			print "Can't %s" % input

	else:
		print "Command not recognized. Please enter commands in the form of 'action noun' (ex: 'get apple')."


	# updating all of actions_list in player and setting
	for k, v in settings[player.location].characters.iteritems():
		v._update_()

	settings[player.location]._update_()
		"""

	file.write(main)

	file.close()


def generator(tree):
	"""Generate Python code based on the tree that's given"""

	# create the game directory if it does not already exist
	if not os.path.exists("./game"):
		os.mkdir("./game")

	# create the classes for each ITEM, CHARACTER, TRAIT, and SETTING in the tlts
	generate_classes(tree)

	# create the while loop that asks the user for inputs
	generate_game(tree)

