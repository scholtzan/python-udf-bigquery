#!/usr/bin/env python3

"""
This script generates the UDF which uses Micropython to be used in BigQuery. 
Supporting files can optionally be automatically pushed into a specified
Google Cloud Storage bucket. A Python file can be provided whose code will
be used used in the generated UDF.
"""

from argparse import ArgumentParser
import os
import sys
import struct
from gcloud import storage


parser = ArgumentParser(description=__doc__)
parser.add_argument(
    "--input",
    default="build/part0.js build/part1.js build/micropython.js",
    nargs="+",
    help="The JavaScript files to be used in BigQuery UDF.",
)
parser.add_argument(
    "--gcs-bucket",
    default="",
    required=False,
    help="The bucket in Google Cloud storage where the micropython should be uploaded to.",
)
parser.add_argument(
    "--gcs-path",
    default="",
    required=False,
    help="The path in Google Cloud storage where the micropython should be uploaded to.",
)
parser.add_argument(
    "--python-file",
    default="*",
    required=False,
    help="Path to file whose code should be used in the generated UDF.",
)


def push_files_to_gcs(gcs_bucket, gcs_path, files):
    """
    Automatically push provided files to Google cloud storage.
    """
    client = storage.Client()
    bucket = client.get_bucket(gcs_bucket)

    for file in files:
        filename = os.path.basename(file)
        blob = bucket.blob(gcs_path + filename)
        blob.upload_from_filename(file)


def generate_udf(gcs_bucket, gcs_path, python_file, files):
    """
    Generates and exemplary UDF that integrates Micropython.
    """
    python = ""

    if python_file != "*":
        with open(python_file, "r") as file:
            python = file.read()

    external_files = ",\n".join(list(map(
        lambda f: 'library = "gs://{}/{}{}"'.format(
            gcs_bucket, gcs_path, os.path.basename(f)
        ),
        files,
    )))

    return """
CREATE TEMP FUNCTION
udf_func()
RETURNS STRING
LANGUAGE js AS \"\"\"
    mp_js_init(64 * 1024);
    const pythonCode = `{}`;
    return mp_js_exec_str(pythonCode);
\"\"\"
OPTIONS (
{});
SELECT
    udf_func()
FROM (
SELECT
1 x,
2 y)
    """.format(
        python, external_files
    )


def main():
    args = parser.parse_args()
    gcs_bucket = "bucket-name"

    if args.gcs_bucket != "":
        push_files_to_gcs(args.gcs_bucket, args.gcs_path, args.input)
        gcs_bucket = args.gcs_bucket

    print(
        generate_udf(gcs_bucket, args.gcs_path, args.python_file, args.input.split(" "))
    )


if __name__ == "__main__":
    main()
