from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import random
import nltk
import collections
from collections import defaultdict
import time

def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200 
            and content_type is not None 
            and content_type.find('html') > -1)


def log_error(e):
    """
    It is always a good idea to log errors. 
    This function just prints them, but you can
    make it do anything.
    """
    print(e)

with open("hateSpeechDetector\DataFiles\\file.txt", "r") as f:
    dictionary_of_words = {}
    for each_line in f:
        line = each_line.split(sep=',')
        time.sleep(0.05)
        ID = line[0]
        Label = line[1]
        dictionary_of_words[ID.strip()] = Label.strip()
        x = 'https' + '://twitter.com/anyuser/status/' + str(ID)
        raw_html = simple_get(x)
        html = BeautifulSoup(raw_html, 'html.parser')
        for title in html.select('title'):
            try:
                if title.text != 'Twitter / Account Suspended':
                    full_title = title.text
                    splited = full_title.split(' Twitter: ')[-1]
                    sentence = splited[1:-1]
                    with open('hateSpeechDetector\DataFiles\\file.txt' , 'a') as f:
                        f.write(sentence + '\n')
                    print(x)
            except:
                x = 1



## Credits to Eugene for creating this Model During YouthHacks 2019 Thanks bro.


# Note:
#   Due to the way the dataset was created, one document (Racism_Codes) contains the sentence ID and the corresponding classification
#   while the folder 'all_files' contains text documents containing one sentence each, where the name of the document is the same as 
#   their sentence ID. It is advised to take a look at the format and contents of Racism_Codes

f=open("hateSpeechDetector\ResultFiles\\result.txt", "r")
if f.mode == 'r':
    contents = f.read()

x = contents.split('\n')
y = [a.split() for a in x]  #Each line is split at blankspace to produce (sentence_ID,classification) tuples

racist = []
normal = []
try:
    for ID,tag in y:
            ## Make sure to change the pathway according to the location of the file in your computer lol
            full_path = z = r'C:\Users\Sean\Desktop\all_files\\' + ID + ".txt"
            f=open(full_path, "r")
            sentence = f.read()
            if tag == 'hate':
                racist.append(sentence)
            else:
                normal.append(sentence)
except:
    tt = 111 ## This was added because I am not sure if an empty code block after 'except' would throw and error

normal_sents = [(sent, 'not racist') for sent in normal]
racist_sents = [(sent, 'racist') for sent in racist]



# Feature Extraction functions
def features_BOW(sentence):
    '''Returns a dictionary where the key is the word and the value is True. This indicates that a word is present in the sentence
    BOW stands for Bag of Words which is the techincal term for this type of feature extraction'''
    words = sentence.lower().split()
    features = {}
    for word in words:
        features[word] = True
    return features

def features_PrevWord(sentence):
    '''Returns a dictionary where the key is a word pair (bigram) and the value is True. This indicates that a word pair is present in the sentence'''
    words = sentence.lower().split()
    bigrams = list(nltk.bigrams(words))
    features = {}
    for bi in bigrams:
        features[bi] = True
    return features


def features(sentence):
    '''Combines feature dictionaries into one'''
    features = features_BOW(sentence)
    # Notice the surprising difference in f-score bewteen using only BOW and using both BOW and Bigrams as featurs
    #features.update(features_PrevWord(sentence))
    return features



#Separate the sentences into 10 folds (folds can be thought of as 'sections')
fold_0 = []
fold_1 = []
fold_2 = []
fold_3 = []
fold_4 = []
fold_5 = []
fold_6 = []
fold_7 = []
fold_8 = []
fold_9 = []

# Remainder thingy used to separate sentences into 10 sections
for i in range(len(normal_sents)):
    if (i + 10)%10 == 0:
        fold_0.append(normal_sents[i])
    elif (i + 10)%10 == 1:
        fold_1.append(normal_sents[i])
    elif (i + 10)%10 == 2:
        fold_2.append(normal_sents[i])
    elif (i + 10)%10 == 3:
        fold_3.append(normal_sents[i])
    elif (i + 10)%10 == 4:
        fold_4.append(normal_sents[i])
    elif (i + 10)%10 == 5:
        fold_5.append(normal_sents[i])
    elif (i + 10)%10 == 6:
        fold_6.append(normal_sents[i])
    elif (i + 10)%10 == 7:
        fold_7.append(normal_sents[i])
    elif (i + 10)%10 == 8:
        fold_8.append(normal_sents[i])
    elif (i + 10)%10 == 9:
        fold_9.append(normal_sents[i])
        


for i in range(len(racist_sents)):
    if (i + 10)%10 == 0:
        fold_0.append(racist_sents[i])
    elif (i + 10)%10 == 1:
        fold_1.append(racist_sents[i])
    elif (i + 10)%10 == 2:
        fold_2.append(racist_sents[i])
    elif (i + 10)%10 == 3:
        fold_3.append(racist_sents[i])
    elif (i + 10)%10 == 4:
        fold_4.append(racist_sents[i])
    elif (i + 10)%10 == 5:
        fold_5.append(racist_sents[i])
    elif (i + 10)%10 == 6:
        fold_6.append(racist_sents[i])
    elif (i + 10)%10 == 7:
        fold_7.append(racist_sents[i])
    elif (i + 10)%10 == 8:
        fold_8.append(racist_sents[i])
    elif (i + 10)%10 == 9:
        fold_9.append(racist_sents[i])

all_sents = [fold_0, fold_1, fold_2, fold_3, fold_4, fold_5, fold_6, fold_7, fold_8, fold_9]


test_dict = defaultdict(list) # Empty dictionary created
for i in range(10):
    test_dict[i]  = all_sents[i]

# This code sets the value of a key in the training data dictionary such that it is a list of sentences from folds which are not used for testing data
# e.g. if fold_0 is used for testing, then fold_1 to fold_9 will be used for training
train_dict = defaultdict(list)
for i in range(10):
    combined_list = []
    for idx in range(10):
        if idx != i:
            combined_list.extend(all_sents[idx])
    train_dict[i] = combined_list


## Tbh I am not 100% sure how this function works
def precision_recall(classifier, testfeats):
    refsets = collections.defaultdict(set)
    testsets = collections.defaultdict(set)
    for i, (feats,label) in enumerate(testfeats):
        refsets[label].add(i)
        observed = classifier.classify(feats)
        testsets[observed].add(i)
    precisions = {}
    recalls = {}
    for label in classifier.labels():
        precisions[label] = nltk.scorer.precision(refsets[label],testsets[label])
        recalls[label] = nltk.scorer.recall(refsets[label], testsets[label])
    return precisions, recalls


normal_precisions = []
normal_recalls = []
racist_precisions = []
racist_recalls = []


for fold in range(10):
    featuresets_test = [(features(sent), classification) for (sent,classification) in test_dict[fold]]
    featuresets_train = [(features(sent), classification) for (sent,classification) in train_dict[fold]]
    # Note: A list of (feature_dictionary, classification) tuples used as the argument for training the classifier
    classifier = nltk.NaiveBayesClassifier.train(featuresets_train)
    precisions,recalls = precision_recall(classifier,featuresets_test)
    # The stuff below appends the precision and recall values for both racist anf non racist sentences into empty lists
    normal_precisions.append(precisions['not racist'])
    normal_recalls.append(recalls['not racist'])
    racist_precisions.append(precisions['racist'])
    racist_recalls.append(recalls['racist'])


average_normal_precision = float(sum(normal_precisions))/10.0
average_normal_recall = float(sum(normal_recalls))/10.0
average_racist_precision = float(sum(racist_precisions))/10.0
average_racist_recall = float(sum(racist_recalls))/10.0
ratio = float(len(normal))/float(len(racist))

average_racist_precision_norm = float((average_racist_precision * 100) * ratio)/float(((average_racist_precision * 100) * ratio)+(100-(average_racist_precision*100)))


normal_f_score = 2*((average_normal_precision*average_normal_recall)/(average_normal_precision+average_normal_recall))
racist_f_score = 2*((average_racist_precision_norm*average_racist_recall)/(average_racist_precision_norm+average_racist_recall))


print('Normal Precision: ' + str(average_normal_precision))
print('Normal Recall: ' + str(average_normal_recall))
print('Racist Precision: ' + str(average_racist_precision_norm))
print('Racist Recall: ' + str(average_racist_recall))
print('Normal F-measure: ' + str(normal_f_score))
print('Racist F-measure: ' + str(racist_f_score))


### For demo purposes
all_sents2 = normal_sents + racist_sents

featuresets_train = [(features(sent), classification) for (sent,classification) in all_sents2]
classifier = nltk.NaiveBayesClassifier.train(featuresets_train)


def classify(sentence):
    input_features = features(sentence)
    classification = classifier.classify(input_features)
    return classification
    

while True:
    try:
        input_sentence = input('Type in a sentence as string:')
        classification = classify(input_sentence)
        if classification == 'not racist':
            print('This sentence is not racist \n \n \n')
        else:
            print('This sentence is racist. This might harm other people, please reconsider your message \n \n \n')
    except:
        print('\n Wrap the sentence in inverted commas please!')
        input_sentence = input('Type in a sentence as string:')
        classification = classify(input_sentence)
        if classification == 'not racist':
            print('This sentence is not racist \n \n \n')
        else:
            print('This sentence is racist. This might harm other people, please reconsider your message \n \n \n')













#z = 0
#while z == 0:
#    x = 'C:/Users/perio/Documents/hackathon.html'
#    raw_html = simple_get(x)
#    html = BeautifulSoup(raw_html, 'html.parser')
#    for x in html.select('input'):
#        input_sentence = x.text
#        print(input_sentence)
#
#def inputFunction():
#    sentence = input("Please type in your comment")