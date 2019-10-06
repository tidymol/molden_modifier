"""Helps to modify molden files

Usage:
    molden_modifier [options] info <molden_file>
    molden_modifier [options] filter -f FILTER <molden_file>
    molden_modifier [options] mirror [--compare] <molden_file>
    molden_modifier [options] sort <molden_file>
    molden_modifier [options] shortest_distance -s SYMBOL <molden_file>
    molden_modifier -h | --help | --version

Required Arguments:
    <molden_file>     Path to Molden file (file extension .molden)

Options:
    -h, --help        Shows this help
    --version         Prints the version
    -v                Raise verbosity level
    --output=<OUTFILE>, -o <OUTFILE>
                      Optional file where results are written to

Subcommands:
    info                  Prints some basic information about the molden file.
    filter                Applies a specific filter on a molden file.
    sort                  Sorts the the moleculs of the molden file by energy.
    Options:
        -f <FILTER>       The molden file which is used for filtering.

    mirror                Mirrors the moleculs of the molden file.
    Options:
        --compare         The mirrored and the original molecule will be added
                          both to the output file. This helps to compare it.

    shortest_distance     Finds the shortest distance of every Hydrogen Bonding
    Options:
        -s <SYMBOL>       The Symbol ...
"""

# Standard Library
import logging
import os
import re
import sys
from logging.config import dictConfig

# Third Party Libraries
from docopt import DocoptExit, docopt, printable_usage

# Local imports
from . import __version__
from .commands import info, filter, mirror, sort, shortest_distance
from .common import DEFAULT_LOGGING_DICT, LOGLEVELS, errorcode
from .molden import parse

#: Use __package__, not __name__ here to set overall LOGging level:
LOG = logging.getLogger(__package__)


def parsecli(cliargs=None):
    """Parse CLI arguments with docopt

    :param cliargs: List of commandline arguments
    :type cliargs: list(str)
    :return: dictionary from :class:`docopt.docopt`
    :rtype: dict
    """
    version = "%s %s" % (__package__, __version__)
    args = docopt(__doc__,
                  argv=cliargs, version=version)
    dictConfig(DEFAULT_LOGGING_DICT)
    LOG.setLevel(LOGLEVELS.get(args['-v'], logging.DEBUG))

    return args


def checkargs(args):
    """Check arguments for validity

    :param args: parsed arguments from :class:`docopt.docopt`
    :type args: dict
    :raises: :class:`docopt.DocoptExit`, :class:`FileNotFoundError`
    :return:
    """
    molden_file = args['<molden_file>']
    if molden_file is None:
        raise DocoptExit()
    if not os.path.exists(molden_file):
        raise FileNotFoundError(molden_file)


def output(results, file_path, cvs):
    """Write the result to a file if the --output argument is set otherwise
       the result will be printed on stdout.

    :param result: The results of the modification
    :type result: List of molecules
    :param file_path: The file path to the output file
    :type file_path: str
    :return: None
    """
    if results is None:
        return None
    path, filename = os.path.split(file_path)
    if path != "":
        os.makedirs(path, exist_ok=True)
    if file_path:
        if cvs:
            results.to_csv(file_path)
        else:
            with open(file_path, "w") as outfile:
                for molecule in results:
                    outfile.write(str(molecule))
    else:
        for molecule in results:
            print(molecule)


def main(cliargs=None):
    """Entry point for the application script

    :param list(str) cliargs: Arguments to parse or None (=use ``sys.argv``)
    :return: return codes from :func:`molden_modifier.common.errorcode`
    :rtype: int
    """
    try:
        args = parsecli(cliargs)
        LOG.info('%s version: %s', __package__, __version__)
        LOG.debug('Python version: %s', sys.version.split()[0])
        LOG.debug("CLI result: %s", args)
        checkargs(args)
        data = ""
        with open(args['<molden_file>'], 'r') as infile:
            for line in infile.readlines():
                data += re.sub(r" *$", "", line)
        if data is None:
            Log.error("Empty file")
            sys.exit(1)
        molecules = parse(data)
        if molecules is None:
            LOG.info("No molecules found!")
            sys.exit(1)
        LOG.info("Found %s molecules in %s", len(molecules), args['<molden_file>'])
        results = None
        cvs = False
        if args["mirror"]:
            results = mirror(molecules, args["--compare"])
        elif args["filter"]:
            with open(args["-f"], 'r') as filter_file:
                filter_data = filter_file.read()
                molecules_filter = parse(filter_data)
                results = filter(molecules_filter, molecules)
        elif args["info"]:
            info(molecules)
        elif args["sort"]:
            results = sort(molecules)
        elif args["shortest_distance"]:
            results = shortest_distance(molecules, args["-s"])
            cvs = True
        else:
            raise RuntimeError("Unknown command")
        output(results, args["--output"], cvs)

        LOG.info("Done.")
        return 0

    except DocoptExit as error:
        LOG.fatal("Need a molden file.")
        printable_usage(__doc__)
        return errorcode(error)

    except FileNotFoundError as error:
        LOG.fatal("File not found '%s'", error)
        return errorcode(error)

    except RuntimeError as error:
        LOG.fatal("Something failed  '%s'", error)
        return 1

    except KeyboardInterrupt as error:
        return errorcode(error)
