#!/usr/bin/env python3

import sys
import glob
import os
import werpy
import csv
import pandas as pd

# script matches reference and generated files via csv
# reference and generated files must be srt or txt

# sys.argv = ['wer_calc.py', '[path/to/reference-directory]', '[path/to/generated-directory]', '[path/to/output.csv]']

print("This script matches reference and generated files via csv file.")
print("Reference and generated files must be .srt or .txt")

# check that command has reference folder location, generated folder location,
# and output file location
if len(sys.argv) != 4:
    print("Usage: python wer_calc.py [path/to/reference-directory] [path/to/generated-directory] [path/to/output.csv]")
    sys.exit(1)

if not os.path.isdir(sys.argv[1]):
    print("Error: %s is not a valid directory." % sys.argv[1])
    print("Usage: python wer_calc.py [path/to/reference-directory] [path/to/generated-directory] [path/to/output.csv]")
    sys.exit(1)
    
if not os.path.isdir(sys.argv[2]):
    print("Error: %s is not a valid directory." % sys.argv[2])
    print("Usage: python wer_calc.py [path/to/reference-directory] [path/to/generated-directory] [path/to/output.csv]")
    sys.exit(1)

if os.path.splitext(sys.argv[3])[1] == "" or os.path.splitext(sys.argv[3])[1] != ".csv":
    print("Error: %s is not a valid file. Must be csv file." % sys.argv[3])
    print("Usage: python wer_calc.py [path/to/reference-directory] [path/to/generated-directory] [path/to/output.csv]")
    sys.exit(1)

arg1 = sys.argv[1]
arg2 = sys.argv[2]
arg3 = sys.argv[3]

print('Reference folder:',arg1)
print('Generated folder:',arg2)
print('Output file:',arg3)

refDir = arg1
genDir = arg2
outputFile = arg3


# check for existing output file
# if none exists, create
# if output file exists, ask whether to exit or overwrite

# print("Checking for output file...")
# if not os.path.exists(outputFile):
#     with open(outputFile, 'w') as outFile:
#         outWriter = csv.writer(outFile, delimiter=',', lineterminator='\n')
#         header = ['Reference','Generated','WER']
#         outWriter.writerow(header)
# else:
#     while True:
#         print("Output file %s already exists\nDo you want to overwrite? (y/n)" % outputFile)
#         userDecide = input()
#         if userDecide == "n":
#             sys.exit("Exiting")
#         elif userDecide == "y":
#             print("Overwriting file %s" % outputFile)
#             break

def check_srt(dir:str, filename_float:str):
    """
    Checks whether a transcript file is in TXT or SRT format. If the file is in TXT format, returns the data unchanged. If the file is in SRT format, the function converts the file to TXT and returns the converted data.
    """
    filename = str(filename_float)
    if filename.endswith('.txt')==True:
        f=open(dir+"/"+filename, "r")
        data = f.read()
    elif filename.endswith('.srt')==True:
        original_filename_noext=filename.split('.srt')[0]
        absolute_original_filepath=dir+"/"+filename
        absolute_converted_filepath=dir+"/"+original_filename_noext+"_converted.txt"
        command=f"python3 srt2text.py -s {absolute_original_filepath} -o {absolute_converted_filepath}"
        os.system(command)
        f=open(absolute_converted_filepath, "r")
        data = f.read()
        os.remove(absolute_converted_filepath) 
    return data

# Open the output file as a Pandas dataframe
df= pd.read_csv(outputFile, dtype="str")
for index, row in df.iterrows():
    # Run check_srt function on both reference and generated files
    reference_data= check_srt(refDir, row["Reference"])
    generated_data = check_srt(genDir, row["Generated"])
    refNormal = werpy.normalize(reference_data)
    genNormal = werpy.normalize(generated_data)
    # Check if WER cell is empty
    if not pd.isna(df.loc[index, 'WER']):
        while True:
            wer_cell = df.loc[index, 'WER']
            print("WER cell not empty (%s), do you want to overwrite? (y/n)" % wer_cell)
            userDecide = input()
            if userDecide == "n":
                break
            elif userDecide == "y":
                print("Overwriting WER entry")
    # Calculate WER from reference and generated data
                wers = werpy.wers(refNormal, genNormal)
                werString = str(wers)
                row["WER"]=werString
                break
    else:
        wers = werpy.wers(refNormal, genNormal)
        werString = str(wers)
        row["WER"]=werString

# Write WER to output file
df.to_csv(outputFile, index=False)

print('Done')