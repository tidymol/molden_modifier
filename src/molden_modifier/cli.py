"""Helps to modify molden files

Usage:
    molden_modifier [options] mirror <molden_file> [--compare]
    molden_modifier [options] sort <molden_file>
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
    mirror            Mirrors the moleculs of the molden file.
    sort              Sorts the the moleculs of the molden file by energy.
"""

# Standard Library
import logging
import os
import sys
from logging.config import dictConfig

# Third Party Libraries
from docopt import DocoptExit, docopt, printable_usage

# Local imports
from . import __version__
from .commands import mirror, sort
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

def output(results, file_path):
    """Write the result to a file if the --output argument is set otherwise
       the result will be printed on stdout.

    :param result: The results of the modification
    :type result: List of molecules
    :param file_path: The file path to the output file
    :type file_path: str
    :return: None
    """
    path, filename = os.path.split(file_path)
    if path != "":
        os.makedirs(path, exist_ok=True)
    if file_path:
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
        with open(args['<molden_file>'], 'r') as infile:
            data = infile.read()
            molecules = parse(data)
            results = None
            if args["mirror"]:
                results = mirror(molecules, args["--compare"])
            elif args["sort"]:
                results = sort(molecules)
            else:
                raise RuntimeError("Unknown command")
            output(results, args["--output"])

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
