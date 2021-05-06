# DataTidy
Generalized Program for Validating and Changing CSV Data

This program is for validating and cleaning CSV data tables.

It takes a CSV source file and a CSV parameters file, and performs 
validation, substitution, and default values in each row, iteratively, 
until the whole file is processed.  The result is a new CSV file with 
the updated information, with a date/time in the filename.  This 
preserves the source data unchanged, and produces a reproduceable output 
file that can be tuned or compared with the source file until you are 
satisfied that the data is altered according to your needs and no data 
is ever lost.
The reason to use a parameters file instead of building it into the
program is that it can be easily read, changed, and written by researchers
who lack programming training.