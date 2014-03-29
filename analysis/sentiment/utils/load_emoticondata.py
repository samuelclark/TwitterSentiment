# assumes input is coming from this specific csv file, needs a bit of work
# to be generalized


def load_csv(infile, data_keys, limit):
    """
        infile (STRING) - specifying csv path
        data_key (LIST) - specifying column headers
        parses a csv file with no headers to a list of dictionaries dictionary
    """
    with open(infile, 'rb') as data_file:
        if not limit:
            return (
                [dict(zip(data_keys, line.split(","))) for line in data_file]
            )
        else:
            data = []
            for num, line in enumerate(data_file):
                if num < limit:
                    data.append(dict(zip(data_keys, line.split(','))))
                else:
                    return data


# should this go in a different file
def get_polarity(value):
    """
        Transform function to assign string polarity
    """
    targets = {0: 'negative', 2: 'neutral', 4: 'positive'}
    val = int(value.replace('"', ''))
    return targets[val]


def clean_data(data, negation=False):
    """
        data (LIST)
        cleans and adds basic representation of data

    """
    print "parsing data"
    cleaned_data = []
    for item in data:
        item['polarity'] = get_polarity(item['polarity'])
        # handle encoding
        if item['polarity'] in ['positive', 'negative']:
            try:
                item['text'] = unicode(item['text'], 'utf-8')
                cleaned_data.append(item)
            except Exception:
                # loss of ~ 1200 files here dude to a specific deconding issue
                # (character offset 80-81)
                pass
    return cleaned_data

# new function to generate features?

def negate(text):
    pass
    """if negation:
        negation = ['not', 'aint', 'shouldnt']
        words = text.split(' ')
        for idx, word in enumerate(words):
            if word in negation and idx + 1 < len(words):
                words[idx] = "_".join([word, words[idx + 1]])
                item['text'] = " ".join(words)
            else:
                item['text'] = text
    """
def load_train_data(limit, emoticon_twitter_file):
    """
        Helper function that executes full loading process
        returns (LIST) data.
        called in model.py
    """
    
    emoticon_twitter_keys = ['polarity', 'id', 'date', 'query', 'user', 'text']
    print "loading data from {0}".format(emoticon_twitter_file)
    data = load_csv(emoticon_twitter_file, emoticon_twitter_keys, None)
    cleaned_data = clean_data(data)
    return cleaned_data


def load_test_data(limit, test_twitter_file):
    """
        Loads the test set for evaluation
    """
    test_twitter_keys = ['polarity', 'id', 'date', 'query', 'user', 'text']
    test_data = load_csv(test_twitter_file, test_twitter_keys, None)
    posneg_data = []
    for item in test_data:
        item['polarity'] = get_polarity(item['polarity'])
        if item['polarity'] in ['positive', 'negative']:
            posneg_data.append(item)
    return posneg_data
