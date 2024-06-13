
echo "$python_script" > Automated_test.py

# Run Python script
python Automated_test.py

# Print completion message
echo "Tests completed."

# Clean up environment
echo "Cleaning up test environment..."
rm -f your_database.db
rm -f Automated_script.py
rm -rf /content/data

echo "Test environment cleaned up."
