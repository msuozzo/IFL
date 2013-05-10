# generates a print statement
#'print : PRINT string_expression'
def generate_print(n):
    return "print " + n.string_expr + "\n"

# generates add statement
def generate_add(n, name):
    targ = ""

    #if(n is None): --- IGNORE FOR NOW - need to fix quantity

    # checks to see how many parts of target list
    if len(n.to) > 1 :
        temp = 0
        # iterates through list of target
        for iString in n.to:
            # special case of first one
            if(iString == name):
                iString = "self"

            if(temp == 0):
                targ = targ + iString
                temp += 1
            else: # all other iterations
                targ = targ + "." + iString

    else: # only one target
        if n.to[0] == name:
            targ = "self"
        else:
            targ = n.to[0]

    # checks what type of add it is
    if n.primitive is None: # not a primitive add
        if n.id_[0] == "trait":
            return "" + targ + "." + n.id_[1] + " = " + n.id_[1].capitalize()  + "()\n"
    else: # primitive add
        return "" + targ + "." + n.primitive.name + " = " + n.primitive.val[1]  + "()\n"

    return ""


def generate_set(n, name):
    targ = ""

    if(len(n.target) > 1):
        temp = 0
        for iString in n.target:
            if(iString == name):
                iString = "self"

            if(temp == 0):
                targ = targ + iString
                temp += 1
            else:
                targ = targ + "." + iString

    else:
        if n.target[0] == name:
            targ = "self"
        else:
            targ = n.target[0]

    return "" + targ + "=" + n["value"] +"\n"

def generate_increase(n):
	targ = ""

	if(len(n["target"]) > 1):
    	temp = 0
    	for iString in n["target"]:
        	if(iString == "SELF"):
            	iString = iString.lower()

        	if(temp == 0):
            	targ = targ + iString
            	temp += 1
        	else:
            	targ = targ + "." + iString

    else: # only one target
        if n["target"][0] == "SELF":
            targ = n["target"][0].lower()
        else:
            targ = n["target"][0]

	return "" + targ + "+=" + n["value"] +"\n"



def generate_decrease(n):
	targ = ""

	if(len(n["target"]) > 1):
    	temp = 0
    	for iString in n["target"]:
        	if(iString == "SELF"):
            	iString = iString.lower()

        	if(temp == 0):
            	targ = targ + iString
            	temp += 1
        	else:
            	targ = targ + "." + iString

    else: # only one target
        if n["target"][0] == "SELF":
            targ = n["target"][0].lower()
        else:
            targ = n["target"][0]

	return "" + targ + "-=" + n["value"] +"\n"
