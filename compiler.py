import sys
from compiler.parser.ifl import generate_lexer
from compiler.parser.ifl_yacc import generate_parser
from compiler.parser.preprocessor import clean_input
from compiler.analyzer.nodes import Program
from compiler.analyzer.semantic_analyzer import gen_tree
from compiler.generator.generator import generator

lexer, tokens = generate_lexer()

parser = generate_parser(lexer, tokens)
data = open(sys.argv[1]).read()
# data = open('examples/ex3.ifl').read()
cleaned_data = '\n'.join(clean_input(data))

lexer.input(cleaned_data)

while True:
    tok = lexer.token()
    if not tok: break

tree = parser.parse(cleaned_data)

t = gen_tree(tree)

generator(t)
print "Complilation Finished"
