from __future__ import print_function

import markovify
import os
import re

import author

current_file_path = os.path.abspath(__file__)
scripts_directory = os.path.split(current_file_path)[0] + "/generated/"

default_num = 5;

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
        return clean_str

    # Build the model.
    model_aretino = author.Author('aretino')
    model_aristotele = author.Author('aristotele')
    model_baudelaire = author.Author('baudelaire')
    model_lovecraft = author.Author('lovecraft')

    text_model = markovify.combine([ model_lovecraft.model, model_baudelaire.model ], [ 0.25, 0.75 ])


    # Print five randomly-generated sentences
    for i in range(5):
        text = get_sentences(5, text_model)
        print(text)
        print("--------------------")

    # Print three randomly-generated sentences of no more than 140 characters
    # for i in range(3):
    #    print(text_model.make_short_sentence(140))
