"""Parsing the molden structure"""

# Standard Library
import logging

# Third Party Libraries
import numpy as np
import ply.lex as lex
import ply.yacc as yacc

# Local imports

LOG = logging.getLogger(__name__)

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
    r'\d+(\ +)?\n'
    t.value = np.int(t.value)
    return t

def t_FLOAT(t):
    r'\-?\d\.\d{1,10}'
    t.value = np.float(t.value)
    return t

def t_error(t):
    raise TypeError("Unknown text '%s'" % (t.value,))

lex.lex()

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
    p[0] = Molecule(p[1], p[2], p[4], p[6])

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


class Molecule(object):

    def __init__(self, number_of_atoms, energy, label, atoms):
        self._number_of_atoms = number_of_atoms
        self._energy = energy
        self._label = label
        self._atoms = atoms

    @property
    def number_of_atoms(self):
        return self._number_of_atoms

    @number_of_atoms.setter
    def number_of_atoms(self, number_of_atoms):
        self._number_of_atoms = number_of_atoms

    @property
    def label(self):
        return self._label

    @label.setter
    def label(self, label):
        self._label = label

    @property
    def energy(self):
        return self._energy

    @energy.setter
    def energy(self, energy):
        self._energy = energy

    @property
    def atoms(self):
        return self._atoms

    @atoms.setter
    def atoms(self, atoms):
        self._atoms = atoms

    def mirror(self, compare=None):
        self.label = "ent_{}".format(self.label)
        for atom in self.atoms:
            atom.x *=  -1

    def __str__(self):
        output = "{}\n".format(self.number_of_atoms)
        output += "{0:<12.9f}     {1}\n".format(
                self.energy, self.label)
        for atom in self.atoms:
            output += "{}\n".format(str(atom))
        return output


class Atom(object):

    def __init__(self, symbol, x, y, z):
        self._symbol = symbol
        self._x = x
        self._y = y
        self._z = z

    @property
    def symbol(self):
        return self._symbol

    @symbol.setter
    def symbol(self, symbol):
        self._symbol = symbol

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, x):
        self._x = x

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, y):
        self._y = y

    @property
    def z(self):
        return self._z

    @z.setter
    def z(self, z):
        self._z = z

    def __str__(self):
        seperator = " "*5
        return "{0:<2}{sep}{1:>12.9f}{sep}{2:>12.9f}{sep}{3:>12.9f}".format(
                self._symbol, np.around(self._x, 9), np.around(self._y, 9),
                np.around(self._z, 9), sep=seperator)


def parse(data):
    return yacc.parse(data)
