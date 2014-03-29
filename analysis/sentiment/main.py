import utils.load_emoticondata as load_emoticon
import cPickle
import os
import datetime
import random
from sklearn import svm
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
import classifiers.classifier as classifier


def split_data(data, key):
    grouped_data = {}
    for row in data:
        polarity = row[key]
        if polarity not in grouped_data:
            grouped_data[polarity] = []
        grouped_data[polarity].append(row)
    return grouped_data


def save_classifier(outfile, clf, save_dir='models'):
    outfile = os.path.join(save_dir, outfile)
    with open(outfile, 'wb') as f:
        cPickle.dump(clf, f)

# build dataset
def load_classifier(data, test_data, vectorizer_label='tfidf',
                    classifier_label='svm', ngram_label='unigram', count=10000):
    """
        balances data, gets vectorizer and classifier, initializes classifier.Classifier
        Initialization includes feature selection and training
        INPUT:
            data ([]) - list of {text, polarity, etc.}
            vectorizer_label ('') - ['tfidf', 'count']
            classifier_label ('') - ['svm', 'linear_svm']
            ngram_label ('') - ['unigram', 'bigram']
            count (int) - [0, 1.6MIL]
    """

    # split into even posneg
    grouped_data = split_data(data, 'polarity')
    # careful not to index past the 1.6 millionth row  (idx 800000 for each
    # array):p
    balanced_data = grouped_data[
        'negative'][
        :count] + grouped_data[
        'positive'][
        :count]
    random.shuffle(balanced_data)
    # setup classifier config
    vectorizer_config = {
        'ngram': ngram_label,
        'label': vectorizer_label,
        'min_df': 5}
    vectorizer = get_vectorizer(vectorizer_config)
    clf = get_classifier(classifier_label)
    clf_id = '{0}_{1}_{2}'.format(
        classifier_label,
        vectorizer_label,
        ngram_label)
    config = {
        'data': balanced_data,
        'test_data': test_data,
        'vectorizer': vectorizer,
        'classifier': clf,
        'name': clf_id,
        'feature_key': 'text',
        'target_key': 'polarity'}
    svm_clf = classifier.Classifier(**config)
    return svm_clf


def get_vectorizer(vec_options):
    """
        Helper function to get vectorizer from label
        returns vectorizer
    """
    if vec_options['ngram'] == 'unigram':
        ngram_range = (1, 1)
    elif vec_options['ngram'] == 'bigram':
        # unigrams and bigrams
        ngram_range = (1, 2)

    elif vec_options['ngram'] == 'trigram':
        ngram_range = (1,3)

    if vec_options['label'] == 'tfidf':
        # possible max_features=10000
        vectorizer = TfidfVectorizer(
            min_df=5,
            stop_words='english',
            ngram_range=ngram_range
            )
    elif vec_options['label'] == 'count':
        vectorizer = CountVectorizer(
            min_df=3,
            stop_words='english',
            ngram_range=ngram_range)
    else:
        raise Exception(
            "vectorizer label {0} invalid".format(vec_options['label']))
    return vectorizer


def get_classifier(classifier_label):
    """
        Helper function to establish which classifier to use
        returns a classifier
    """
    if classifier_label == 'svc':
        classifier = svm.SVC()

    elif classifier_label == 'linear_svc':
        classifier = svm.LinearSVC()
    else:
        raise Exception("classifier label invalid")

    return classifier


def run_batch_scores(data, docsize=10000, batches=5):
    """
        Runs <batch> runs with <2 * docsize> 
        - scores in results/classifier_results.txt
        - should fix the 2 * docsize thing since its deceptive
        - should make classifier, vecotirzer, ngram customizable
    """

    for i in range(batches):
        sclf = load_classifier(
            data,
            'tfidf',
            'linear_svc',
            'bigram',
            (i + 1) * docsize)
        sclf.score()

# should configure these in settings
save = False
test_twitter_file = 'trainingandtestdata/testdata.manual.2009.06.14.csv'
emoticon_twitter_file = 'trainingandtestdata/training.1600000.processed.noemoticon.csv'
data = load_emoticon.load_train_data(None, emoticon_twitter_file)
test_data = load_emoticon.load_test_data(None, test_twitter_file)
# should I shuffle?
random.shuffle(data)
classifier_obj = load_classifier(data, test_data, 'tfidf', 'linear_svc', 'bigram', 500000)
s = classifier_obj
fv = s.feature_vectors
print len(fv)
result = classifier_obj.score()
save_str = "{0}_{1}_{2}.pkl".format(
    datetime.datetime.now().strftime("%y-%m-%d-%H-%M"),
    classifier_obj.name, len(classifier_obj.train_data),
    result
)
if save:
    save_classifier(save_str, classifier_obj)
# example of how to load a model
"""
v = 'models/linear_svc_tfidf_bigram_100000_0.757660167131.pkl'
with open(v, 'rb') as f:
    nclf = cPickle.load(f)"""
