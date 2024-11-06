# wer_calc
Python script that performs word error rate (WER) calculation for a set of reference and generated text files and outputs results to csv.

## Usage
```
python wer_calc.py [path/to/reference-directory] [path/to/generated-directory] [path/to/output.csv]
```

## Requirements
The script matches reference files with generated files on filename, so files in reference directory must have the same name as files in the generated directory.

It also requires that files are text ('.txt').  To run the script on caption or subtitle files, first use something like [srt2text](https://github.com/yumstar/srt2text/) to remove timing information and convert files to .txt.

Before running this script, install [werpy](https://github.com/analyticsinmotion/werpy/blob/main/README.md): `pip install werpy` or `pip3 install werpy`

This script relies on `werpy` to do the following:
- preprocess/normalize input text to remove punctuation, remove duplicated spaces, leading/trailing blanks and convert all words to lowercase
- calculate word error rate (WER) for each of the reference and hypothesis texts

## Licensing
This script is created with an [MIT license](LICENSE).

werpy is released under the terms of the BSD 3-Clause License. Please refer to its [LICENSE](https://github.com/analyticsinmotion/werpy/blob/main/LICENSE) file for full details.

werpy also includes third-party packages distributed under the BSD-3-Clause license (NumPy, Pandas) and the Apache License 2.0 (Cython).  The full NumPy, Pandas and Cython licenses can be found in the werpy [LICENSES](https://github.com/analyticsinmotion/werpy/tree/main/LICENSES) directory.  They can also be found directly in the following source codes:
  - NumPy - [https://github.com/numpy/numpy/blob/main/LICENSE.txt](https://github.com/numpy/numpy/blob/main/LICENSE.txt)
  - Pandas - [https://github.com/pandas-dev/pandas/blob/main/LICENSE](https://github.com/pandas-dev/pandas/blob/main/LICENSE)
  - Cython - [https://github.com/cython/cython/blob/master/LICENSE.txt](https://github.com/cython/cython/blob/master/LICENSE.txt)
