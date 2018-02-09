#!/usr/bin/python
from __future__ import print_function

import markovify
import re
import io
import sys, getopt
import spacy

import fnmatch
import json
import random
import os

current_file_path = os.path.abspath(__file__)
input_directory = os.path.split(current_file_path)[0] + "/input/"
scripts_directory = os.path.split(current_file_path)[0] + "/generated/"

# Spacy
import author

state_size = 2

if __name__ == "__main__":

    def find(pattern, path):
            """
            Finds the *first* instance of a file name in a single directory.
            :param pattern: str, file name pattern to search for
            :param path:    str, path to search
            :return:        list of str or empty list, any matching file name ends up in the list
            """
            result = []
            files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
            for file in files:
                if fnmatch.fnmatch(file, pattern):
                    result.append(file)
                    break
            return result

    def main(argv):
        spacy_language = 'it';
        try:
            opts, args = getopt.getopt(argv,"hl:",["language="])
        except getopt.GetoptError:
            print('generate.py -l it')
            sys.exit(2)
        for opt, arg in opts:
            if opt == '-h':
                print('generate.py -l <language code for spacy>')
                sys.exit()
            elif opt in ("-l", "--language"):
                spacy_language = arg
        print("Spacy set to {} language;".format(spacy_language))
        print("--------------------")

        for file in os.listdir( input_directory ):
            if file.endswith(".txt"):
                filename_clean = file.replace(".txt", "")
                # Check and generate json cache file
                if find(filename_clean + "_" + str(state_size) + ".json", scripts_directory):
                    print("Found:", filename_clean)
                else:
                    print("Starting cache for {};".format(filename_clean))

                    # Spacy
                    nlp = spacy.load(spacy_language)

                    text = io.open(input_directory + filename_clean + '.txt', 'r', encoding='utf-8')
                    model = author.POSifiedText(text, 2)
                    model_json = model.to_json()
                    with open(scripts_directory + filename_clean + "_" + str(state_size) + ".json", "w") as json_data:
                        json.dump(model_json, json_data, indent=4)
                    print("Generated cache for {};".format(filename_clean))

    main(sys.argv[1:])
