from parser.ifl import generate_lexer
from parser.ifl_yacc import generate_parser
from parser.preprocessor import clean_input
from analyzer.nodes import Program
from analyzer.semantic_analyzer import *


lexer, tokens = generate_lexer()

parser = generate_parser(lexer, tokens)
data = open("examples/ex4.ifl").read()
cleaned_data = '\n'.join(clean_input(data))

lexer.input(cleaned_data)

while True:
    tok = lexer.token()
    if not tok: break
    print tok

tree = parser.parse(cleaned_data)

print "tree is "
print tree

print get_definitions(tree)
t = Program()
t = const_tree(tree, t, 0)

