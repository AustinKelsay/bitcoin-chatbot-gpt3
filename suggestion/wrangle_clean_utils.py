from pandarallel import pandarallel
import psutil
import pandas as pd
import json as j
import re
import num2words
import spacy
spacy.util.fix_random_seed(0)


def wrangle_jsonl(path: str):
    '''
    Reads in our bitcoin data from a json lines file

    Parameters
    ----------
    None

    Returns
    -------
    df: pandas datafarme 
        Contains text data from several reputable BTC news and historical sources
    '''
    # Preparing jsonl file for reading in
    with open(path) as l:
        lines = l.read().splitlines()

    # Loading the json lines object into an intermediary pandas DataFrame
    df_inter = pd.DataFrame(lines)
    df_inter.columns = ['json_element']

    # Applying json loads function on each row of the json_element column to decode
    # json object into a dictionary
    df_inter['json_element'].apply(j.loads)

    # Converting any semi-structured json data with a normalize function
    # json keys are made into a flat table
    df = pd.json_normalize(df_inter['json_element'].apply(j.loads))

    # Returning read_in json and its DF equivalent so we can explore our data
    # whichever way we wish
    return df


def clean_suggestion_title(uncleaned):
    """
    Accepts a single text document in the form of a pandas Series and performs 
    several regex substitutions in order to clean it.

    Is only meant to be applied to the title column.

    Parameters
    ----------
    text: pandas Series

    Returns
    -------
    text: pandas Series
    """
    newline_breaks = '\n\n###\n\n'
    left_over = ' ->'
    replace_with = ""
    removed_lines = re.sub(newline_breaks, replace_with, uncleaned)
    cleaned = re.sub(left_over, replace_with, removed_lines)

    return cleaned


def clean_suggestion_text(uncleaned):
    """
    Accepts a single text document in the form of a pandas Series and performs 
    several regex substitutions in order to clean it.

    Is only meant to be applied to the text column.

    Parameters
    ----------
    text: pandas Series

    Returns
    -------
    text: pandas Series
    """
    newline_break = '\n'
    end = 'END'
    replace_with = ""
    removed_line = re.sub(newline_break, replace_with, uncleaned)
    nearly_clean = re.sub(
        r"(\d+)", lambda x: num2words.num2words(int(x.group(0))), removed_line)
    almost_clean = re.sub(r'https?://[^\s]+', '', nearly_clean)
    cleaned = re.sub(end, replace_with, almost_clean)

    # Applying case normalization to each body of text
    return cleaned.lower()


def listintostring(string):
    '''
    This function converts lists into strings
    '''
    str = " "
    return (str.join(string))
