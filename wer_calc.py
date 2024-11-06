#!/usr/bin/env python3

import sys
import glob
import os
import werpy
import csv

# script matches reference and generated text files on filename
# (i.e. it assumes that reference and generated files have the same filename)

# sys.argv = ['wer_calc.py', '[path/to/reference-directory]', '[path/to/generated-directory]', '[path/to/output.csv]']


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

if os.path.splitext(sys.argv[3])[1] == "":
    print("Error: %s is not a valid file." % sys.argv[3])
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
print("Checking for output file...")
if not os.path.exists(outputFile):
    with open(outputFile, 'w') as outFile:
        outWriter = csv.writer(outFile, delimiter=',', lineterminator='\n')
        header = ['Reference','Generated','WER']
        outWriter.writerow(header)
else:
    while True:
        print("Output file %s already exists\nDo you want to overwrite? (y/n)" % outputFile)
        userDecide = input()
        if userDecide == "n":
            sys.exit("Exiting")
        elif userDecide == "y":
            print("Overwriting file %s" % outputFile)
            break

with open(outputFile, 'w') as outFile:
    outWriter = csv.writer(outFile, delimiter=',', lineterminator='\n')
    header = ['Reference','Generated','WER']
    outWriter.writerow(header)


# calculate WER for each pair of files
for filename in glob.glob(refDir + '/*.txt'):
    origFile = os.path.basename(filename)
    genPath = os.path.join(genDir, origFile)
    genFile = os.path.basename(genPath)
    
    with open(filename, 'r') as editedFile:
        reference = editedFile.read()
        input_ref = reference
        refNormal = werpy.normalize(input_ref)
    
    with open(genPath, 'r') as rawFile:
        generated = rawFile.read()
        input_gen = generated
        genNormal = werpy.normalize(input_gen)
        wers = werpy.wers(refNormal, genNormal)
        werString = str(wers)
        line = [origFile, genFile, werString]

# write WER result to output file
    with open(outputFile, 'a') as outFile:
        outWriter = csv.writer(outFile, delimiter=',', lineterminator='\n')
        outWriter.writerows([line])
            
    print('Reference: ' + origFile + ', Generated: ' + genFile + ', WER: ' + werString)

print('Done')