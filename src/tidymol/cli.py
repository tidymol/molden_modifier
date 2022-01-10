"""Helps to modify molden files
"""
# Local imports
from . import __version__
from .constants import SYMBOLS
from .exceptions import EmptyFile, NoMolecules
from .parsers.molden import parse

# Standard Library
import copy
import re
import sys
from logging import DEBUG, INFO, WARNING

# Third Party Libraries
import click
import pandas as pd
from loguru import logger
from molmod.molecules import Molecule

LOGLEVELS = {
    0: WARNING,
    1: INFO,
    2: DEBUG,
}


def convert_molecule_to_molmod(molecule):
    molModMolecule = Molecule(
        molecule.numbers,
        molecule.coordinates, molecule.label,
        symbols=molecule.symbols
    )
    molModMolecule.set_default_graph()
    return molModMolecule


def output(results):
    """Prints results

    :param result: The results of the modification
    :type result: List of molecules
    :return: None
    """
    for molecule in results:
        print(molecule)


def read_file(filename):
    data = ""
    with open(filename, 'r') as infile:
        for line in infile.readlines():
            data += re.sub(r" *$", "", line)
    if data is None:
        raise EmptyFile()
    molecules = parse(data)
    if molecules is None:
        raise NoMolecules()
    logger.info("Found %s molecules in %s", len(molecules), filename)
    return molecules


@click.group()
@click.version_option(__version__, prog_name="tidymol")
@click.option("-v", "--verbose", count=True, default=0)
@click.pass_context
def main(ctx, verbose):
    ctx.ensure_object(dict)
    ctx.obj["LOGLEVEL"] = LOGLEVELS.get(min(len(LOGLEVELS) - 1, verbose))
    logger.remove()
    logger.add(sys.stderr, level=ctx.obj["LOGLEVEL"])
    logger.info(f"tidymol version: {__version__}")
    logger.debug("Python version: {}".format(sys.version.split()[0]))


@main.command()
@click.argument("filename", type=click.Path(exists=True))
def info(filename):
    """Prints some basic information about the molden file."""
    molecules = read_file(filename)
    click.echo(f"Filename: {filename}")
    click.echo("=" * len(f"Filename: {filename}"))
    click.echo("Fileformat: .molden")
    click.echo(f"Number of Molecules: {len(molecules)}")


@main.command()
@click.option(
    "-f",
    "--filter-file",
    type=click.Path(exists=True),
    help="The molden file which is used for filtering.",
)
@click.argument("filename", type=click.Path(exists=True))
def filter(filter_file, filename):
    """Applies a specific filter on a molden file."""
    molecules = read_file(filename)
    molecules_filter = read_file(filter_file)
    filtered_list = list()
    for molecule in molecules:
        for molecule_filter in molecules_filter:
            if molecule.label == molecule_filter.label:
                filtered_list.append(molecule)
                continue
    output(filtered_list)


@main.command()
@click.option(
    "--compare",
    is_flag=True,
    help="The mirrored and the original molecule will be added both to the output file. This helps to compare it.",  # noqa
)
@click.argument("filename", type=click.Path(exists=True))
def mirror(compare, filename):
    """Mirrors the moleculs of the molden file."""
    molecules = read_file(filename)
    _molecules = list()
    for molecule in molecules:
        if compare:
            _molecules.append(copy.deepcopy(molecule))
        molecule.mirror()
        _molecules.append(molecule)
    _molecules = sorted(_molecules, key=lambda molecule: molecule.energy)
    output(_molecules)


@main.command()
@click.argument("filename", type=click.Path(exists=True))
def sort(filename):
    """Sorts the the moleculs of the molden file by energy."""
    molecules = read_file(filename)
    output(sorted(molecules, key=lambda molecule: molecule.energy))


@main.command()
@click.argument("filename", type=click.Path(exists=True))
@click.option(
    "-s",
    "--symbol",
    type=click.Tuple([str, click.Choice(SYMBOLS)]),
    help="The symbol",
)
def shortest_distance(symbol, filename):
    """Finds the shortest distance of every Hydrogen Bonding"""
    molecules = read_file(filename)
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
            H_neighbors = [
                (neighbor,  molModMolecule.distance_matrix[i][neighbor])
                for neighbor in neighbors_r1
                if molModMolecule.symbols[neighbor] == "H"
            ]
            shortest_H = sorted(H_neighbors, key=lambda neighbor: neighbor[1])[0]
            r1_index = shortest_H[0]
            r1_distance = shortest_H[1]

            neighbors_r2 = molModMolecule.graph.neighbors[r1_index]
            neighbors_r2 = list(filter(lambda neighbor: neighbor != i, neighbors_r2))
            X_neighbors = [
                (neighbor, molModMolecule.distance_matrix[r1_index][neighbor])
                for neighbor in neighbors_r2
                if molModMolecule.symbols[neighbor] == "O"
                or molModMolecule.symbols[neighbor] == symbol
            ]
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
            distances["types"].append(
                "{}-H-{}".format(symbol, molModMolecule.symbols[r2_index])
            )

    results = pd.DataFrame(distances)
    print(results)
