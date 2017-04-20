import pickle
import retrieve2
import index
import pagerank                                                                                                                             
import sys
#import subprocess                                                                                                                           
import os

def combine(pr, tf): #Takes the pagerank and tfidf dictionaries and combines the scores                                                      
    ans = {}
    for i in tf:
        if i in pr:
            ans[i] = tf[i] + pr[i] #Adds them together because both scores are lower than one and multiplying                                
                                                #them would decrease the overall score                                                       
    return ans

def search(words):
    try:
        ranks = open("pageranks", "r")
    except:
        try:
            webgraph = open("webgraph", "r")
        except:
            print("No crawling has been done.")
            return
        wgraph = pickle.load(webgraph)
        pagerank.pagerank(wgraph)
        ranks = open("pageranks", "r")
    pageranks = pickle.load(ranks)                                                                                                 
    if len(words) < 1:
        print "Please give at least one search query."
        return
    retrieve2.retrieve(words)
    scores = open("tfidf", "r") #This cannot fail if retrieve2 is present because it was run on the previous line                            
    tfidf = pickle.load(scores)
    together = combine(pageranks, tfidf)
    final = sorted(together, key=together.__getitem__)
    final.reverse()
    if len(final) > 25:
        final = final[0:25]
    return final

if __name__== '__main__' and len(sys.argv) > 1 and sys.argv[1] == "i427grading":
    print(search(["news"]))

