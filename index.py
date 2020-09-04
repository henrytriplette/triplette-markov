import markovify

# Get raw text as string.
with open("input/arthur_rimbaud.txt") as f:
    text = f.read()

# Build the model.
text_model = markovify.Text(text) # For point as end of sentence formatted text
# text_model = markovify.NewlineText(text) # For new line  as end of sentence formatted text

# Print five randomly-generated sentences
for i in range(5):
    print(text_model.make_sentence())

# Print three randomly-generated sentences of no more than 280 characters
for i in range(3):
    print(text_model.make_short_sentence(280))
