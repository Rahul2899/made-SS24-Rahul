#!/bin/bash

# Removing Existing Files
echo "Starting Tests"
echo "Installing pre-requisite libraries"
pip install pandas pysqlite3

echo "------------------------"

echo "Running system tests."
python ./Automated_test.py

# Check the return value of the test script
if [ $? -ne 0 ]; then
    echo "System Test failed."
    exit 1
fi
