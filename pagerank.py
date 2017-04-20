#Pagerank
import os
import sys
import numpy as np
import pickle
import unittest

webgraph = {}
webgraph["A"]  = set(["B", "C", "D"])
webgraph["B"]  = set(["C", "D"])
webgraph["C"]  = set(["A"])
webgraph["D"]  = set(["A","C"])
webmatrix = np.matrix([[ 0.0, 1.0, 0.0,0.5],
                                        [ 0.33333333,  0.0, 0.5, 0.5 ],
                                        [ 0.33333333,  0.0,0.0, 0.0],
                                         [0.33333333,  0.0, 0.5,0.0 ]])

empty = {}

class testing(unittest.TestCase):
    def testmatrix(self):
        self.assertEqual(makematrix(webgraph).all(), webmatrix.all())

    def testrank(self):
        self.assertAlmostEqual(.3680377,pagerank(webgraph)['A'])
        self.assertAlmostEqual(.2880295,pagerank(webgraph)['C'])
        self.assertAlmostEqual(.1417868,pagerank(webgraph)['B'])
        self.assertAlmostEqual(.2021459,pagerank(webgraph)['D'])

    def testempty(self):
        self.assertEqual(pagerank(empty), {})
        
        


global gkeys #Saves the keys list globally because I need it in both makematrix and pagerank, and
                        #since dictionaries are unordered, the order is sometimes different, which messes up
                        #the final pagerank answer.

def makematrix(dic):
    keys = dic.keys()
    global gkeys
    gkeys = keys
    n = len(keys)
    ans = [[0 for x in range(n)] for y in range(n)]
    for i in range(n):
        for j in range(n):
            if keys[j] in dic[keys[i]]:
                if len(dic[keys[i]]) == 0:
                    ans[i][j] = 0.15 #If no outlinks, sets the value at this position to the dampening factor
                                                #This is done on the Princeton website shown in lab
                else:
                    ans[j][i] = float(1)/float(len(dic[keys[i]]))
    return np.matrix(ans)
        
def pagerank(dic): #Takes a dictionary, returns a dictionary of page : rank
    ans = {}
    if len(dic.keys()) == 0:
        return ans
    n = len(dic.keys())
    a = makematrix(dic)
    s = (len(dic.keys()), len(dic.keys()))
    b = np.matrix(np.ones(s))
    b =  (float(1) / float(n)) * b #Google matrix
    m = 0.85 * a + 0.15 * b
    v = (float(1) / float(n)) * np.ones((n,1)) #Will be the vector of ranks
    while sum(abs(m*v - v)) > 0.001:
        v = (m * v)
    v = m*v
    v = v.tolist()
    for i in range(len(gkeys)):
        ans[gkeys[i]] = v[i][0]
    rankfile = open("pageranks", "wb") #Put the pagerank dictionary in a pickled file
    pickle.dump(ans, rankfile)
    return ans
    
if __name__== '__main__': #This will overwrite the pickle file!
    unittest.main()


