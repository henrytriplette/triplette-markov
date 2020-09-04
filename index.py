#!/usr/bin/python
from __future__ import print_function

import markovify
import os
import re
import sys, getopt
import random
import datetime

import author

# List of paths used by the generator
current_file_path = os.path.abspath(__file__)
scripts_directory = os.path.split(current_file_path)[0] + "/generated/"
input_directory = os.path.split(current_file_path)[0] + "/input/"
output_directory = os.path.split(current_file_path)[0] + "/output/"

# Date for filename save
date_string = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

if __name__ == "__main__":

    def get_sentences(n, text_model):
        string = ''

        # use the default_num for sentences if not specified
        sentence_num = int(n) if n is not None else default_num;

        # generate the appropriate num of sentences
        for i in range(sentence_num):
            sentence = text_model.make_sentence()
            if sentence is not None:
                string += sentence

        # clean the resulting string
        clean_str = re.sub(r'\.([A-Z]|[a-z]|<)', r'. \1', string)

        # slightly better format
        clean_str = clean_str.replace(" , ", ", ")
        clean_str = clean_str.replace(" . ", ".\n")
        clean_str = clean_str.replace(" ; ", ";\n")

        clean_str = clean_str.replace(" ?", "?\n")
        clean_str = clean_str.replace(" !", "!\n")

        return clean_str

    def main(argv):
        input_state_size = 2;
        output_lenght = 5;
        output_total = 5;
        output_file = False
        try:
            opts, args = getopt.getopt(argv,"hd:l:t:o:",["depth=","length=","total=","output="])
        except getopt.GetoptError:
            print('index.py -d 2 -l 5 -t 5 -o output')
            sys.exit(2)
        for opt, arg in opts:
            if opt == '-h':
                print('index.py -d <depth> -l <lenght of rows> -t <total texts> -o <output-filename>')
                sys.exit()
            elif opt in ("-d", "--depth"):
                input_state_size = int(arg)
            elif opt in ("-l", "--length"):
                output_lenght = int(arg)
            elif opt in ("-t", "--total"):
                output_total = int(arg)
            elif opt in ("-o", "--output"):
                output_file = arg
        print("Printing {} sentences to single textblock;".format(output_lenght))
        print("Will create {} textblock;".format(output_total))
        if output_file != False:
            print("Saving into {}.txt;".format(output_file + "-" + date_string))
        print("--------------------")

        # Load authors in generated
        authors = {}
        author_available = []
        for file in os.listdir( scripts_directory ):
            if file.endswith("_" + str(input_state_size) + ".json"):
                filename_clean = file.replace(".json", "")
                #remove last part from author name
                filename_clean = filename_clean[:-2]
                # filename_author = author.Author(filename_clean, input_state_size)
                if filename_clean != False:
                    print("- Found {} author;".format(filename_clean + " " + str(input_state_size)))
                    # authors[filename_clean] = filename_author
                    author_available.append(filename_clean)

        author_selected = []
        author_choose = ""

        while author_choose != "run":
            author_choose = input("Insert author name or run to proceed: ")
            if author_choose in author_available:
                author_record = {}
                author_record['name'] = author_choose
                author_record['weight'] = int( input("Set weight: "))
                author_selected.append(author_record)

                # Load only selected authors when requested
                filename_author = author.Author(author_choose, input_state_size)
                if filename_author != False:
                    print("- Loaded {}: {} state size, {} weight;".format(author_choose,str(input_state_size),str(author_record['weight'])))
                    authors[author_choose] = filename_author

                print("Currently selected:")
                print(author_selected)
            elif author_choose in ("run", "RUN"):
                print("--------------------")
            else:
                print("That is not a valid input. Please choose between:")
                print(author_available)



        # Build the model by splitting the dictionary into two separated lists.
        author_tocombine = []
        author_toweight = []
        author_filename = ""
        for author_toload in author_selected:
            print(author_toload)
            name = author_toload['name']
            weight = int(author_toload['weight'])
            if authors[name].model:
                author_tocombine.append(authors[name].model)
                author_toweight.append(weight)
                author_filename = author_filename + "_" + name

        # Combine the two or more authors and their weight
        text_model = markovify.combine(author_tocombine, author_toweight)

        # Print/save five randomly-generated sentences
        if output_file != False:
            f = open( output_directory + output_file + "-" + author_filename + "-" + date_string + ".txt", 'a')
            f.truncate()
            for i in range(output_total):
                text = get_sentences(output_lenght, text_model)
                print(text)
                print("--------------------")
                f.write(text + '\n\n')
        else:
            for i in range(output_total):
                text = get_sentences(output_lenght, text_model)
                print(text)
                print("--------------------")

    main(sys.argv[1:])
