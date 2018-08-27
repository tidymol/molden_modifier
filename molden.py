import ply.lex as lex

tokens = [ NUMBER_OF_ATOMS, ENERGY, LABEL, SYMBOL
           X_CORD, Y_CORD, Z_CORD ]

t_NUMBER_OF_ATOMS,

class molecul(object):

    def __init__(self, number_of_atoms, energy):
        self.atoms = atoms[number_of_atoms]
        self.label = ""
        self.energy = energy

    @property
    def atoms(self):
        return self._atoms

    @atoms.setter
    def atoms(self, atoms):
        self._atoms = atoms

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



class atom(object):

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

    @propertz
    def z(self):
        return self._z

    @z.setter
    def z(self, z):
        self._z = z
