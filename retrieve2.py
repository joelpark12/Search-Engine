#Joel Park
#collaborated with Indiana Reed
#This implementation is very similar to the previous assignment, only adding the calculation for the
#tf-idf scores and some logic for sorting and printing. I used a dictionary to hold the document name
# and the tf-idf score for it. This brings me to the only real issue I had with the project: I wasn't really
# sure what formula for tf-idf I should use. The one we used in class is drastically different than the
# one on wikipedia. I chose to use the one in class. But really, that was the only problem. This assignment
# was only slight modifications to assignment 4.
import os
import nltk
import sys
import string
import pickle
import ast #This is for parsing the string from the file into a list
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from bs4 import BeautifulSoup #NLTK's documentation says to use beautifulsoup for parsing HTML
from nltk.stem.porter import *

import unittest



class testing(unittest.TestCase):
    def test_tfidf(self):
        d = {}
        d["basketball"] = ["1.html"]
        d["football"] = ["Something"]
        docs = {}
        docs["1.html"] = [1, "a;sldja"]
        docs["Something"] = [1, "asdfasf"]
        self.assertEqual(0, tf_idf("1.html", "basketball",  d, docs))
    def test_or(self):
        d = {}
        d["basketball"] = ["1.html"]
        d["football"] = ["Something"]
        docs = {}
        docs["1.html"] = [1, "a;sldja"]
        docs["Something"] = [1, "asdfasf"]
        self.assertEqual(set(["1"]),  mode_or(d, ["basketball"]))

    def test_and(self):
        d = {}
        d["basketball"] = ["1.html"]
        d["football"] = ["Something"]
        docs = {}
        docs["1.html"] = [1, "a;sldja"]
        docs["Something"] = [1, "asdfasf"]
        self.assertEqual(set([]), mode_and(d, ["basketball", "football"]))
        
reload(sys) #These two lines guarantee utf8
sys.setdefaultencoding("utf-8")
tokenizer = RegexpTokenizer('[a-z,A-Z]\w+') #Defines the tokenizer to only take words that start with letters.
stop = set(stopwords.words('english'))
st = PorterStemmer() #Makes the stemmer

def initdict(inp_dict, f): #Takes a dictionary as input and fills it with data from the input file (used for invind).
    for line in f:
        line = line.rstrip()
        info = line.split("\t")
        name = info[0]
        rest = info[1:][0] #These next three lines get it into a list
        n = len(rest)
        values = rest[1:n-1]
        inp_dict[name] = ast.literal_eval(values)
    return inp_dict

def initdocs(inp_dict, f): #Takes a dictionary as input and fills it with data from the input file (used for docs).
    for line in f:
        line = line.rstrip()
        info = line.split("\t")
        name = info[0]
        inp_dict[name] = info[1:]
    return inp_dict

def mode_or(d1, words): #Takes a list of words and the inverted index dictionary
    hits = set()
    for word in words:
        if word in d1:
            for i in d1[word]:
                if len(d1[word]) == 2: #This is needed because of a quirk in the
                        #way I split up the strings from inverted index. If there is only one document that a word
                        #appears in, the function does not make it a doubly nested list, hence this check.
                    try: #However, it could be that the doubly nested list is two long, meaning I need another
                        #check. Not the cleanest solution, but it works and is not overly expensive.
                        hits.add(d1[word][0])
                    except: #Sees if it is a hashable value, if not,  it must be two long, so adds both html pages.
                        hits.add(i[0])
                        hits.add(d1[word][1][0])
                else:
                    hits.add(i[0])
    return hits

#This uses the TF-IDF formula given in class for Quiz 1. 
def tf_idf(doc, term, d, docd): #Takes a document, a word, and a dictionary and computes the tf-idf score
    if term in d:     #The docd argument is used for the length of each document
        hits = d[term]                  
        tf = 0
        numdocs = len(hits)
        if len(hits) == 2:  #This is needed because of a quirk in the
                        #way I parsed the strings from inverted index. If there is only one document that a word
                        #appears in, the function does not make it a doubly nested list, hence this check.
            try: #Try to divide the first element by idf score.
                if hits[0] == doc:
                    tf = hits[1] / float(docd[doc][0])
                return tf/numdocs
            except: #If it fails, it must be a 2 long, doubly nested list. So add the score to the correct document.
                if hits[0][0] == doc:
                    tf = hits[0][1] / float(docd[doc][0])
                elif hits[1][0] == doc:
                    tf = hits[1][1] / float(docd[doc][0])
                return tf/numdocs
        else:
            for i in hits:
                if i[0] == doc:
                        tf = i[1] / float(docd[doc][0])
            return tf/numdocs
    else:
        return 0
        
    

def mode_and(d1, words): #Takes a list of words and the inverted index dictionary
    hits = set()
    first = True
    for word in words:
        check = mode_or(d1, [word]) #You can just run the or mode repeatedly and intersect the sets.
        if first:
            first = False
            hits = check #For the first one, you have to set the return set equal to the set of documents that
            #contain that term, because if you don't you'll always get None.
        else:
            hits = hits.intersection(check)
    return hits

def retrieve(words):
    try:
        invind = open("invindex.dat", 'r') #Opens the inverted index
    except:
        print "Cannot find file invindex.dat."
        return
    invdict = {} #Dictionary to hold inverted index
    try:
        docs = open("docs.dat", 'r') #Opens docs
    except:
        print "Cannot find file docs.dat."
        return
    docdict = {} #Dictionary to hold docs
    docdict = initdocs(docdict, docs) #Fills the dictionaries
    invdict = initdict(invdict, invind)
    docs.close()
    invind.close()
    for i in range(len( words)): #Fills the words array                                                             
        words[i] = words[i].translate(None, string.punctuation) #removes punctuation                                
        words[i] =  words[i].lower() #makes it all lowercase    
    stopped = [i for i in words if i not in stop] #Remove stopwords
    stemmed = [st.stem(i) for i in stopped]  #Stems using Porter Stemmer
    hits = mode_and(invdict, stemmed)
    scores = {} #Keeps the document and tfidf score
    for word in hits: #Puts the word in the dictionary with an initial tf-idf score of 0
        scores[word] = 0
    for i in stemmed:
        for j in hits:
                scores[j] += tf_idf(j, i, invdict, docdict)
    if len(scores.keys()) == 0:
        print "No pages found."
        return
    lst = sorted(scores, key=scores.__getitem__) #Sorts the keys from scores by the tfidf score
    k = 1#For numbering the entries
    lst = scores.keys()
    urls = {}
    for i in lst:
        if len(docdict[i]) > 2:
            urls[docdict[i][2]] = scores[i]
               # print str(k) + ".  " +  docdict[i][1] + "\t" + docdict[i][2] + "\t" + str(scores[i                 
    tfidf = open("tfidf", "w") #Put the tfidf dictionary in a pickled fil                                           
    pickle.dump(urls, tfidf)
    return urls

#Not intended to be called from commandline, but I've provided a way for you to see unittests
if __name__== '__main__' and len(sys.argv) == 1: #This will overwrite the pickle file!
    unittest.main()
