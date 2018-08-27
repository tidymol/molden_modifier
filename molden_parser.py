import ply.yacc as yacc
import molden_lexer
tokens = molden_lexer.tokens


def p_atom (p):
    '''atom : SYMBOL SEP FLOAT SEP FLOAT SEP FLOAT'''

def p_atoms (p):
    '''atoms : atom
             | atoms SEP atom'''

def p_molecul (p):
    '''molecul : NUMBER_OF_ATOMS FLOAT SEP LABEL EOL atoms'''

def p_error(p):
    print("Syntax error at '%s'" % p.value)


yacc.yacc()

test = yacc.parse(open("total.molden").read())
#import pdb
#pdb.set_trace()
