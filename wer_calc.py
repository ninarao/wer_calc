#!/usr/bin/env python3

import sys
import os
import werpy
import pandas as pd
import re

# script matches reference and generated files via csv
# reference and generated files must be srt or txt

# sys.argv = ['wer_calc.py', '[path/to/reference-directory]', '[path/to/generated-directory]', '[path/to/output.csv]']

print("This script matches reference and generated files via csv file.")
print("Reference and generated files must be .srt, .vtt, or .txt")

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


def srt_to_txt(file_path):
    just_read_interval = False
    output_line = ""
    with open(file_path, 'r', encoding="utf8") as srt_file:
        txt_version = ""
        for line in srt_file:
            # if line consists of single integer ==> sequence number
            if re.match(r'^\d+\n$', line):
                just_read_interval = False
            # if line consists of time interval ==> subtitle timing
            if re.match(r'^\d{2,}:[0-5][0-9]:[0-5][0-9],\d{3} --> \d{2,}:[0-5][0-9]:[0-5][0-9],\d{3}\n$', line):
                just_read_interval = True
            # if time interval was just read, current line is subtile text
            # or space between subtitle timing block  ==> write line to text file
            elif just_read_interval:
                output_line = line
                txt_version += output_line
        return txt_version                

def vtt_to_txt(file_path):
    just_read_interval = False
    output_line = ""
    with open(file_path, 'r', encoding="utf8") as vtt_file:    
        txt_version = ""
        for line in vtt_file:
            # if line consists of time interval ==> subtitle timing
            if re.match(r'^\d{2,}:[0-5][0-9]:[0-5][0-9].\d{3} --> \d{2,}:[0-5][0-9]:[0-5][0-9].\d{3}\n$', line) or re.match(r'[0-5][0-9]:[0-5][0-9].\d{3} --> [0-5][0-9]:[0-5][0-9].\d{3}\n$', line):
                just_read_interval = True
            # if time interval was just read, current line is subtile text
            # or space between subtitle timing block  ==> write line to text file
            elif just_read_interval:
                output_line = line
                txt_version += output_line
            # if line consists of single integer ==> sequence number
            elif re.search(r'^$', line, re.MULTILINE):
                just_read_interval = False
        return txt_version
    
def check_srt(dir:str, filename_float:str):
    """
    Checks whether a transcript file is in TXT, SRT, or VTT format.
    If the file is in TXT format, returns the data unchanged. 
    If the file is in SRT or VTT format, calls srt_to_txt or vtt_to_txt function and returns the converted data.
    """
    filename = str(filename_float)
    file_path = os.path.join(dir, filename)
    if filename.endswith('.txt')==True:
        validFormat = "Yes"
        f=open(file_path, "r", encoding="utf8")
        data = f.read()
    elif filename.endswith('.srt')==True:
        validFormat = "Yes"
        data = srt_to_txt(file_path)
    elif filename.endswith('.vtt')==True:
        validFormat = "Yes"
        data = vtt_to_txt(file_path)
    else:
        validFormat = "No"
        data = filename
    return data, validFormat

# Open the output file as a Pandas dataframe
df= pd.read_csv(outputFile, dtype="str")
for index, row in df.iterrows():
    # Run check_srt function on both reference and generated files
    reference_data, validFormat = check_srt(refDir, row["Reference"])
    if validFormat == "No":
        print(f'Row contains a file {reference_data} that is not the right format; skipping row.')
    generated_data, validFormat = check_srt(genDir, row["Generated"])
    if validFormat == "No":
        print(f'Row contains a file {generated_data} that is not the right format; skipping row.')
    else:
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
        # Calculate WER from reference and generated data and write to output file
                    wers = werpy.wers(refNormal, genNormal)
                    werString = str(wers)
                    row["WER"]=werString
                    print(werString)
                    df.to_csv(outputFile, index=False)
                    break
        else:
            wers = werpy.wers(refNormal, genNormal)
            werString = str(wers)
            row["WER"]=werString
            print(werString)
            df.to_csv(outputFile, index=False)

print('Done')
