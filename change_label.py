#!/usr/bin/env python
import os
import sys
import re
import argparse
import datetime

_version = "1.0.0"

def change_label(in_path, out_path):
    find_energy = re.compile("(\d+\.\d{9}).*(mo_\d+\.out)")
    count = 1
    with open(in_path, 'r') as in_f, open(out_path, 'w') as out_f:
        number_of_elements = int(in_f.readline())
        while number_of_elements:
            energy_result = find_energy.search(in_f.readline())
            if energy_result:
                energy = float(energy_result.group(1))
            else:
                print("Could not find any energy for this moelcule.")
                sys.exit(1)
            out_f.write("DG={0:.1f}{1}HBr_n3_{2}\n".format(round(energy, 1)," "*8, count))
            for element in range(number_of_elements):
                out_f.write(in_f.readline())
            try:
                number_of_elements = int(in_f.readline())
                count +=1
            except ValueError:
                number_of_elements = 0


def main():
    name = "python-molden"
    usage = "%(prog)s [FUNCTION] [OPTIONS] [PARAMETER]"
    description = "Alter molden files"

    parser = argparse.ArgumentParser(prog=name, usage=usage, description=description)

    # Required Arguments
    parser.add_argument("molden_file", help="The file path of the molden file.")
    parser.add_argument("-o", "--output", dest="output", help="The path to the output file.")
    parser.add_argument("--version", action="version", version="%(prog)s {}".format(_version))
    args = parser.parse_args()

    if not args.output:
        now = datetime.datetime.now()
        out_file = "changed-label-{}.out".format(now.strftime("%Y-%m-%d_%H:%M"))
    else:
        out_file = args.output

    if os.path.isfile(args.molden_file):
        change_label(args.molden_file, out_file)
    else:
        print("The molden file does not exist!")


if __name__ == "__main__":
    main()
