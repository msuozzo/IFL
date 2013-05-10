from generator_functions import *
import os

def generate_code(node, id):
    """Select the appropriate function based on the type of the node"""

    # if node.type_ == "ADD":
    #     return generate_add(node, id)
    #
    # elif node.type_ == "SET":
    #     return generate_set(node, id)
    #
    # elif node.type_ == "PRINT":
    #     return generate_print(node, id)
    return "pass"


def generate_classes(tlts):
    """Traverse through the tlts to generate code for classes"""

    # loop through all of the Definition Nodes in the tlts
    for node in tlts:

        # create the file
        file = open("./game/" + node.id_ + ".py", 'w')

        # add the appropriate imports by looping through all of the definition nodes in tlts
        for element in tlts:
            if node.id_ != element.id_:
                file.write("from %s import *\n" % element.id_)

        # class declaration begins here
        file.write("\nclass %s:" % node.id_.title() + "\n")

        # iterate through each statement in start and add it to constructor
        file.write("\tdef __init__(self):\n")

        # set the initial location of the player to None
        if node.id_ == "PLAYER":
            file.write("\t\tself.location = None\n")

        for statement in node.start:

            # get the code, add the appropriate tabs, and write to file
            # (Note that the code might be multi-lined)
            s = generate_code(statement, node.id_)
            for line in s.splitlines():
                file.write("\t\t" + line + "\n")

        # add the description if it has any
        if node.desc is not None:
            file.write("\t\tself.description = '%s'" % node.desc)

        # create a list of functions is there is any
        if hasattr(node, "FUNCTIONS"):
            pass

        # create a list of actions if there is any
        if hasattr(node, "ACTIONS"):
            pass

        # create a list of dialogues if there is any
        if hasattr(node, "DIALOGUE"):
            pass

        file.close()

    # end of the for loop here

def generate_game(tlts):
    """Generate the main class file for the game"""

    # create the file
    file = open("./game/game.py", 'w')

    # loop through all of the Definition Nodes in the tlts and add the appropriate imports
    # also initialize any settings that are available and add them to a dictionary called settings
    settings = "\nsettings = {}\n"
    for node in tlts:
        file.write("from %s import *\n" % node.id_)
        if node.type_ == "SETTING":
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
        help_string = "The following basic commands are supported: 'help', 'inventory', 'traits', 'quit'"

        print help_string

    elif input == "inventory":
        inventory_string = "The following items are in your inventory: "

        print inventory_string

    elif input == "traits":
        traits_string = "You have the following traits: "

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
        print "Command not recognized. Please try again."
	    """

    file.write(main)


    file.close()


def generator(tree):
    """Generate Python code based on the tree that's given"""

    # create the game directory if it does not already exist
    if not os.path.exists("./game"):
        os.mkdir("./game")

    # create the classes for each ITEM, CHARACTER, TRAIT, and SETTING in the tlts
    generate_classes(tree.tlts)

    # create the while gloop that asks the user for inputs
    generate_game(tree.tlts)

