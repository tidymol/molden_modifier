import ply.yacc as yacc
import molden_lexer
from molden import Atom, Molecul
tokens = molden_lexer.tokens

def p_molden_file(p):
    '''molden_file : molecul
                   | molden_file molecul
    '''
    if len(p) > 2:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]

def p_molecul(p):
    '''molecul : NUMBER_OF_ATOMS FLOAT SEP LABEL EOL atoms EOL'''
    p[0] = Molecul(p[1], p[2], p[4], p[6])

def p_atom(p):
    '''atom : SYMBOL SEP FLOAT SEP FLOAT SEP FLOAT'''
    p[0] = Atom(p[1], p[3], p[5], p[7])

def p_atoms(p):
    '''atoms : atom
             | atoms EOL atom'''
    if len(p) > 2:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = [p[1]]

def p_error(p):
    print("Syntax error at '%s'" % p.value)


yacc.yacc()

test = yacc.parse(open("total.molden").read())
