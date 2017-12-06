
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn import metrics
from sklearn.linear_model import PassiveAggressiveClassifier
from sklearn.linear_model import LassoLars
from sklearn.feature_extraction.text import HashingVectorizer
import pickle

# df = pd.read_csv("https://s3.amazonaws.com/assets.datacamp.com/blog_assets/fake_or_real_news.csv")
# df.to_pickle('news_data')


def tfidf_vectorizer(X_train,X_test, Y_train, Y_test):
    tfidf_vectorizer = TfidfVectorizer(stop_words='english', max_df=0.7)
    tfidf_train = tfidf_vectorizer.fit_transform(X_train)
    tfidf_test = tfidf_vectorizer.transform(X_test)
    print ("The accuracy with NB classifier and tfidf vectorizer is %f",NB_classifier(tfidf_train,tfidf_test,Y_train,Y_test))
    print ("The accuracy with pasive agressive classifier and tfidf vectorizer is %f", passive_aggressive_classifier(tfidf_train,tfidf_test,Y_train,Y_test))
    # print larso_lass_classifier(tfidf_train, tfidf_test, Y_train, Y_test)

def count_vectorizer(X_train,X_test, Y_train, Y_test):
    vectorized_count = CountVectorizer(stop_words='english')
    count_train = vectorized_count.fit_transform(X_train)
    count_test = vectorized_count.transform(X_test)
    print ("The accuracy with NB classifier and count vectorizer is %f",NB_classifier(count_train,count_test, Y_train, Y_test))
    print ("The accuracy with pasive agressive classifier and count vectorizer is %f", passive_aggressive_classifier(count_train, count_test, Y_train, Y_test))
    # print larso_lass_classifier(count_train,count_test, Y_train, Y_test)

def hashing_vectorizer(X_train, X_test, Y_train, Y_test):
    hashing_vect = HashingVectorizer(stop_words='english', non_negative=True)
    hash_train = hashing_vect.fit_transform(X_train)
    hash_test = hashing_vect.transform(X_test)
    print ("The accuracy with NB classifier and hash vectorizer is %f",
           NB_classifier(hash_train, hash_test, Y_train, Y_test))
    print ("The accuracy with pasive agressive classifier and hash vectorizer is %f",
           passive_aggressive_classifier(hash_train, hash_test, Y_train, Y_test))


def NB_classifier(X_train,X_test,Y_train, Y_test):
    clf = MultinomialNB()
    clf.fit(X_train, Y_train)
    prediction = clf.predict(X_test)
    return metrics.accuracy_score(prediction, Y_test)

def passive_aggressive_classifier(X_train,X_test,Y_train, Y_test):
    clf1 = PassiveAggressiveClassifier(n_iter=50)
    clf1.fit(X_train,Y_train)
    prediction = clf1.predict(X_test)
    return metrics.accuracy_score(prediction,Y_test)

def larso_lass_classifier(X_train,X_test,Y_train, Y_test):
    clf2 = LassoLars(alpha=0.2)
    clf2.fit(X_train, Y_train)
    prediction = clf2.predict(X_test)
    return metrics.accuracy_score(prediction, Y_test)

def fake_news_detector(data):
    df = pd.read_pickle(data)
    # print df.shape
    # print df.head()
    df = df.set_index("Unnamed: 0")
    y = df.label
    df.drop('label', axis=1)

    X_train, X_test, Y_train, Y_test = train_test_split(df['text'], y, test_size=0.33, random_state=53)

    tfidf_vectorizer(X_train, X_test, Y_train, Y_test)
    count_vectorizer(X_train, X_test, Y_train, Y_test)
    hashing_vectorizer(X_train, X_test, Y_train, Y_test)



fake_news_detector('news_data')