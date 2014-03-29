# svg class
import time
import datetime
class Classifier:

    """
        Classifier class to wrap different methods, svm, niave bayes, etc..
    """

    def __init__(self, **kargs):
        """
            Size of data set should be controlled above this layer.
            Trying to keep this as lightweight as possible 
            **kargs
                data ([]]) - [{'text': X, 'polarity': Y]
                name ('') - label for the classifier
                vectorizer -(<instance>) sklearn.feature_extraction.text vectorizer
                clf = - (<instance>)-  sklearn classifier
                feature_key ('') - key to build feature_vectors. currently = 'text'
                target_key ('') - key to build target_vectors. currently = 'polarity'

            maybe rip the data part out of this and just pass in target_vectors, feature_vectors
            vectorizer would have to move out too though
        """
        self.data = kargs['data']
        self.test_data = kargs['test_data']
        self.name = kargs['name']
        self.vectorizer = kargs['vectorizer']
        self.clf = kargs['classifier']
        self.feature_key = kargs['feature_key']
        self.target_key = kargs['target_key']
        self.train_time = None
        self.train_data = [row[self.feature_key]
                           for row in self.data]
        self.target_vectors = [row[self.target_key]
                               for row in self.data]
        self.feature_vectors = None
        self.test_targets = [row[self.target_key]
                                for row in self.test_data]
        self.test_data = [row[self.feature_key]
                            for row in self.test_data]
        self.train()
        self.test_features = self.create_test_vectors(self.test_data)


    def __len__(self):
        return len(self.data)

    def __str__(self):
        return'{0}\t{1}'.format(self.name, len(self))

    def train(self):
        """
            Helper function to train classifier
        """
        print "Training {0}".format(self)
        self.feature_vectors = self.create_feature_vectors(self.train_data)
        self.fit_classifier()


    def create_feature_vectors(self, train_data):
        """
            Transforms train_data into vectors using sklearn vectorizer specified by self.vectorizer
        """
        print "creating {0} feature vectors with {1}".format(len(train_data), self.name)
        return self.vectorizer.fit_transform(train_data)

    def create_test_vectors(self, test_data):
        print "Creating {0} test feature vectors with {1}".format(len(test_data), self.name)
        return self.vectorizer.transform(test_data)


    def fit_classifier(self):
        """
            trains classifier with self.feature_vectors, target_vectors
        """
        print "fitting classifier with {0} vectors".format(len(self))
        start = time.clock()
        self.clf.fit(self.feature_vectors, self.target_vectors)
        end = time.clock()
        diff = (end - start)
        self.train_time = diff
        print "{0} train {1} seconds".format(len(self), diff)

    def text_to_feature(self, text):
        return self.vectorizer.transform(text)


    def predict(self, text, negation=False):
        """if negation:
            negation = ['not', 'aint', 'shouldnt']
            words = text.split(' ')
            for idx, word in enumerate(words):
                    if word in negation and idx+1 < len(words):
                        neg_str = "_".join([words[idx], words[idx + 1]])
                        print "negating\t",neg_str
                        words[idx] = neg_str
            text = " ".join(words)"""
        val = self.clf.predict(self.text_to_feature([text]))
        print val
        return val

    def score(self):
        print "scoring ... {0}".format(self)
        # get results
        res = self.clf.score(self.test_features, self.test_targets)
        # write result to file
        with open('results/classifier_results.txt', 'a') as outf:
            res_str = "{5},{0},{1},{2},{3},{4}".format(
                self.name,
                len(self.train_data),
                len(self.test_data),
                self.train_time,
                res,
                datetime.datetime.now().strftime("%y-%m-%d-%H-%M")
                )
            outf.write('\n')
            outf.write(res_str)
        print res_str
        # return result, and res_str for save_file
        return res



