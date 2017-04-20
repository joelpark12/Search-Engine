#Joel Park
# Report
# The only major design decision I had to make was how to represent the graph. Normally, graphs
# are just represented by adjancency lists, but with the list containing edge names and weights, my
# adjacency lists would have to have those encoded in them, or be stored separately. This is why
# I made another dictionary called edges that has keys that are (vertex v, vertex u) tuples, and the
# values are a list of [edge weight, edge name]. The only major problem was translating from psuedocode
# into Dijkstra's algorithm. Other than that, it was smooth sailing, and that problem was just solved
# through trial and error. BFS and Best first both return fairly decent driving directions. Depth on the
# other hand, does not. For example, depth returns a path that is over 7000 miles long to go from
# Bloomington to Chicago, while breadth and best do 220 and 209 miles respectively. Best first is almost
# always shorter than breadth, but it has more road segments. So I would rather follow breadth in general
# because it would be an easier drive, even though it is a bit longer. Discussed code with Indiana Reed.

import Queue
import sys
roads = {}
edges = {}

def initialize():
    f = open('road-segments.txt', 'r')
    for line in f:
        temp = line.split(" ")
        if temp[0] in roads:
            roads[temp[0]] += [temp[1]]
        elif temp[0] not in roads:
            roads[temp[0]] = [temp[1]]
        if temp[1] in roads:
            roads[temp[1]] += [temp[0]]
        elif temp[1] not in roads:
             roads[temp[1]] = [temp[0]]
        edges[(temp[0], temp[1])] = [temp[2], temp[3].strip()]
        edges[(temp[1], temp[0])] = [temp[2], temp[3].strip()]
    f.close()

#Breadth First Search. Pseudocode gotten from C343 Textbook
def bfs(start, end):
    queue = [[start]]
    seen = set() #Have to make a list of seen vertices in case there is a cycle, and there will be a cycle.
    while queue:
        path = queue.pop(0)
        v = path[-1]
        if v == end:
            return path
        elif v not in seen:
            for n in roads.get(v): #Gets the list of vertices connected to this vertex
                path2 = list(path)
                path2.append(n)
                queue.append(path2)
            seen.add(v)

#Depth First Search
def dfs(start, end):
    stack = [[start]]
    seen = set() #Have to make a list of seen vertices in case there is a cycle, and there will be a cycle.
    while stack:
        path = stack.pop() #Same as breadth first, just stack instead of queue
        v = path[-1]
        if v == end:
            return path
        elif v not in seen:
            for n in roads.get(v): #Gets the list of vertices connected to this vertex
                path2 = list(path)
                path2.append(n)
                stack.append(path2)
            seen.add(v)

#minimizes distance traveled with Dijkstra's Algorithm. 
def best(start, end):
    q = Queue.PriorityQueue()
    dist = {} #Makes two new dictionaries to hold distances and parent nodes
    prev = {}
    for v in roads: #Populates the two new dictionaries 
        dist[v] = sys.maxint
        prev[v] = None
    dist[start] = 0
    for v in roads: #Populates the queue
        q.put([dist[v], v, prev[v]])
    while q:
        u = q.get() #Gets the current node
        curr = u[0]
        v = u[1]
        if v == end:
            s = [] #The stack that will be the final path
            while prev[v] != None: #This goes back up the graph until there is no node to go back to.
                s.append(v)
                v = prev[v]
            s.append(v)
            s.reverse() #Then reverses the stack
            return s
        else:
            for x in roads.get(v):
                alt = dist[v] + int(edges[(v,x)][0]) #This means that a shorter path from start to v has been found
                if alt < dist[x]:
                    dist[x] = alt
                    prev[x] = v
                    q.put([dist[x], x, prev[x]])
    return "This shouldn't happen" #Should never get here



def router(start, end):
    initialize()
    ans = best(start,end)
    count = 0
    distance = 0
    for i in xrange(len(ans)-1):
        rd = edges[(ans[i], ans[i+1])]
        print "<p>Take " + str(rd[1]) + " for " + str(rd[0]) + " miles to " + str(ans[i+1]) + ""
        count += 1
        distance += int(rd[0])
    print "Total road segments: " + str(count) + "\n"
    print "Total distance: " + str(distance) + "\n"

