echo "Running Tests.."

python ./Automated_test.py

# Check the return value of the test script
if [ $? -ne 0 ]; then
    echo "System Test failed..."
    exit 1
fi
