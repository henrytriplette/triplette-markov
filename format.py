#!/usr/bin/python
from __future__ import print_function

import re
import io
import sys, getopt

import fnmatch
import json
import random
import os

current_file_path = os.path.abspath(__file__)
input_directory = os.path.split(current_file_path)[0] + "/input/"
format_directory = os.path.split(current_file_path)[0] + "/formatted/"

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
        autor_to_format = False
        try:
            opts, args = getopt.getopt(argv,"ha:",["author="])
        except getopt.GetoptError:
            print('format.py -a lovecraft')
            sys.exit(2)
        for opt, arg in opts:
            if opt == '-h':
                print('generate.py -l <language code for spacy> -d <depth, int>')
                sys.exit()
            elif opt in ("-a", "--author"):
                autor_to_format = arg
                print("Formatting author: {}.txt;".format(autor_to_format))
        print("--------------------")

        if not autor_to_format:
            sys.exit('No author specified')

        if find(autor_to_format + ".txt", input_directory):
            print("Found:", autor_to_format)

            text = io.open(input_directory + autor_to_format + '.txt', 'r', encoding='utf-8')
            print(text)
        else:
            sys.exit('No author found in input directory')

    main(sys.argv[1:])
