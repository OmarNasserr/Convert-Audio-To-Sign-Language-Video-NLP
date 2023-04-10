import nltk
# nltk.download('stopwords')
# from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import string
import time


def tokenize_text(transcribed_text):
    start_tokenize_time = time.time()
    text=transcribed_text
    text.lower()
    
    stop_words = ['a', 'an', 'the', 'and', 'of', 'that', 'this', 'it', 'is', 'are', 'am', 'be', 'been',"'re",
                  'was', 'were', 'has', 'have', 'had', 'do', 'does', 'did', 'will', 'would', 'should',
                  'could', 'may', 'might', 'must', 'can', 'ought', 'to', 'in', 'on', 'at', 'with', 'from',
                  'for', 'by', 'about', 'like', 'as', 'but', 'only', 'just', 'very', 'really', 'so',
                  'then', 'there', 'here', 'when', 'where', 'why', 'how', 'what', 'which', 'who', 'whom',
                  'whose', 'if', 'else', 'or', 'either', 'neither', 'nor', 'unless', 'although', 'even', 'though',
                  'whether', 'while', 'since', 'before', 'after', 'until', 'till', 'forth',
                  'here', 'there', 'then', 'today', 'yesterday', 'tomorrow', 'last', 'next', 'every', 'each',
                  'all', 'any', 'some', 'many', 'few', 'several', 'most', 'much', 'more', 'less', 'least', 'enough',
                  'too', 'such', 'other', 'another', 'own', 'same', 'different', 'previous', 'following', 'first',
                  'second', 'third', 'fourth', 'fifth', 'sixth', 'seventh', 'eighth', 'ninth', 'tenth', 'one', 'two',
                  'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten']

    
    # Tokenize the text
    tokens = word_tokenize(text)

    # Lemmatize the tokens to get the right tense
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(token, pos='v') for token in tokens]

    # Remove stop words and punctuation marks
    punctuations = set(string.punctuation)
    tokens = [token.lower() for token in tokens if token not in punctuations and token not in stop_words]

    print("TOKENS ",tokens)
    
    #calculate time used
    end_tokenize_time = time.time()
    total_tokenize_time = end_tokenize_time - start_tokenize_time
    
    print(f"Total tokenize time: {total_tokenize_time:.2f} seconds")
        
    return tokens