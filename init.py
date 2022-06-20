# Setup project
import os

# Get Current Path
dirname = os.path.dirname(os.path.abspath(__file__))
print("Current directory: " + dirname)
# Create output directory to store csv files
path = os.path.join(dirname, 'output')

# Check if directory already exists
isExist = os.path.exists(path)
if not isExist:
    # Create a new directory because it does not exist
    os.makedirs(path)
    print("output directory " + path + " is created!")


print("Initialization Complete")