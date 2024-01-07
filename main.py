import subprocess
import re

# Define the command to run
command = ["speedtest-cli", "--secure"]

# Run the command and capture the output
result = subprocess.run(command, stdout=subprocess.PIPE, text=True)

# Print the command output
print("Command Output:")
print(result.stdout)

# Use a regular expression to find all numbers in the output
numbers = re.findall(r'\b\d+\b', result.stdout)

# Print the numbers
print("Numbers found in the output:")
print(numbers)
