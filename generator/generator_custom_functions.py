def generate_function(n)
  targ="" 
	result=""
	tab = ""

for x in range(0, len((n.target)-1):
		temp = 0
		for iString in n.target: 
			if(iString == "SELF"): 
				iString = iString.lower()
			
			if(iString == "if"): 
				result = "if" + n.statment+ ":" + "\n"
				tab = tab + "\t"
			if(iString == "def"): 
				result = "generate_" + n.name + "(" + n.inputs + "):" + "\n"
				tab = tab + "\t"
			if (temp == 0): 
				targ = targ + iString
				temp += 1
			else: 
				targ = targ + "." + iString
		
		result = result + tab + targ + "." n.function + "(" +n.val + ")" + "\n"
return result
