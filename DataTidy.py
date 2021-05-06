#!/usr/bin/python

# This program is for validating and cleaning CSV data tables.
#
# It takes a CSV source file and a CSV parameters file, and performs 
# validation, substitution, and default values in each row, iteratively, 
# until the whole file is processed.  The result is a new CSV file with 
# the updated information, with a date/time in the filename.  This 
# preserves the source data unchanged, and produces a reproduceable output 
# file that can be tuned or compared with the source file until you are 
# satisfied that the data is altered according to your needs and no data 
# is ever lost.

# The reason to use a parameters file instead of building it into the
# program is that it can be easily read, changed, and written by researchers
# who lack programming training.

import sys
import re
import datetime
import csv
import pandas

# Following are the base validation functions

def dateCheck(myDateString):
    # Parse the date using the datetime tools, the put the date into the
    # format needed for consistency, adding an Error Value if the parsing
    # fails and a default value if there is nothing in the cell.
    pass

# Start by pulling in the Parameter file.  By default this will be 
# 'parameters.csv', but should eventually be specifiable on the command 
# line.

with open('parameters.csv', newline='') as parametersfile:
    parameterReader =  pandas.read_csv(parametersfile)

    # Next open the source datafile.  By default this will be 'source.csv' 
    # but should be specifiable on the command line.

    with open('source.csv', newline='') as sourcefile:
        sourceReader = csv.reader(sourcefile)

        # Finally, open the destination file.  Having all of these files 
        # open at once ensures that we break on missing or misnamed files 
        # right away, and lets use read and write only one file at a 
        # time, keeping the memory needs very low and the number of times 
        # we loop through the source file to one.

        # Use datetime.now() to give the output file a name unique to a 
        # given minute.
        myDateTimeString = datetime.datetime.now().strftime("%Y%m%d%H%M")

        with open(myDateTimeString + "tidyData.csv" , newline='') as outputfile:
            for row in sourceReader:
                outputfile.writerow(row)

