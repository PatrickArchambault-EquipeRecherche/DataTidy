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
    # format needed for consistency, returning an error if the parsing
    # fails and a default value if there is nothing in the cell.
    pass

# Start by pulling in the Parameter file.  By default this will be 
# 'parameters.csv', but should eventually be specifiable on the command 
# line.

with open('parameters.csv' , "r" , newline='') as parametersfile:
    parameterDataframe =  pandas.read_csv(parametersfile)

    # Next open the source datafile.  By default this will be 'source.csv' 
    # but should be specifiable on the command line.

    with open('source.csv' , "r" , newline='') as sourcefile:
        sourceReader = csv.reader(sourcefile)
        header = next(sourceReader)

        # Next, open the destination file.  Having all of these files 
        # open at once ensures that we break on missing or misnamed files 
        # right away, and lets use read and write only one file at a 
        # time, keeping the memory needs very low and the number of times 
        # we loop through the source file to one.

        # Use datetime.now() to give the output file a name unique to a 
        # given minute.
        myDateTimeString = datetime.datetime.now().strftime("%Y%m%d%H%M")

        with open(myDateTimeString + "tidyData.csv" , "a+" , newline='') as outputfile:
            # Create a csv object
            processedOutput = csv.writer(outputfile)
            # Finally, we create a file for rows that are outliers in some way.

            with open(myDateTimeString + "outliers.csv" , "w+" , newline='') as outlierfile:
                # Create a csv object for the outliers
                myOutliers = csv.writer(outlierfile)
                
                # Check the "New Name" row in the paramters file, and if 
                # any columns need to be renamed, do that here.
                
                parameterDataframe
                #header = [parameterDataframe.loc['New Name',i] if parameterDataframe.loc['New Name',i] else i for i in header]
                print(header)

                processedOutput.writerow(header)
                for row in sourceReader:
                    updatedRow = []
                    for cell in row:
                        updatedRow.append(cell)
                    processedOutput.writerow(row)

