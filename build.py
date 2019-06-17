#!/usr/bin/env python3

"""
This script prepares micropython to be used in BigQuery UDF by splitting
the firmware.wasm file into different javascript files containing the 
bytes.
"""

from argparse import ArgumentParser
import os
import sys
import struct

parser = ArgumentParser(description=__doc__)
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
    "--max-size",
    default="670000",
    help="The approximate maximum size of the generated files in bytes.",
)


def split_wasm(filepath, outdir, max_size):
    with open(filepath, "rb") as f:
        byte = f.read(1)
        formatted_byte = int.from_bytes(byte, byteorder=sys.byteorder)
        part = 0
        output_file = outdir + "part" + str(part) + ".js"

        with open(output_file, "a") as out:
            out.write("const part{}=[{}".format(part, formatted_byte))

        total_bytes_written = 14    

        byte = f.read(1)
        formatted_byte = int.from_bytes(byte, byteorder=sys.byteorder)

        while byte:
            if total_bytes_written >= max_size:
                with open(output_file, "a") as out:
                    out.write("];")

                total_bytes_written = 0
                part += 1
                output_file = outdir + "part" + str(part) + ".js"

                with open(output_file, "a") as out:
                    out.write("const part{}=[{}".format(part, formatted_byte))
                    
                total_bytes_written += 14
            else:
                with open(output_file, "a") as out:
                    out.write(",{}".format(formatted_byte))

                total_bytes_written += 2

            byte = f.read(1)
            formatted_byte = int.from_bytes(byte, byteorder=sys.byteorder)

        with open(output_file, "a") as out:
            out.write("];".format(formatted_byte))  


def main():
    args = parser.parse_args()
    split_wasm(args.input_wasm, args.out_dir, int(args.max_size))


if __name__ == "__main__":
    main()
