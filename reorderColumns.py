#!/usr/bin/python

"""Take a header in a semi-colon-separated CSV file and some data in a CSV 
file and return a copy of the data in the order specified by the header, 
leaving extra columns blank. This is basically a way to coerce some data 
into a format where it can be imported.  Built to solve the problem of 
wanting to import a subset of data into a database without doing it in SQL 
column-by-column."""

import sys
import pandas
import csv

# Grab the source and the parameters files from the command line

if len(sys.argv) == 4:
    myDataFile = sys.argv[1]
    myHeaderFile = sys.argv[2]
    myOutputFile = sys.argv[3]
else:
    # We want hard-coded values for testing, as a fall-back.
    print("Using default values, 'someData.csv' as the data file, 'header.csv' as the header file, and 'output.csv' as the output file.\n \
        To avoid this, use:\n \
            reorderColumns.py DATAFILE HEADERFILE OUTPUTFILE")
    myDataFile = "someData.csv"
    myHeaderFile = "header.csv"
    myOutputFile = "output.py"


header = []

with open(myHeaderFile , "r" , newline='') as headerfile:
    headerReader = csv.reader(headerfile , delimiter=';')
    header = next(headerReader)

data = pandas.read_csv(myDataFile , delimiter=';')

# Create a new, empty dataframe based on the desired header
newDF = pandas.DataFrame(columns = header)
#print(newDF)
#print(newDF.columns)
#print(data.columns)

# Iterate over the columns, checking if the column in the new dataframe is in 
# the existing data, and if it is, pull in the column data.
for column in newDF.columns:
    if column in data.columns:
        #print(column)
        newDF[column] = data.loc[:,column]


#print(newDF)

# The above process adds an index column in position 0, which we drop with the
#  index = False parameter

newDF.to_csv(myOutputFile , index = False)