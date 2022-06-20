import argparse
import requests
import datetime
import os
import numpy as np
import csv

# Array to hold formation data from geolex
formations = []

# Get Current Date
today = datetime.datetime.now()

# Convert date to string for filenaming purposes
dt = today.strftime("%Y%m%d_%H%M%S")

# Get User Input Parameters
parser = argparse.ArgumentParser(description='Enter Range of Formation Identifiers (left - right')
parser.add_argument('-left', '--leftBound', help='Left (Minimum) Bound', required=True)
parser.add_argument('-right', '--rightBound', help='Right (Maximum) Record Bound', required=True)
parser.add_argument('-verbose', '--verbose', help='Verbose script execution using true/false (default false)', required=True, default="false")
args = parser.parse_args()
leftBound = args.leftBound
rightBound = args.rightBound
verboseoutput = args.verbose.lower().strip()
requestrange = leftBound + '-' + rightBound

# Set CSV Files
dirname = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(dirname, 'output')
rawfile = path + '/' + 'raw_' + requestrange + '_' + dt + '.csv'
parsedfile = path + '/' + 'parsed_' + requestrange + '_' + dt + '.csv'


# Create parsed csv file from raw data
def remove_array_chars():

    data = ""
    with open(rawfile) as file:
        data = file.read().replace(",[\'", ",").replace("\'],", ",").replace("\', \'", ", ").replace("[]", "").replace(",\"[\'",",\"").replace("\']\",","\",")

    with open(parsedfile, "w", encoding='utf-8') as file:
        file.write(data)


# Get data from API
def get_formations(record):

    formationid = str(record)

    url = "https://ngmdb.usgs.gov/connect/apiv1/geolex/units/"+formationid+"/"
    if verboseoutput == "true":
        print('Getting results for ' + url)

    r = requests.get(url)
    response = r.json()

    locations = []
    usages = []
    record = []

    # Check if record exists, if not then populate specific results array
    if 'detail' in response:
        record = ['', '', '', '', '', formationid, url]
        return record

    else:
        # JSON Parameters
        # Assign specific parameters from the API response to variables to populate results array
        name = response['name']

        # First check if json array is empty, then set variable to empty or populate
        if len(response['usages']) == 0:
            locations = ""
        else:
            locations = response['usages'][0]['states']

        # First check if json array is empty, then set variable to empty or populate
        if len(response['unit_reference_summaries']) == 0:
            lithology = ""
        else:
            lithology = response['unit_reference_summaries'][0]['lithology']

        age = response['age_description'][0]

        for usage in response['usages']:
            usages = [usage['usage']]

        # Create results array
        record = [name, age, usages, locations, lithology, formationid, url]
        if verboseoutput == "true":
            print(record)

        return record


# Write data returned from request to raw csv file
def create_raw(first, last):

    # Clear existing data
    # clear_csv()

    # Setup raw csv file
    data_file = open(rawfile, 'w', newline='', encoding='utf-8')
    writer = csv.writer(data_file)

    # Write Header Row
    writer.writerow(["prefLabel", "age", "altLabels", "states", "lithology", "formationId", "source"])

    # Create empty array
    formationlist = []

    # Write array to file
    for i in np.arange(int(first), int(last), 1):
        formationlist.append(get_formations(i))
        writer.writerow(get_formations(i))
    # Close file
    data_file.close()

    # Create parsed data file from raw data
    remove_array_chars()


# Run Script using User Input
create_raw(leftBound, rightBound)


