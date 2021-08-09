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
import random

def interval(indexDateTime , targetDateTime , fuzzFactor):
    """Provide a datetime object for the index time, the time that needs the 
    interval after the index time measures (again, as a Python datetime 
    object), and a fuzz factor in seconds, which will be an integer defining 
    the size of the fuzzing window, in seconds."""
    intervalDays = 0
    intervalHours = 0
    intervalMinutes = 0
    intervalSeconds = 0
    ff = random.randint(0 , fuzzFactor)
    intervalSeconds = datetime.timedelta.total_seconds\
        (targetDateTime - indexDateTime) + ff
    # Here we also generate, selectively, appropriate other measures
    if (intervalSeconds > 60):
        intervalMinutes = intervalSeconds / 60
    else:
        intervalMinutes = 0
    if (intervalSeconds > 60 * 60):
        intervalHours = intervalSeconds / 60 / 60
    else:
        intervalHours = 0
    if (intervalSeconds > 60 * 60 * 24):
        intervalDays = intervalSeconds / 60 / 60 / 24
    else:
        intervalDays = 0

    i = (intervalDays , intervalHours , intervalMinutes, intervalSeconds)
    return i

