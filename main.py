import argparse
import requests
import datetime
import os
import csv
import time


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


# Get data from API
def get_formations(record):

    formationid = str(record)

    url = "https://ngmdb.usgs.gov/connect/apiv1/geolex/units/"+formationid+"/"
    if verboseoutput == "true":
        print('Getting results for ' + url)

    r = requests.get(url)
    response = r.json()

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
            locations = ', '.join(response['usages'][0]['states'])

        # First check if json array is empty, then set variable to empty or populate
        if len(response['unit_reference_summaries']) == 0:
            lithology = ""
        else:
            lithology = ', '.join(response['unit_reference_summaries'][0]['lithology'])

        age = response['age_description'][0]

        for usage in response['usages']:
            usages = usage['usage']

        # Create results array
        record = [name, age, usages, locations, lithology, formationid, url]
        if verboseoutput == "true":
            print(record)

        return record


# Write data returned from request to raw csv file
def create_raw(first, last):
    # Setup raw csv file
    data_file = open(parsedfile, 'w', newline='', encoding='utf-8')
    writer = csv.writer(data_file)

    # Write Header Row
    writer.writerow(["prefLabel", "age", "altLabels", "states", "lithology", "formationId", "source"])

    # Write array to file
    for i in range(int(first), int(last) + 1, 1):
        # pause between iterations to avoid too many requests to the API
        time.sleep(.25)
        writer.writerow(get_formations(i))

    # Close file
    data_file.close()


# Run Script using User Input
create_raw(leftBound, rightBound)


