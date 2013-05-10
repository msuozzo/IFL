from generator_functions import *
import os

def generate_code(node, id, tree):
    """Select the appropriate function based on the type of the node"""

    if node.type_ == "ADD":
        return generate_add(node, id, tree)

    elif node.type_ == "SET":
        return generate_set(node, id, tree)

    elif node.type_ == "PRINT":
        return generate_print(node, id, tree)
    else:
        return "pass"

def generate_action(action_phrase, statement_list):
    return "pass"


def generate_classes(tree):
    """Traverse through the tlts in the tree to generate code for classes"""

    # loop through all of the Definition Nodes in the tlts
    for node in tree.tlts:

        # create the file
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

        # set the initial location of the player to None and items to empty
        if node.id_ == "PLAYER":
            constructor_string += "\t\tself.location = None\n"
            constructor_string += "\t\tself.items = {}\n"

        # iterate through each statement in start and add it to constructor
        for statement in node.start:

            # get the code, add the appropriate tabs, and write to file
            # (Note that the code might be multi-lined)
            s = generate_code(statement, node.id_, tree)
            for line in s.splitlines():
                constructor_string += "\t\t" + line + "\n"

        # add the description if it has any
        if node.desc is not None:
            constructor_string += "\t\tself.description = '%s'" % node.desc



        # add the action_list of all the items in setting to self.action_list

        # add the action_list of all the characters in setting to self.action_list

        # create a list of actions if there is any
        action_string = ""
        if node.actions is not None:
            for a in node.actions:
                s = generate_action(a.action_phrase, a.statements)
                for line in s.splitlines():
                    action_string += "\t\t" + line + "\n"
            # create a self.action_list in the class
            # file.write("\t\tself.action_list.append(..)")

        # create a list of functions if there is any
        if hasattr(node, "FUNCTIONS"):
            pass

        # create a list of dialogues if there is any
        if hasattr(node, "DIALOGUE"):
            pass

        file.write(import_string)
        file.write(class_string)
        file.write(constructor_string)


        file.close()

    # end of the for loop here

def generate_game(tree):
    """Generate the main class file for the game"""

    # create the file
    file = open("./game/game.py", 'w')

    # loop through all of the Definition Nodes in the tlts and add the appropriate imports
    # also initialize any settings that are available and add them to a dictionary called settings
    settings = "\nsettings = {}\n"
    for node in tree.tlts:
        file.write("from %s import *\n" % node.id_)
        if node.type_ == "SETTING":
            # ex: settings['house'] = House()
            settings = settings + "settings['%s'] = %s()\n" %(node.id_, node.id_.title())

    file.write(settings)

    # main body of the game file begins here
    main = """
player = Player()

while True:
    if player.location is not None:
        print "You are at a " + settings[player.location].description

    print "\\nWhat would you like to do? (Enter 'help' for more):"
    input = raw_input(">>")

    if input == "help":
        help_string = "The following basic commands are supported: 'help', 'inventory', 'traits', 'inspect' 'quit'.\\n"
        help_string += "You can also type 'inspect item' to inspect a particular item.\\n"
        help_string += "The following actions are available: "


        print help_string

    elif input == "inventory":
        inventory_string = "The following items are in your inventory:\\n"
        for k, v in player.items.iteritems():
            # ex: "3 apples"
            inventory_string += v[1] + " " + k + "\\n"

        print inventory_string

    elif input == "traits":
        traits_string = "You have the following traits:\\n"

        print traits_string

    elif input == "quit":
        print "Game Over"
        quit()

    elif " " in input:
        input = input.split()
        action = input[0]
        noun = input[1]
        print "action is " + action
        print "noun is " + noun

    else:
        print "Command not recognized. Please enter commands in the form of 'action noun' (ex: 'get apple')."
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

