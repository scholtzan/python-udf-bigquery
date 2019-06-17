#!/usr/bin/env python3

"""
This script prepares micropython to be used in BigQuery UDF by splitting
the firmware.wasm file into different javascript files containing the 
bytes. Optionally, a python file can be provided whose source code
will be used for the UDF. Also all files can get automatically pushed
into a Google cloud storage bucket. The output of running this script
is a query that can be copied and executed in BigQuery.
"""

from argparse import ArgumentParser
import os, sys


parser = ArgumentParser(description=__doc__)
parser.add_argument(
    "--input-js",
    default="build/micropython.js",
    help="The JavaScript file to be used in BigQuery UDF.",
)
parser.add_argument(
    "--input-wasm",
    default="build/firmware.wasm",
    help="The WebAssembly file to be used in BigQuery UDF.",
)
parser.add_argument(
    "--out-dir",
    default="build/",
    help="The path to the local directory generated files are written to.",
)
parser.add_argument(
    "--gcs",
    default="",
    help="The bucket and path in Google Cloud storage where the micropython should be uploaded to.",
)
parser.add_argument(
    "--python-file",
    default="*",
    help="Path to file whose code should be used in the generated UDF.",
)


def split_wasm_files(filepath, outdir):



def main():
    args = parser.parse_args()



    gcs_path = "gc://path/in/gcs"




if __name__ == "__main__":
    main()
