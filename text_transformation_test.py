import string
my_text = "a\n\n\n\n\n\n"
print(my_text.translate(str.maketrans('', '', string.punctuation)))