#! /usr/bin/env python
## @PowhegControl MergeLHE
#  PowhegControl LHE merger
#
#  Authors: James Robinson  <james.robinson@cern.ch>

import argparse
import logging
import shutil

parser = argparse.ArgumentParser(description="Combine LHE files into a single file.")
parser.add_argument(
    "output_file", metavar="file_name", type=str, help="an output LHE file"
)
parser.add_argument(
    "input_files", metavar="file_list", nargs="+", help="a list of input LHE files"
)
args = parser.parse_args()

logging.basicConfig(format="%(message)s", level=logging.INFO)
logger = logging.getLogger("LHE_merger")
logger.info(
    "Preparing to create {0} from {1} input files".format(
        args.output_file, len(args.input_files)
    )
)
nEvents = 0

# Open output file
with open(args.output_file, "ab") as output_file:

    # Start with the first file
    logger.info("... working on {0}".format(args.input_files[0]))
    output_footer = []
    with open(args.input_files[0], "rb") as input_file:
        in_LesHouchesEvents = True
        for line in input_file:
            if "<event>" in line:
                nEvents += 1
            if "</LesHouchesEvents>" in line:
                in_LesHouchesEvents = False
            if in_LesHouchesEvents:
                output_file.write(line)
            else:
                output_footer.append(line)

    # Now append other files in turn
    for file_name in args.input_files[1:]:
        logger.info("... working on {0}".format(file_name))
        in_event = False
        with open(file_name, "rb") as input_file:
            for line in input_file:
                if "<event>" in line:
                    in_event = True
                    nEvents += 1
                if in_event:
                    output_file.write(line)
                if "</event>" in line:
                    in_event = False

    # Finally add the footer
    for line in output_footer:
        output_file.write(line)

logger.info("Wrote {0} events to {1}".format(nEvents, args.output_file))
