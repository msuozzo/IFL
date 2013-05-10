# generates a print statement
#'print : PRINT string_expression'
def generate_print(n):
    return "print " + n["value"] + "\n"

def generate_set(n):
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

    else:
        if (n["target"][0] == "SELF"):
            targ = n["target"][0].lower()
        else:
            targ = n["target"][0]

    return "" + targ + "=" + n["value"] +"\n"


# generates add statement
def generate_add(n):

    #add : ADD quantity ID to_or_nothing
    # ex/ ADD apple TO player

    targ = ""

    if(n["quantity"] is None):
        # iterates through list of target
        if len(n["target"]) > 1 :
            temp = 0
            for iString in n["target"]:
                # special case of first one
                if(iString == "SELF"):
                    iString = iString.lower()

                if(temp == 0):
                    targ = targ + iString
                    temp += 1
                else: # all other iterations
                    targ = targ + "." + iString

        else: # only one target
            if n["target"][0] == "SELF":
                targ = n["target"][0].lower()
            else:
                targ = n["target"][0]

        return "" + targ + "." + n["obj"].ID + " = " + n["obj"].value + "\n"



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
