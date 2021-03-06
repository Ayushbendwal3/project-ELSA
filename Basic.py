import nltk
from sklearn import linear_model
import sklearn
import random
from nltk.stem.lancaster import LancasterStemmer
import pickle
import json
import os
import numpy
nltk.download('punkt')
stemmer = LancasterStemmer()


def init():
    with open("models/intents.json") as file:
        data = json.load(file)

    try:
        with open("models/data.pickle", "rb") as f:
            words, labels, training, output = pickle.load(f)

    except:
        words = []
        labels = []
        docs_x = []
        docs_y = []

        for intent in data["intents"]:
            for pattern in intent["patterns"]:
                wrds = nltk.word_tokenize(pattern)
                words.extend(wrds)
                docs_x.append(wrds)
                docs_y.append(intent["tag"])

            if intent["tag"] not in labels:
                labels.append(intent["tag"])

        words = [stemmer.stem(w.lower()) for w in words if w != "?"]
        words = sorted(list(set(words)))

        labels = sorted(labels)

        training = []
        output = []

        out_empty = [0 for _ in range(len(labels))]

        for x, doc in enumerate(docs_x):
            bag = []

            wrds = [stemmer.stem(w.lower()) for w in doc]

            for w in words:
                if w in wrds:
                    bag.append(1)
                else:
                    bag.append(0)

            output_row = out_empty[:]
            output_row[labels.index(docs_y[x])] = 1

            training.append(bag)
            output.append(output_row)

        training = numpy.array(training)
        output = numpy.array(output)

        with open("models/data.pickle", "wb") as f:
            pickle.dump((words, labels, training, output), f)

    try:
        pre_model = open("models/model.pickle", "rb")
        model = pickle.load(pre_model)

    except:
        x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(
            training, output, test_size=0.1)
        model = linear_model.LinearRegression()
        model.fit(x_train, y_train)
        with open("models/model.pickle", "wb") as f:
            pickle.dump(model, f)

    return model, words, labels, data


def bag_of_words(s, words):
    bag = [0 for _ in range(len(words))]

    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]

    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1

    return numpy.array(bag)
