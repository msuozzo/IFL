from parser.ifl import generate_lexer
from parser.ifl_yacc import generate_parser
from parser.preprocessor import clean_input

lexer, tokens = generate_lexer()

parser = generate_parser(lexer, tokens)
data = open("examples/ex1.ifl").read()
cleaned_data = '\n'.join(clean_input(data))

lexer.input(cleaned_data)

while True:
    tok = lexer.token()
    if not tok: break
    print tok

print parser.parse(cleaned_data)

