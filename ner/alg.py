import learn as learn
import opencorpora
from ast import literal_eval

import numpy
import pycrfsuite
import scipy
import sklearn
import sklearn_crfsuite
from sklearn.cross_validation import cross_val_score
from sklearn.grid_search import RandomizedSearchCV
from sklearn.metrics import make_scorer
from sklearn_crfsuite import metrics
from sklearn import svm
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.feature_extraction import DictVectorizer, FeatureHasher
import sklearn.metrics

def word2features(sent, i):
    word = sent[i][0]
    postag = sent[i][1]
    features = {
    'bias': 1.0,
    'word.lower()': word.lower(),
    'word[-3:]': word[-3:],
    'word[-2:]': word[-2:],
    'word.isupper()': word.isupper(),
    'word.istitle()': word.istitle(),
    'word.isdigit()': word.isdigit(),
    'postag': postag,
    'postag[:2]': postag[:2],
}
    if i > 0:
        word1 = sent[i - 1][0]
        postag1 = sent[i - 1][1]
        features.update({
            '-1:word.lower()': word1.lower(),
            '-1:word.istitle()': word1.istitle(),
            '-1:word.isupper()': word1.isupper(),
            '-1:postag': postag1,
            '-1:postag[:2]': postag1[:2],
        })
    else:
        features['BOS'] = True
    if i < len(sent) - 1:
        word1 = sent[i + 1][0]
        postag1 = sent[i + 1][1]
        features.update({
            '+1:word.lower()': word1.lower(),
            '+1:word.istitle()': word1.istitle(),
            '+1:word.isupper()': word1.isupper(),
            '+1:postag': postag1,
            '+1:postag[:2]': postag1[:2],
        })
    else:
        features['EOS'] = True
    return features
def sent2features(sent):
    return [word2features(sent, i) for i in range(len(sent))]
def sent2labels(sent):
    return [label for token, postag, label in sent]
def sent2tokens(sent):
    return [token for token, postag, label in sent]
if __name__ == '__main__':
    sents=list()
    sents2=list()

    with open('corpus2',"r",encoding="utf-16") as f:
        for i in f.readlines():
            i.replace('\n','')
            k=eval(i)
            sents.append(k)
    with open('test2.txt',"r",encoding="utf-16") as f:
        for i in f.readlines():
            i.replace('\n','')
            k=eval(i)
            sents2.append(k)
    X_train = [sent2features(s) for s in sents]
    y_train = [sent2labels(s) for s in sents]
    X_test = [sent2features(s) for s in sents2]
    y_test = [sent2labels(s) for s in sents2]
    print(sent2features(sents[0])[0])
    crf = sklearn_crfsuite.CRF(
        algorithm='lbfgs',
        c1=0.051508376528013232,
        c2=0.0027557838685648719,
        max_iterations=100,
        all_possible_transitions=True
    )
    crf.fit(X_train, y_train)
    labels = list(crf.classes_)
    #labels.remove('O')
    y_pred = crf.predict(X_test)
    #print(cross_val_score(crf,X_train,y_train,cv=5,scoring='f1_micro'))
    print(metrics.flat_f1_score(y_test, y_pred,
        average='weighted'))
    sorted_labels = sorted(
        labels,
        key=lambda name: (name[1:], name[0]))
    print(metrics.flat_classification_report(
        y_test, y_pred, labels=sorted_labels, digits=3
        ))

    clf= svm.SVC(kernel='linear')
    temp=numpy.array(DictVectorizer(sparse=False).fit_transform(X_train[0]))
    X=list()
    to_vector=pycrfsuite.ItemSequence(X_train[0]).items()
    for t in X_train:
        wordtemp=pycrfsuite.ItemSequence(t).items()
        for z in wordtemp:
            to_vector.append(z)
    vectorizer=DictVectorizer()
    X=vectorizer.fit_transform(to_vector)
    Y1 = list()
    for t in y_train[0]:
        Y1.append(t)
    for t in y_train:
        #wordtemp=pycrfsuite.ItemSequence(t).items()
        for z in t:
            Y1.append(z)
    #Y=FeatureHasher().fit_transform(Y1)
    clf.fit(X,Y1)
    to_vector2 = pycrfsuite.ItemSequence(X_test[0]).items()
    for t in X_test:
        wordtemp = pycrfsuite.ItemSequence(t).items()
        for z in wordtemp:
            to_vector2.append(z)
    X2 = vectorizer.transform(to_vector2)
    Y2 = list()
    for t in y_test[0]:
        Y2.append(t)
    for t in y_test:
        # wordtemp=pycrfsuite.ItemSequence(t).items()
        for z in t:
            Y2.append(z)
    y_pred = clf.predict(X2)
    print(sklearn.metrics.f1_score(Y2,y_pred,average=None))
    print("ok")
    clf2= sklearn.linear_model.LogisticRegression()
    clf2.fit(X,Y1)
    y_pred2=clf2.predict(X2)
    print(sklearn.metrics.f1_score(Y2, y_pred2, average=None))
    print(sklearn.metrics.precision_recall_fscore_support(Y2, y_pred, labels=sorted_labels, average=None))
    print(sklearn.metrics.precision_recall_fscore_support(Y2, y_pred2, labels=sorted_labels, average=None))


