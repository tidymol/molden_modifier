"""Cli commands"""

# Standard Library
import copy
import logging
import pdb
import pandas as pd

from molmod.molecules import Molecule

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

def convert_molecule_to_molmod(molecule):
    molModMolecule = Molecule(molecule.numbers,
            molecule.coordinates, molecule.label,
            symbols=molecule.symbols)
    molModMolecule.set_default_graph()
    return molModMolecule

def shortest_distance(molecules, symbol, max_distance=100):
    distances = {
        "molecules": [],
        "indxs_a": [],
        "indxs_H": [],
        "indxs_b": [],
        "q1s": [],
        "q2s": [],
        "types": [],
    }
    for indx, molecule in enumerate(molecules):
        indexes = molecule.get_indexes_by_symbol(symbol)
        molModMolecule = convert_molecule_to_molmod(molecule)
        for i in indexes:
            neighbors_r1 = molModMolecule.graph.neighbors[i]
            H_neighbors = [(neighbor, molModMolecule.distance_matrix[i][neighbor]) for neighbor
                           in neighbors_r1
                           if molModMolecule.symbols[neighbor] == "H"]
            shortest_H = sorted(H_neighbors, key=lambda neighbor: neighbor[1])[0]
            r1_index = shortest_H[0]
            r1_distance = shortest_H[1]

            neighbors_r2 = molModMolecule.graph.neighbors[r1_index]
            neighbors_r2 = list(filter(lambda neighbor: neighbor != i, neighbors_r2))
            X_neighbors = [(neighbor, molModMolecule.distance_matrix[r1_index][neighbor]) for neighbor
                           in neighbors_r2
                           if molModMolecule.symbols[neighbor] == "O"
                           or molModMolecule.symbols[neighbor] == symbol]
            shortest_X = sorted(X_neighbors, key=lambda neighbor: neighbor[1])[0]
            r2_index = shortest_X[0]
            r2_distance = shortest_X[1]

            q1 = (r1_distance-r2_distance)/2.0
            q2 = r1_distance+r2_distance

            distances["molecules"].append(indx)
            distances["indxs_a"].append(i+1)
            distances["indxs_H"].append(r1_index+1)
            distances["indxs_b"].append(r2_index+1)
            distances["q1s"].append(q1)
            distances["q2s"].append(q2)
            distances["types"].append("{}-H-{}".format(symbol,
                molModMolecule.symbols[r2_index]))

    results = pd.DataFrame(distances)
    return results
