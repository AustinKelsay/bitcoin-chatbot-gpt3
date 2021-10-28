import string
my_text = "It turns out that + is associative, which means that (A + B) + C = A + (B + C). That means we can write A + B + C without parentheses and without ambiguity.\n"
print(my_text.translate(str.maketrans('', '', string.punctuation)))