# HarvestGeolex
## Harvest formation data from the National Geologic Map Database API

### Overview
The script generates a set of timestamped CSV files populated with specific parameters from the JSON response bodies of the GeoLex API. Each row corresponds to an API request and a specific formation in the GeoLex database. The raw CSV file is populated directly from the JSON response (including JSON arrays nomenclature). The parsed file attempts to remove specific JSON structures from the results to make further processing easier. The find and replace strings are provided below (Parse Strings).
The user is required to specify the range of records to query by entering a minimum record ID (leftBound) and maximum record ID (rightBound) when running the main script (main.py). An additional option controls whether or not to display verbose execution of script. The default is false. 

Note: Converting a complex JSON structure with nested objects and arrays to a flat CSV file is not a clean process. In order to do so, compromises are necessary. Therefore, some post-processing will be necessary after CSV files are generated (even for the parsed CSV) for further reuse.

### Procedure
This procedure assumes you have python 3.x already installed on your computer 
and the proper PATH environmental variables are set.
1. Clone the GitHub repo or download the zip and extract the contents to a local folder. The examples below assume you cloned or extracted the repo to: C:\HarvestGeolex-main
2. Open the cmd prompt and navigate to the folder where cloned the Github repo (using example)
```console
C:\>cd C:\HarvestGeolex-main
```
3. Create a virtual environment (venv)
```console
C:\HarvestGeolex-main>python -m venv venv
```
3. Activate the virtual environment
```console
C:\HarvestGeolex-main>.\venv\Scripts\activate
```
4. Install packages
```console
(venv) C:\HarvestGeolex-main>pip install pandas numpy requests argparse
```
4. Run init.py 
```console
(venv) C:\HarvestGeolex-main>python init.py
```
5. Run main.py with the leftBound, rightBound, and verbose parameters set (Example: python main.py --leftBound=1000 --rightBound=1010 --verbose=true). Maximum (as of 20220620): 16641  
```console
(venv) C:\HarvestGeolex-main>python main.py --leftBound=1 --rightBound=10 --verbose=true  
```
If successful, the output directory will contain two new timestamped CSV files 

### JSON Parameters
JSON Parameters may be customized in the main.py file. To do so, make sure you do the following:  
1. Add the parameter to the header array (Write Header Row, line 114)
2. Set a variable to the response JSON object (JSON Parameters, lines 74 - 96)
3. Add the variable to the results array (Create results array, line 98)
 
### Examples
Example JSON Response from Geolex API: examples/sample-response.json  
Example Raw CSV File (Range: 1 - 10): raw_1-10_20220620_143111.csv  
Example Parsed CSV File (Range: 1 - 10): parsed_1-10_20220620_143111.csv


API Root: https://ngmdb.usgs.gov/connect/apiv1/geolex/units
API Request URL https://ngmdb.usgs.gov/connect/apiv1/geolex/units/{id} where {id} is a numerical identifier for a unit/formation

### Requirements
Python 3.x
Packages: Pandas and Numpy

Created with PyCharm and Python 3.10 on Windows 10


### Parse Strings
Original String, New String (enclosed in double quotation marks)*

| Old String | New String |
| --- | --- |
| ",['" | "," |
| "']," | "," |
| "', '" | ", " |
| "[]" | "" |
| ","['" | ","" |
| "']"," | ""," |

_* Escape characters were removed_


### Contact
Ben Norton
Head of Technology, Data Curator, and Collections Manager of Mineralogy
North Carolina Museum of Natural Sciences
ben.norton@naturalsciences.org
https://naturalsciences.org/staff/ben-norton

#### Last Updated: 20220620