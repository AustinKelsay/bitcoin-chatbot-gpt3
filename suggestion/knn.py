import pandas as pd
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
from wrangle_clean_utils import *

# Assigning filepaths of datasets to variables
data_path1 = '/Users/pretermodernist/bitcoin-chatbot-gpt3/datasets/chow_collection_scrape.json'
data_path2 = '/Users/pretermodernist/bitcoin-chatbot-gpt3/datasets/mastering_bitcoin_scrape.json'
data_path3 = '/Users/pretermodernist/bitcoin-chatbot-gpt3/datasets/nakamoto_institute_scrape.json'

# Reading in datasets and combining them into one
btc1 = wrangle_jsonl(data_path1)
btc2 = wrangle_jsonl(data_path2)
btc3 = wrangle_jsonl(data_path3)
btc = pd.concat([btc1,btc2,btc3])

# Cleaning columns with regex functions
btc['title'] = btc['title'].apply(clean_suggestion_title)
btc['text'] = btc['text'].apply(clean_suggestion_text)

### Install python -m spacy download en_core_web_sm in your terminal before running this file! ###
nlp = spacy.load('en_core_web_sm')


def tokenize(doc):
    tokens = []
    doc = nlp(doc)
    for token in doc:
        # Filtering out punctuation, and stop words. Filtering in lemmas and case normalizion.
        if ((token.is_punct != True) and
            (token.is_lower != True) and
            (token.lemma_ != 'PRON-') and
                (token.is_stop == False)):
            tokens.append(token.lemma_)
    return tokens


# Confirming number of CPU cores we can use for parrallel processing
cores = psutil.cpu_count()
# Can't use all our processing power. Might crash our machines
num_cores = cores - 3
# Instantiating our multi-threadder
pandarallel.initialize(
                       progress_bar=True,
                       nb_workers=num_cores
                       )
# Preprocessing our data with speed
btc['tokens'] = btc['text'].parallel_apply(tokenize)

# Formatting our preprocessed data for our NLP algorithms
btc['token_list'] = btc['tokens'].apply(listintostring)


### USER INPUT FROM GPT3 CHATBOT###
# Current value is a PLACEHOLDER
user_input = ["What is a blockchain?"]
# Creating a new DF solely for nearest neighbor querying
btc_test = pd.DataFrame(btc['text'])
# Inserting our user input into the dataframe for querying
btc_test.loc[len(btc_test.index)] = user_input
# viewing our user input in our test DF
btc_test.tail(1)

# Tuning our vectorizer model
vect = TfidfVectorizer(
                       stop_words='english',
                       # Allowing for both unigrams, bigrams, and trigrams
                       ngram_range=(1, 2),
                       max_features=10000       # Not allowing more than 10k features/dimensions in our model
                       )

# Creating our document term matrix
dtm = vect.fit_transform(btc_test['text'])
dtm = pd.DataFrame(dtm.toarray(), columns=vect.get_feature_names())
# Using ball_tree to measure distance of points
nn = NearestNeighbors(
                      n_neighbors=25,
                      algorithm='ball_tree'
                      )
nn.fit(dtm)  # Fitting our DTM to our KNN model

### For debugging user inputs ###
# print(btc_test.iloc[-1])

# Assigning our last row(which contains our user input from the chatbot)
doc_index = 10371
# using integer location(iloc) on the document index in order to sample them
doc = [dtm.iloc[doc_index].values]
# Query ysing kneighbors
neigh_dist, neigh_index = nn.kneighbors(doc)

# For loop for querying articles based on our user input for the chatbot
for doc in neigh_index:
    suggestion = btc_test.iloc[doc]


def return_link(suggestion, btc):
    num_index = suggestion.index[1]
    for b in btc.index:
        if num_index == b:
            return btc.link.iloc[b]


query = return_link(suggestion, btc)
### You can surface this `query` variable to the frontend! ###
print(query)
