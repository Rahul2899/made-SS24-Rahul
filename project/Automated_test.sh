#!/bin/bash

# Navigate to the project directory
cd "$(dirname "$0")"

python datapipeline.py

pytest Automated_test.py

# Capture the exit code of pytest
exit_code=$?

exit $exit_code
