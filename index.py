#Joel Park
#Collaborated with Indiana Reed
#Report
#I used a dictionary hold the inverted index, with the keys as stemmed words and the values as the
#list of two-element lists where the first element is the document name and the second element is
#the number of times that that word appears in the document. Some of the design decisions included
#using a tokenizer that includes only words that start with letters. Another one was using the Porter
#Stemmer instead of another option like the Lancaster Stemmer. I chose this because it was discussed
# in class. I also made sure to force the encoding to UTF-8. While this sometimes means characters
#don't come out exactly right, it also means that it won't error out. The main difficulty I had was
#parsing the HTML file to get rid of the extra markup. I solved this by using BeautifulSoup's get_text
#function, which solved most of the problems. It did leave some strange things in the keys of the inverted
#index, like "i9ty0u26ql", but it doesn't make much of a difference in performance, and no one is going
#to search for that term. Even if they do, they'll find the one page it appears in.
import os
import nltk
import sys
import pickle
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from bs4 import BeautifulSoup #NLTK's documentation says to use beautifulsoup for parsing HTML
from nltk.stem.porter import *

#No real unit tests or refactoring to be done here. The index function just calls a bunch of
#pre-defined functions in a specific order and writes to a file. 

reload(sys) #These two lines guarantee utf8
sys.setdefaultencoding("utf-8")
tokenizer = RegexpTokenizer('[a-z,A-Z]\w+') #Defines the tokenizer to only take words that start with letters.
stop = set(stopwords.words('english'))
st = PorterStemmer() #Makes the stemmer

def index():
    folder = sys.argv[1]
    dat = sys.argv[2]
    if len(sys.argv) != 3:
        print "Please give two arguments."
        return
    try:
        f = open(folder + dat, 'r')
    except IOError:
        print "File or directory does not exist"
        return
    if os.path.getsize(folder + dat) == 0: #Checks if there is anything in the index file.
        print "Index file is empty. "
        return
    invind = open("invindex.dat", 'w') #Creates inverted index file
    docs = open("docs.dat", 'w') #Creates docs file
    invdict = {} #Creates dictionary that will populate inverted index
    for line in f:
        info = line.split()
        name = info[0]
        url = info[1]
        try:
            curr = open(folder + name, 'r') #opens current html file
        except IOError:
            print "HTML file in index does not exist. Halting execution."
            return
        data = curr.read()
        data = data.lower()
        soup = BeautifulSoup(data, "lxml")#Removes HTML markup
        data = soup.get_text()#Removes HTML markup
        tokens = tokenizer.tokenize(data)
        stopped = [i for i in tokens if i not in stop]
        stemmed = [st.stem(i) for i in stopped] #Uses the Porter stemmer
        for i in stemmed: #Loops through the words in the document
            if i not in invdict: 
                invdict[i] = [[name, 1]]
            else:
                exists = False #At this point, we know that the key i is in the invdict. But we have two more
                #conditions: if the html name is in the value of invidict[i] and if it is not. This is what this
                #flag is for and what the next checks are for.
                for j in invdict[i]:
                    if j[0] == name:
                        exists = True
                        j[1] += 1
                        break
                if not exists:
                    invdict[i] += [[name, 1]]
        docs.write(name + "\t"  + str(len(stemmed)) + "\t" + soup.title.string  + "\t" + url + "\n")
        curr.close()
    for key in invdict:
        invind.write(key + "\t"  + str(invdict[key])+ "\n")
    f.close()
    docs.close()
    invind.close()
    

if __name__== '__main__':
    index()
    
