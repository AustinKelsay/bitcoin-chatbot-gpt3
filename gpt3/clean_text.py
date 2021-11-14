
def clean(text):
    num_of_letters = len(text) - text.count(" ")
    if text.count(" ") < num_of_letters:
        return text
    else:
        return False