from keras.models import load_model
from keras_preprocessing.text import Tokenizer
from keras_preprocessing.sequence import pad_sequences
import numpy as np
import re
import string
from sklearn.feature_extraction._stop_words import ENGLISH_STOP_WORDS


MODEL_PATH = "SpamDetection\\spam_model.h5"

model = load_model(MODEL_PATH) 


# some config values 
embed_size = 100 # how big is each word vector
max_feature = 50000 # how many unique words to use (i.e num rows in embedding vector)
max_len = 2000 # max number of words in a question to use

tokenizer = Tokenizer(num_words= max_feature)


def Analyze_Message(message : str):
    def remove_hyperlink(word):
        return  re.sub(r"http\S+", "", word)

    def to_lower(word):
        result = word.lower()
        return result
    def remove_stop_words(words):
        result = [i for i in words if i not in ENGLISH_STOP_WORDS]
        return result
    
    def remove_number(word):
        result = re.sub(r'\d+', '', word)
        return result

    def remove_punctuation(word):
        result = word.translate(str.maketrans(dict.fromkeys(string.punctuation)))
        return result

    def remove_whitespace(word):
        result = word.strip()
        return result

    def replace_newline(word):
        return word.replace('\n','')   

    def clean_up_pipeline(sentence):
        cleaning_utils = [remove_hyperlink,
                        replace_newline,
                        to_lower,
                        remove_number,
                        remove_punctuation,
                        remove_whitespace,
                        remove_stop_words]
        for func in cleaning_utils:
            sentence = func(sentence)
        return sentence
    
    message = clean_up_pipeline(message)
    
    del clean_up_pipeline,remove_stop_words,remove_hyperlink,replace_newline,to_lower,remove_number,remove_punctuation,remove_whitespace
    
    text = np.array(message)
    tokenizer.fit_on_texts(text)
    toCheck = tokenizer.texts_to_sequences(text)
    toCheck = pad_sequences(toCheck,maxlen=max_len)
    predict_result = 10*model.predict(toCheck)[0][0] 
    return True if predict_result > 0.5 else False



