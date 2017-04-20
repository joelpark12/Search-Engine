# Joel Park. Collaborated with Indiana Reed.
# Report
# The design decisions I made were very few. The skeleton code dictated what data structures, etc. to use.
# However, error handling was an important design decision. The crawler would get stuck when it was
# forbidden by robot.txt. So I looked around in the scrapy documentation and found the errback feature.
# This allowed me to see if there was an error and then keep going afterwards. It was extremely easy to
# comply with robots.txt, as you just have to change one of the settings to be True instead of False.
# Some problems encountered were making the crawler stop after getting through the specified number
# of pages, as well as handling errors. The first one was fixed by gaining a deeper understanding of how
# the parse function works, as well as moving the check on the number of printed pages from inside the
# for loop to outside. The second one was handled as described above.
from collections import deque
import scrapy
import os
import pickle

webgraph = {}

#===========
# Exceptions
#===========
class AlgoNotProvidedException(Exception):
    pass

class AlgoNotSupportedException(Exception):
    pass

class NumPageNotProvidedException(Exception):
    pass

class DestFolderNotProvidedException(Exception):
    pass

class UrlNotProvidedException(Exception):
    pass


#===========
# Containers
#===========
class Container(deque):
    ''' This is a class that serves as interface to the Spider '''
    def add_element(self, ele):
        ''' Add an element to the contain, always to the right '''
        return self.append(ele)

    def get_element(self):
        ''' This is an abstract method '''
        # One can also implement this using built-in module "abc",
        #   which stands for Abstract Base Class and produces a
        #   more meaningful error
        raise NotImplementedError

class Queue(Container):
    ''' Queue data structure implemented by deque '''
    def get_element(self):
        ''' Pop an element from the left '''
        return self.popleft()

class Stack(Container):
    ''' Stack data structure implemented by deque '''
    def get_element(self):
        ''' Pop an element from the right '''
        return self.pop()


#=======
# Spider
#=======
class ExampleSpider(scrapy.Spider):
    name = "IUB-I427-jgpark"
    allowed_domains = []
    start_urls = [
        'http://www.example.com/'
    ]

    def __init__(self, algo=None, num=None, directory=None, urls=None,
            *args, **kwargs):
        ''' Cutomized constructor that takes command line arguements '''
        super(self.__class__, self).__init__(*args, **kwargs)

        # check manditory inputs
        if num is None:
            raise NumPageNotProvidedException
        self.num_page_to_fetch = int(num) - 1

        if directory is None:
            raise DestFolderNotProvidedException
        self.dest_folder = directory

        if urls is None:
            raise UrlNotProvidedException
        self.start_urls = urls.split(',')

        # check algorithm choice, and construct container accordingly
        if algo is None:
            raise AlgoNotProvidedException
        elif algo == 'dfs':
            self.container = Stack()
        elif algo == 'bfs':
            self.container = Queue()
        else:
            raise AlgoNotSupportedException

        self.visited = set([urls])
        if not os.path.exists(self.dest_folder): #Makes the folder. Code obtained from stackoverflow.
            os.makedirs(self.dest_folder)
        self.counter = int(num) #This lets us count the number of pages more easily (Idea by Indiana Reed)
        return


     #Sees if there is an error and keeps going
    def errback(self, failure):# Contents identical to below without decrement
        if self.num_page_to_fetch > 0:
            curr = self.container.get_element()
            self.log(curr)
            go = True
            while go:
                if curr not in self.visited:
                    go = False
                    self.visited.append(curr)
                    yield scrapy.Request(curr, callback=self.parse, errback=self.errback)
                else:
                    curr = self.container.get_element()
                    
    def parse(self, response):
        fname = '%s.html' % str(self.counter-self.num_page_to_fetch)
        with open(self.dest_folder + 'index.dat', 'a') as f: #Writes to dat
            f.write(str(self.counter-self.num_page_to_fetch) + ".html " + str(response.url) + "\n")
            #if str(self.counter-self.num_page_to_fetch) + ".html" not in webgraph:
             #   webgraph[str(self.counter-self.num_page_to_fetch) + ".html"] = set([])
        with open(self.dest_folder + fname, 'wb') as f2: #Writes to the html files
            f2.write(response.body)
        webgraph[str(response.url)] = set([])
        try:
            for url in response.selector.xpath('//a/@href').extract(): #Extracts links
                url = response.urljoin(url)
                if self.num_page_to_fetch > 0:
                    webgraph[str(response.url)].add(url)
                    self.container.append(url)
        except:
            pass
        if self.num_page_to_fetch >  0: #Decrements the total number of pages left. 
            curr = self.container.get_element() #Current url
            go = True #This handles the case when the website is already in the visited list. If true, keeps going
            while go:
                if curr not in self.visited:
                    go = False
                    self.visited.add(url)
                    self.num_page_to_fetch -= 1
                    yield scrapy.Request(curr, callback=self.parse, errback=self.errback)
                else:
                    curr = self.container.get_element()
        else:
            pfile = open("webgraph", "wb")
            pickle.dump(webgraph, pfile)
   

