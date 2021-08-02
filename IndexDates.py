#!/usr/bin/python

"""This is a utility program to help anonymize dates within a dataset.  The 
concept is that the relationships between events in a clinical trial is 
important, but it creates an opportunity for patient re-identification if 
correlated with external data that includes dates and times.  This tool finds 
the earliest time in a CSV file and sets it to be equal to 1, and then 
references all of the other times based on that index time.  This retains the 
relationships between events without pinning that timeline to a specific date 
and time that can be used to re-identify patients.

NOTE: This is brittle, in that any time that is disambiguated will then expose 
the entire timeline.  Because of this, a 'fuzz' factor is specified, creating 
a random noise parameter for each value.  Please note that long periods of 
high-resolution measurements will make this approach unworkable."""

import datetime

