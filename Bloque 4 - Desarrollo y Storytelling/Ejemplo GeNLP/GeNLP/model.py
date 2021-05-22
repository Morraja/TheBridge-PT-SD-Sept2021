"""
Model preprocessing file for GeNLP.

Author: Esteban M. Sanchez Garcia
LinkedIn: linkedin.com/in/estebanmsg/
GitHub: github.com/esan94
Medium: medium.com/@emsg94
Kaggle: kaggle.com/esan94
"""


from nltk import pos_tag, word_tokenize
from nltk.stem import WordNetLemmatizer


PUNCTUATION = dict.fromkeys('!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~', " ")
POS_MAP_LEMMA = {
    "JJ": "a", "JJR": "a", "JJS": "a", "NN": "n", "NNS": "n", "RB": "r",
    "RBR": "r", "RBS": "r", "VB": "v", "VBD": "v", "VBG": "v", "VBN": "v",
    "VBP": "v", "VBZ": "v"}
LEMMATIZER = WordNetLemmatizer()


def lemmatization(text, lemmatizer, pos_lemma):
    """Make lematization in a text.

    Make a lemmatization taking into account part-of-speech
    on each word of a sencente. And delete extra white
    space.

    Parameters
    ----------
        text: str
            Synopsis of a film.

        lemmatizer: class
            WordNetLemmatizer instance.

        pos_lemma: dict
            Part of speech mapping dictionary.

    Return
    ------
        str:
            Synopsys lemmatized.

    """
    return " ".join([lemmatizer.lemmatize(token[0],
                     pos=pos_lemma.get(token[1], "n"))
                     for token in pos_tag(word_tokenize(text))])

def is_alpha(text):
    """Only letters.

    Keep only alphabet.

    Parameters
    ----------
        text: str
            Synopsis of a film.

    Return
    ------
        numpy.array:
            Data with synopsis cleaned.

    """
    return " ".join(word if word.isalpha()
                    else " " for word in text.split())

def preprocessing_text_data(data):
    """Preprocessing text data.

    Take into account all preprocessing techniques and apply
    everyone to a synopsis column.

    Parameters
    ----------
        data: str
            Data from form.

    Return
    ------
        numpy.array:
            Data with synopsis cleaned.

    """
    # Lowercase text.
    data = data.lower()
    # Remove punctuation.
    data = data.translate(str.maketrans(PUNCTUATION))
    # Keep letters only.
    data = is_alpha(data)
    # Lemmatize text.
    data = lemmatization(data, LEMMATIZER, POS_MAP_LEMMA)

    return data
