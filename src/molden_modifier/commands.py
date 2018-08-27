"""Cli commands"""

# Standard Library
import copy
import logging

LOG = logging.getLogger(__name__)

def mirror(molecules, compare):
    copy_of_molecules = list()
    for molecule in molecules:
        if compare:
            copy_of_molecules.append(copy.deepcopy(molecule))
        molecule.mirror()
        copy_of_molecules.append(molecule)
    copy_of_molecules = sort(copy_of_molecules)
    return copy_of_molecules


def sort(molecules):
    return sorted(molecules, key=lambda molecule: molecule.energy)
