import sys
import numpy as np
import ply.lex as lex

float_formatter = lambda x: "%.9f" % x
np.set_printoptions(formatter={'float_kind':float_formatter})

tokens = [ 'NUMBER_OF_ATOMS', 'EOL', 'SEP', 'LABEL',
           'SYMBOL', 'FLOAT' ]

t_LABEL = r'[a-zA-Z_][a-zA-Z0-9_\.]*'
t_EOL = r'\n'
t_SEP = r'\ +'


def t_SYMBOL(t):
    r'(X|H|He|Li|Be|B|C|N|O|F|Ne|Na|Mg|Al|Si|P|S|Cl|Ar|K|Ca|Sc|Ti|V|Cr|Mn|Fe|Co|Ni|Cu|Zn|Ga|Ge|As|Se|Br|Kr|Rb|Sr|Y|Zr|Nb|Mo|Tc|Ru|Rh|Pd|Ag|Cd|In|Sn|Sb|Te|I|Xe|Cs|Ba|La|Ce|Pr|Nd|Pm|Sm|Eu|Gd|Tb|Dy|Ho|Er|Tm|Yb|Lu|Hf|Ta|W|Re|Os|Ir|Pt|Au|Hg|Tl|Pb|Bi|Po|At|Rn|Fr|Ra|Ac|Th|Pa|U|Np|Pu|Am|Cm|Bk|Cf|Es|Fm|Md|No|Lr)(\ |\t)'
    t.value = t.value[:-1]
    return t

def t_NUMBER_OF_ATOMS(t):
    r'\d+\n'
    t.value = np.int(t.value)
    return t

def t_FLOAT(t):
    r'\-?\d\.\d{1,10}'
    t.value = np.float(t.value)
    return t

def t_error(t):
    raise TypeError("Unknown text '%s'" % (t.value,))

lex.lex()

lex.input(open("total.molden").read())
for tok in iter(lex.token, None):
    print(repr(tok.type), repr(tok.value))
