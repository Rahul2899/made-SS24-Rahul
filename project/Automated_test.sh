# Removing Existing Files
echo "Starting Tests"
echo "Installing pre-requisit lib"
pip install pandas pysqlite3

echo "------------------------"

echo "running system test."
python ./Automated_test.py

# Check the return value of system_test.sh
if [ $? -ne 0 ]; then
    echo "System Test failed."
    exit 1
fi
