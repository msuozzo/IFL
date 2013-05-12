from parser.ifl_lex import generate_lexer
from parser.ifl_yacc import generate_parser
from parser.preprocessor import clean_input
from analyzer.nodes import Program
from analyzer.semantic_analyzer import gen_tree
from generator.generator import generator


lexer, tokens = generate_lexer()

parser = generate_parser(lexer, tokens)
data = open("test/test1.ifl").read()
cleaned_data = '\n'.join(clean_input(data))

lexer.input(cleaned_data)

while True:
    tok = lexer.token()
    if not tok: break
    print tok

tree = parser.parse(cleaned_data, debug=1)

print "tree is "
print tree

t = gen_tree(tree)


generator(t)

print "done"
