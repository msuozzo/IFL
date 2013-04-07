from parser.ifl import generate_lexer
lexer = generate_lexer()[0]
data = open("examples/ex2.ifl").read()
lexer.input(data)
while True:
  tok = lexer.token()
  if not tok: break
  print tok
