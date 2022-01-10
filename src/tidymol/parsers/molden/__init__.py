"""Parsing the molden structure"""

# Standard Library
import logging

# Third Party Libraries
import numpy as np
import ply.lex as lex
import ply.yacc as yacc
from molmod.periodic import periodic

# Local imports

LOG = logging.getLogger(__name__)

tokens = [ 'INT', 'FLOAT', 'EOL', 'SEP', 'LABEL',
           'SYMBOL']

t_LABEL = r'[a-zA-Z_][\w\._]+'
t_EOL = r'(\n|\r\n|\r)'
t_SEP = r'(\ +|\t+)'

def t_SYMBOL(t):
    r'(X|H|He|Li|Be|B|C|N|O|F|Ne|Na|Mg|Al|Si|P|S|Cl|Ar|K|Ca|Sc|Ti|V|Cr|Mn|Fe|Co|Ni|Cu|Zn|Ga|Ge|As|Se|Br|Kr|Rb|Sr|Y|Zr|Nb|Mo|Tc|Ru|Rh|Pd|Ag|Cd|In|Sn|Sb|Te|I|Xe|Cs|Ba|La|Ce|Pr|Nd|Pm|Sm|Eu|Gd|Tb|Dy|Ho|Er|Tm|Yb|Lu|Hf|Ta|W|Re|Os|Ir|Pt|Au|Hg|Tl|Pb|Bi|Po|At|Rn|Fr|Ra|Ac|Th|Pa|U|Np|Pu|Am|Cm|Bk|Cf|Es|Fm|Md|No|Lr)(\ |\t)'
    t.value = t.value[:-1]
    return t

def t_INT(t):
    r'(?m)^\d+\ *$'
    t.value = np.int(t.value)
    return t

def t_FLOAT(t):
    r'\-?\d+\.\d+'
    t.value = np.float(t.value)
    return t

def t_error(t):
    raise TypeError("Unknown text '%s'" % (t.value,))

LEXER = lex.lex()

def p_molden_file(p):
    '''molden_file : molecul
                   | molden_file molecul
                   | molden_file EOL
    '''
    if len(p) > 2:
        if p[2] == "\n":
            p[0] = p[1]
        else:
            p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]

def p_molecul(p):
    '''molecul : INT EOL FLOAT SEP LABEL EOL atoms EOL
               | INT EOL LABEL EOL atoms EOL
               | INT EOL atoms EOL'''
    if len(p) == 9:
        if not p[1] == len(p[7]):
            LOG.warning("Mismatch of the number_of_atoms in Molecule %s", p[5])
            LOG.warning("Parsed value: %s", p[1])
            LOG.warning("Real value of atoms: %s", len(p[7]))
            LOG.warning("The value will be automatically corrected")
        p[0] = Molecule(p[5], p[3], p[7])
    elif len(p) == 7:
        if not p[1] == len(p[5]):
            LOG.warning("Mismatch of the number_of_atoms in Molecule %s", p[3])
            LOG.warning("Parsed value: %s", p[1])
            LOG.warning("Real value of atoms: %s", len(p[5]))
            LOG.warning("The value will be automatically corrected")
        p[0] = Molecule(p[3], 0, p[5])
    else:
        if not p[1] == len(p[3]):
            LOG.warning("Mismatch of the number_of_atoms in Molecule")
            LOG.warning("Parsed value: %s", p[1])
            LOG.warning("Real value of atoms: %s", len(p[3]))
            LOG.warning("The value will be automatically corrected")
        p[0] = Molecule("", 0, p[3])

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
    try:
        LOG.error("{1}: Syntax error on '{0}'".format(p.value, LEXER.lineno))
    except AttributeError:
        LOG.error("{0}: Syntax error on line".format(LEXER.lineno))

yacc.yacc()


class Molecule(object):

    def __init__(self, label, energy, atoms):
        self._label = label
        self._energy = energy
        self._atoms = atoms


    @property
    def number_of_atoms(self):
        return len(self._atoms)

    @property
    def numbers(self):
        return [atom.number for atom in self._atoms]

    @property
    def symbols(self):
        return [atom.symbol for atom in self._atoms]

    @property
    def coordinates(self):
        return np.array([ atom.coordinates for atom in self._atoms])

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
        self._energy = np.float(energy)

    @property
    def atoms(self):
        return self._atoms

    @atoms.setter
    def atoms(self, atoms):
        if len(atoms) < 2:
            raise ValueError("A molecule needs to consist at least of two atoms.")
        self.number_of_atoms = len(atoms)
        self._atoms = atoms

    def get_atoms_by_symbol(self, symbol):
        return [ atom for atom in self._atoms if atom.symbol == symbol ]

    def get_indexes_by_symbol(self, symbol):
        return [ self._atoms.index(atom) for atom in self._atoms if atom.symbol == symbol ]

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
    def number(self):
        return periodic.atoms_by_symbol[self._symbol.lower()].number

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

    @property
    def coordinates(self):
        return np.array([self._x, self._y, self._z], np.float)

    def __str__(self):
        seperator = " "*5
        return "{0:<2}{sep}{1:>12.9f}{sep}{2:>12.9f}{sep}{3:>12.9f}".format(
                self._symbol, np.around(self._x, 9), np.around(self._y, 9),
                np.around(self._z, 9), sep=seperator)


def parse(data):
    return yacc.parse(data)
