#!/usr/bin/python
from __future__ import print_function

import markovify
import os
import re
import sys, getopt

import author

current_file_path = os.path.abspath(__file__)
scripts_directory = os.path.split(current_file_path)[0] + "/generated/"
output_directory = os.path.split(current_file_path)[0] + "/output/"

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
        clean_str = clean_str.replace(" . ", ". ")
        clean_str = clean_str.replace(" ; ", "; ")
        return clean_str

    def main(argv):
        output_lenght = 5;
        output_total = 5;
        output_file = False
        try:
            opts, args = getopt.getopt(argv,"hl:t:o:",["length=","total=","output="])
        except getopt.GetoptError:
            print('index.py -l 5 -t 5 -o output.txt')
            sys.exit(2)
        for opt, arg in opts:
            if opt == '-h':
                print('index.py -l <lenght of rows> -t <total texts>')
                sys.exit()
            elif opt in ("-l", "--length"):
                output_lenght = int(arg)
            elif opt in ("-t", "--total"):
                output_total = int(arg)
            elif opt in ("-o", "--output"):
                output_file = arg
        print("Printing {} sentences to single textblock;".format(output_lenght))
        print("Will create {} textblock;".format(output_total))
        if output_file != False:
            print("Saving into {}.txt;".format(output_file))
        print("--------------------")

        # Build the model.
        model_aretino = author.Author('aretino')
        model_aristotele = author.Author('aristotele')
        model_baudelaire = author.Author('baudelaire')
        model_lovecraft = author.Author('lovecraft')
        model_irving = author.Author('washington_irving')
        model_john_keats = author.Author('john_keats')
        model_john_milton = author.Author('john_milton')
        model_edgar_allan_poe = author.Author('edgar_allan_poe')
        model_plato = author.Author('plato')

        print("--------------------")

        text_model = markovify.combine([ model_lovecraft.model, model_baudelaire.model ], [ 0.25, 0.75 ])

        # Print/save five randomly-generated sentences
        if output_file != False:
            f = open( output_directory + output_file + ".txt", 'a')
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
