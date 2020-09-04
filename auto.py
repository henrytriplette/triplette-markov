#!/usr/bin/python

import os
import re
import sys, getopt
import time
import random
import argparse
import markovify

from datetime import datetime

import author
import upload

# List of paths used by the generator
current_file_path = os.path.abspath(__file__)
scripts_directory = os.path.split(current_file_path)[0] + "/generated/"
input_directory = os.path.split(current_file_path)[0] + "/input/"
output_directory = os.path.split(current_file_path)[0] + "/output/"

# Date for filename save
date_string = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")



def generateRandomAuthors(authors, max_lenght):

    # Set random lenght for lists
    first_pass_len = random.randint(1,len(authors))
    second_pass_len = random.randint(1,len(authors))

    # Clone lists
    first_pass = authors[:]
    second_pass = authors[:]

    # Shuffle list
    random.shuffle(first_pass)
    random.shuffle(second_pass)

    # Truncate lists and return
    output = authors[:first_pass_len] + authors[:second_pass_len]

    if len(output) > max_lenght:
        random.shuffle(output)
        output = output[:max_lenght]

    author_data = []
    for author in output:
        author_record = {}
        author_record['name'] = author
        author_record['weight'] = random.randint(1,2)
        author_data.append(author_record)

    return author_data

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
    clean_str = clean_str.replace(" ,", ", ")
    clean_str = clean_str.replace(" .", ".\n")
    clean_str = clean_str.replace(" ;", ";\n")

    clean_str = clean_str.replace(" ?", "?\n")
    clean_str = clean_str.replace(" !", "!\n")

    return clean_str

def main(argv):

    input_state_size = argv.depth
    output_lenght = argv.length
    output_total = argv.total
    output_file = argv.file

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
    print("+--------------------+")

    # Generate author list
    authors_selected = generateRandomAuthors(author_available, 2)
    print(authors_selected)

    ## Load
    for author_selected in authors_selected:
        # Load only selected authors when requested
        filename_author = author.Author(author_selected['name'], input_state_size)
        if filename_author != False:
            print("- Loaded {}: {} state size, {} weight;".format(author_selected['name'],str(input_state_size),str(author_selected['weight'])))
            authors[author_selected['name']] = filename_author

    print("+--------------------+")

    # Build the model by splitting the dictionary into two separated lists.
    author_tocombine = []
    author_toweight = []
    author_filename = ""
    for author_toload in authors_selected:
        print(author_toload)
        name = author_toload['name']
        weight = int(author_toload['weight'])
        if authors[name].model:
            author_tocombine.append(authors[name].model)
            author_toweight.append(weight)
            author_filename = author_filename + name

    # Combine the two or more authors and their weight
    text_model = markovify.combine(author_tocombine, author_toweight)

    # Print/save five randomly-generated sentences
    f = open( output_directory + output_file + "-" + author_filename + "-" + date_string + ".txt", 'a')
    f.truncate()
    for i in range(output_total):
        text = get_sentences(output_lenght, text_model)
        print(text)
        print("+--------------------+")
        f.write(text + '\n\n')

if __name__ == "__main__":

    # Initialize
    parser = argparse.ArgumentParser(description='Generate random text based on markov chains.')
    parser.add_argument('-d', '--depth', help='Model Depth', default=2, choices=[ 2, 3 ]) # input_state_size
    parser.add_argument('-l', '--length', help='Text lenght', default=5) # output_lenght
    parser.add_argument('-t', '--total', help='Total number of text generated', default=5) # output_total
    parser.add_argument('-f', '--file', help='Filename Prefix', default='auto') # output_file

    args = parser.parse_args()

    try:
        while True:
            main(args)
            upload.main()
            time.sleep(60)
    except KeyboardInterrupt:
        print('Ended!')
