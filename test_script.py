import os
import sys

# Simple test script to verify file writing
output_file = 'demo.md'

# Create/clear the file
with open(output_file, 'w') as f:
    f.write('# Test Output File\n\nThis is a test to verify file writing works.\n')

print(f'File created at: {os.path.abspath(output_file)}')
print(f'Current working directory: {os.getcwd()}')