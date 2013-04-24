from parser import ifl, ifl_yacc, preprocessor
######from generator import generator #not sure if this is the module to import
import sys
filename = sys.argv[1]
try:
  program_code = open(filename).read()
except:
  print "Couldn't load program at location '"+filename+"'"
  sys.exit()
l = ifl.generate_lexer()
lexer = l[0]
tokens = l[1]
parser = ifl_yacc.generate_parser(lexer, tokens)
cleaned = '\n'.join(preprocessor.clean_input(program_code))
lexer.input(cleaned)
#while True:
#  tok = lexer.token()
#  if not tok: break
#  print tok

lst = parser.parse(cleaned, debug=0)

### lst is the AST data structure
### pass this in to your generator function (ie. generator(lst))
