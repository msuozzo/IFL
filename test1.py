from parser.ifl import generate_lexer
from parser.ifl_yacc import generate_parser
from parser.preprocessor import clean_input
from analyzer.nodes import Node
from analyzer.semantic_analyzer import construct_tree, debug, tree_traversal


lexer, tokens = generate_lexer()

parser = generate_parser(lexer, tokens)
data = open("examples/ex1.ifl").read()
cleaned_data = '\n'.join(clean_input(data))

lexer.input(cleaned_data)

while True:
    tok = lexer.token()
    if not tok: break
    print tok

tree = parser.parse(cleaned_data)

print "tree is "
print tree

t = construct_tree(tree)



# print debug(t)
















