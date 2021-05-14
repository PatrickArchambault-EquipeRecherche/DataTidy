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
import os
import re
import datetime
import csv
import pandas
import numpy
from pandas.core.dtypes.missing import notnull

# Grab the source and the parameters files from the command line

if len(sys.argv) == 3:
    mySourceFile = sys.argv[1]
    myParameterFile = sys.argv[2]
else:
    mySourceFile = "source.csv"
    myParameterFile = "parameters.csv"

# Following are the base validation functions

def dateCheck(myDateString,baseFormat,desiredFormat):
    # Parse the date using the datetime tools, the put the date into the
    # format needed for consistency, returning an error if the parsing
    # fails.
    #print(myDateString + " " + baseFormat)
    try:
        myDate = datetime.datetime.strptime(myDateString, baseFormat)
        #print(myDate)
        cleanDate = datetime.datetime.strftime(myDate, desiredFormat)
        #print(cleanDate)

        return cleanDate
    except:
        return "Date error"

#debug print(dateCheck("23-04-2021", "%d-%m-%Y", "%Y/%m/%d"))

# Start by pulling in the Parameter file.  By default this will be 
# 'parameters.csv', but should eventually be specifiable on the command 
# line.

with open(myParameterFile , "r" , newline='') as parametersfile:
    parameterDataframe =  pandas.read_csv(parametersfile, index_col=0)

    # Next open the source datafile.  By default this will be 'source.csv' 
    # but should be specifiable on the command line.

    with open(mySourceFile , "r" , newline='') as sourcefile:
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
                
                newHeader = [parameterDataframe.at['New Name',i] if pandas.notnull(parameterDataframe.at['New Name',i]) else i for i in header]
                #print(header)

                processedOutput.writerow(newHeader)
                for row in sourceReader:
                    # We need to put the changed values into a new row.
                    # Here's the list for that:
                    updatedRow = []
                    # Set a flag for catching errors.  We can set this 
                    # lots of times, because any value over zero 
                    # triggers putting this row into the outliers file.
                    is_wrong_somehow = 0
                    
                    for i in range(len(row)):
                        # Here is where we do all of the data validation
                        # and reformatting.

                        #Set a cell variable equal to the cell we pull 
                        # from the source data, so that manipulate (or 
                        # not) that value and put it into our temporary 
                        # row

                        cell = row[i]

                        if parameterDataframe.at["Data Type" , header[i]] == "number":
                            # Canary here for number
                            #print("this is a number")

                            # If there is a base format defined, check if the data conforms and throw a flag if not
                            if pandas.notnull(parameterDataframe.at['Base Format' , header[i]]):
                                # Check if the cell conforms to the defined format
                                if re.fullmatch(parameterDataframe.at['Base Format' , header[i]] , cell):
                                    
                                    pass
                                else:
                                    #print("Error in pattern match of the base format: " + cell)
                                    is_wrong_somehow = is_wrong_somehow + 1
                            else:
                                pass
                            # If there is a desired format defined, check if the data conforms and throw a flag if not
                            if pandas.notnull(parameterDataframe.at['Desired Format' , header[i]]):
                                # Check if the cell conforms to the defined format
                                if re.fullmatch(parameterDataframe.at['Desired Format' , header[i]] , cell):
                                    
                                    pass
                                else:
                                    #print("Error in pattern match of the desired format: " + cell)
                                    is_wrong_somehow = is_wrong_somehow + 1
                            else:
                                pass
                            
                        elif parameterDataframe.at["Data Type" , header[i]] == "string":
                            pass
                        elif parameterDataframe.at["Data Type" , header[i]] == "date":
                            checkedDate = dateCheck(cell , parameterDataframe.at['Base Format' , header[i]] , parameterDataframe.at['Desired Format' , header[i]])
                            if checkedDate == "Date error":
                                #print("Error in date format: " + cell)
                                is_wrong_somehow = is_wrong_somehow +1
                            else:
                                cell = checkedDate
                        else:
                            print("This cell fell through the cracks all the way to the bottom: " + cell)
                            is_wrong_somehow = is_wrong_somehow + 1

                        updatedRow.append(cell)
                    
                    # check the error flag value, and write out the row to
                    # either the outliers file or the output file.
                    if (is_wrong_somehow > 0):
                        myOutliers.writerow(row)
                    else:
                        processedOutput.writerow(updatedRow)

            # Cleanup code - if the outliers file is empty, delete it
            if os.path.exists(outlierfile.name) and os.stat(outlierfile.name).st_size == 0:
                os.remove(outlierfile.name)

