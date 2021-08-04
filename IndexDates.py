#!/usr/bin/python

"""This is a utility program to help anonymize dates within a dataset.  The 
concept is that the relationships between events in a clinical trial are 
important, but it creates an opportunity for patient re-identification if 
correlated with external data that includes dates and times.  This tool finds 
the earliest time in a CSV file and then references all of the other times 
based on that index time.  This retains the relationships between events 
without pinning that timeline to a specific date and time that can be used 
to re-identify patients.

NOTE: This is brittle, in that any time that is disambiguated will then expose 
the entire timeline.  Because of this, a 'fuzz' factor is specified, creating 
a random noise parameter for each value.  Please note that long periods of 
high-resolution measurements will make this approach unworkable."""

import datetime
import csv

# This is an example from a recent project, to test string parsing, index
# creation, etc.

example_string_1 = "2021-02-08 20:29:00.000"
example_string_2 = "2021-02-08 20:30:00.000"
# The milliseconds are never present, and they need reformatting to match the 
# %f in the datetime module, which is microseconds (zero-padded millionths of 
# a second, so 000000, 000001, etc.)
#print(example_string[:-4])
example_dt_1 = datetime.datetime.strptime(example_string_1[:-4] , "%Y-%m-%d %H:%M:%S")
example_dt_2 = datetime.datetime.strptime(example_string_2[:-4] , "%Y-%m-%d %H:%M:%S")
#print(example_dt)
myarray = [example_dt_1,example_dt_2]
print(sorted(myarray))

for a in myarray:
    print(a - myarray[0])
    print(datetime.timedelta.total_seconds(a - myarray[0]))

bigarray = []
with open("datetimes.csv") as csvdata:
    bigarray = csvdata.readlines()

print(len(bigarray))

bigarray = sorted(bigarray)

diffarray = []

print(bigarray[0])
print(bigarray[0][:-5])
myindex = datetime.datetime.strptime(bigarray[0][:-5] , "%Y-%m-%d %H:%M:%S")
print(myindex)
count = 0
for a in bigarray:
    count = count + 1
    if len(a) != 24:
        diffarray.append([a , "oopsie"])
        # print("Line " + str(count) + ": [" + a + "]")
    else:
        difference = datetime.timedelta.total_seconds(datetime.datetime.strptime(a[:-5] , "%Y-%m-%d %H:%M:%S") - myindex)
        
        diffarray.append([a[:-1] , difference, difference / 60, difference / (60 * 60), difference / (60 * 60 * 24)])

print(len(diffarray))

with open("blah.csv" , "w+") as out:
    csvwriter = csv.writer(out, delimiter=",")
    header = ["datetime","seconds","minutes","hours","days"]
    csvwriter.writerow(header)
    csvwriter.writerows(diffarray)
