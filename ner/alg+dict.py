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
def make_dict(a):
    d=dict()
    with open(a,"r",encoding="utf-16") as f:
        for i in f.readlines():
            if(len(i)<3):
                continue
            k=i.split('/')
            # if('Person' in k[1]):
            #     l=k[0].split(',')
            #     if(len(l)<2):
            #         l=l[0].split('_',1)
            #         if(len(l)<2):
            #             d.update(((l[0], ''),))
            #             continue
            #     d.update(((l[0], l[1]),))
            # else:
            #     d.update(((k[0], k[1]),))
    d.update(((k[0], k[1]),))
    return d

def in_dict(word):
    a=dictianory.get(word)
    if(a!=None):
        if("Place" in a):
            return "Place"
        elif("Organisation" in a):
            return "Organisation"
        elif("Misc" in a):
            return "Misc"
        else:
            return "Person"
    else:
        return "S"
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
    'in_dict': in_dict(word)
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
    dictianory=make_dict('Output_Packeruni.txt')
    print("ok")
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

