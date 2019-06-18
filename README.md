# User-Defined Functions with Python in BigQuery

* background, limitations of BigQuery, idea, helper scripts, prrof-of-concept


## Usage

The `udf.py` script automatically generates a skeleton UDF function using Micropython. Optionally, it allows to provide a Google Storage location where supporting files can automatically get uploaded. For this it is necessary to have write permissions in the bucket and to export `GOOGLE_APPLICATION_CREDENTIALS`.

```
$ python3 udf.py --help                                                                                                                                                                                                 
usage: udf.py [-h] [--input INPUT [INPUT ...]] [--gcs-bucket GCS_BUCKET]
              [--gcs-path GCS_PATH] [--python-file PYTHON_FILE]

This script generates the UDF which uses Micropython to be used in BigQuery.
Supporting files can optionally be automatically pushed into a specified
Google Cloud Storage bucket. A Python file can be provided whose code will be
used used in the generated UDF.

optional arguments:
  -h, --help            show this help message and exit
  --input INPUT [INPUT ...]
                        The JavaScript files to be used in BigQuery UDF.
  --gcs-bucket GCS_BUCKET
                        The bucket in Google Cloud storage where the
                        micropython should be uploaded to.
  --gcs-path GCS_PATH   The path in Google Cloud storage where the micropython
                        should be uploaded to.
  --python-file PYTHON_FILE
                        Path to file whose code should be used in the
                        generated UDF.
```


## Build from Scratch 

To generate all the JavaScript files for using Micropython in BigQuery, [Python 3](https://www.python.org/downloads/) and [emscripten](https://emscripten.org/docs/getting_started/downloads.html) needs to be installed. Run `make` to start the build process.

To use a newer version of Micropython, update the commit hash in `Makefile`. This will most likely break applying the changes in `micropython.patch`, so these changes need to be adjusted for newer versions.

Generated files will be written to `build/`
