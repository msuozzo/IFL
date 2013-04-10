from parser import ifl_yacc, ifl

l = ifl.generate_lexer()
lexer = l[0]
tokens = l[1]
parser = ifl_yacc.generate_parser(lexer, tokens)


