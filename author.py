#!/usr/bin/python
from __future__ import print_function

import markovify
import re
import io
import sys
import spacy

import fnmatch
import json
import random
import os

# Spacy
nlp = spacy.load("it")

class Author(object):
    """
    An actor for whom arbitrary-length sentences and a following speaker can be generated.
    Attributes:
        source_text (list of list): a script comprised of a list of lists formatted [SPEAKER, line]
        name (str):                 speaker name, uppercase
        cast (list of str):         list of cast members you want in your new script
        line_nums (list of num):    all the line numbers from `source_text` in which `name` speaks
        text (str):                 all the lines from `source_text` that `name` speaks
        model (POSifiedText):       a markovify.Text model of `text` for generating sentences from
                                        relationships (RangeDict): used for working out the likely next speaker
                                        by `next_speaker`
        relationships_limit (num):  used as the upper random number limit by `choose_next_speaker`
    """
    def __init__(self, name, state_size=2, load_only=False):
        self.name = name
        self.model = self.get_or_generate_model(self.name, state_size, load_only)

    @staticmethod
    def get_or_generate_model(name, state_size, load_only, scripts_location="/generated/", input_location="/input/"):
        """
        Retrieve a stored model or generate a new one and store it
        Generating models can be a time-intensive process, especially during testing, but thankfully Markovify offers a
        `to_json()` method for its model objects. I have used a file naming convention of ACTOR_STATE-SIZE.JSON, but you
        could use whatever you like as long as you provide the correct `pattern` to `find`. This method looks for a file
        of the right name or generates the model and saves it to the scripts folder as JSON. It returns a Markovify text
        model either way.
        :param name:             str, name of actor to return model for
        :param state_size:       num, state size parameter for the model
        :param scripts_location: str, the folder name of where you're keeping the files
        :return:                 obj, Markovify text model
        """

        current_file_path = os.path.abspath(__file__)
        scripts_directory = os.path.split(current_file_path)[0] + scripts_location
        scripts_input = os.path.split(current_file_path)[0] + input_location

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

        if find(name + "_" + str(state_size) + ".json", scripts_directory):
            print("Found:", name)
            with open(scripts_directory + name + "_" + str(state_size) + ".json") as json_data:
                model_json = json.load(json_data)
            return POSifiedText.from_json(model_json)
        else: # Skip missing author
            print("Missing {}.json - Use generate.py to compile;".format(name + "_" + str(state_size)))
            return False

class POSifiedText(markovify.Text):
    def word_split(self, sentence):
        return ["::".join((word.orth_, word.pos_)) for word in nlp(sentence)]

    def word_join(self, words):
        sentence = " ".join(word.split("::")[0] for word in words)
        return sentence
