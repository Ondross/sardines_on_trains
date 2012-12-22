#11.14.11
#Eve: integrated iteration (now it works!!) with Andrew's Andremas trafficControl in which he fixed a lot of bugs in original PathFinding algorithms we were using
#ais: modified uniqueDistances to find next route based on least vertices overlap (not edge overlap like before)

from math import *
from random import *
from copy import *

#Traffic Instruction Set

def connect(a, b):
    a.neighbors.append(b)
    b.neighbors.append(a)
    return edge(a, b)

def pathfind(location, destination):
    if location == destination:
        return (0, None)
    point = location
    traveling = True
    found = False
    visited = []
    waypoints = []
    waypoint = []
    distance = 0
    shortest = [10000000000]   #a hack
    while traveling == True:
        if point == destination:                     #if you've arrived
            waypoints.append([distance, waypoint])  #store path
            if distance < shortest[0]:                     #if it was the best path yet
                shortest = (distance, deepcopy(waypoint))  #remember it
            lastedge = waypoint.pop()                    #backtrack by one vertex and edge
            distance -= lastedge.length  # subtract the backtracked distance
            if point == lastedge.b:   #Go to the correct point
                point = lastedge.a    #start at the last item now
            else:
                point = lastedge.b
            backtracked = True         #We've started backtracking, (so we might be able to go back to previously forbidden edges)
        for edge in point.neighbors:    #Look at all neighbors
            found = False               #We don't know where to go yet
            if edge not in visited:     #If we haven't been there yet
                if edge.a == point:
                    point = edge.b
                else:
                    point = edge.a        #go there
                visited.append(edge)     #Mark it as visited
                waypoint.append(edge)     #add to path
                distance += edge.length    #sum distance
                found = True               
                backtracked = False        
                break                
        if found == False:                 #if we're at a deadend
            if len(waypoint) > 0:            #and we're not at the beginning
                lastedge = waypoint.pop()                    #backtrack by this vertex and edge
                distance -= lastedge.length  # remove the last distance
                if point == lastedge.b:
                    point = lastedge.a    #start at the last item now         if isclass(point, Vertex):
                else:
                    point = lastedge.b
                if backtracked == True:  #if this is the second backtrack in a row
                    visited.pop()        #allow us to go down some already visited edges.
                else:
                    backtracked = True
            else:
                return shortest

#Define Bus Routes

def find_shortest_path(start, end, path=[]):
    #returns the shortest path (in the form of a list of vertices) between start and end
    if start == end:
        return path
    if start.neighbors == []:
        return None
    shortest = None
    length_shortest = 0

    for edge in start.neighbors:
        path = path + [edge]

        if start.isEqual(edge.a):
            node = edge.b
        else:
            node = edge.a

        newpath = find_shortest_path(node, end, path)
        if edge not in path:
            #newpath is a list of edges
            
            if shortest == None:
                #creates initial shortest path
                shortest = newpath
            shortest_length = 0
            for edge in shortest:
                shortest_length += edge.length
            newpath_length = 0
            for edge in newpath:
                newpath_length += edge.length
            if newpath_length < shortest_length:
                #replaces shortest path if newpath is shorter
                shortest = newpath
    return shortest


def find_all_shortest_paths(vertices, Path):
    #creates dictionary of shortest paths with keys being the two variables that the path is between
    list_of_paths = dict()
    #goes through all possible pairs of vertices and returns the shortest path between them
    for i in range(len(vertices)-1):
        vert1 = vertices[i]
        for n in range((i+1), (len(vertices))):
            vert2 = vertices[n]
            key = '%s%s' %(vert1, vert2)
            list_of_paths[key] = Path(pathfind(vert1, vert2)[1])
    return list_of_paths
  
def weight_edges (list_of_paths, edgelist):
    #weights edges by creating a dictionary where key is edge and value is the number of occurences of edge in all shortest paths
    for edge in edgelist:
        edge.demand = 0
    all_pairs = list_of_paths.keys()
    weight = dict()
    for pair in all_pairs:
        edges = list_of_paths[pair].edges
        for edge in edges:
            found = False
            for k in weight.keys():
                if edge.isEqual(k):
                    weight[k] += 1
                    for e in edgelist:
                        if e.isEqual(edge):
                            e.demand += 1
                    found = True
                    break
            if found == False:
                weight[edge] = 1
                for e in edgelist:
                    if e.isEqual(edge):
                        e.demand = 1
    return weight

def thresholdStdDev2(paths, error):
    '''Makes a dictionary of path objects and their stdDevs, and returns
    the lowest set of them'''
    
    pathStdDev = dict()
    candidates = dict()
    for path in paths:
        pathStdDev[path] = path.stdDev

    lowest = min(pathStdDev.values())
    threshold = lowest + lowest * error

    for (k, v) in pathStdDev.items():
        if v <= threshold:
            candidates[k] = v
        if error > 1:
            return candidates

    if len(candidates) < 3:# there is no reason to limit the # we consider.
        error += .2
        candidates = thresholdStdDev(paths, error)
    return candidates

def thresholdStdDev(paths, error):
    '''Makes a dictionary of path objects and their stdDevs, and returns
    the lowest set of them'''
    
    pathStdDev = dict()
    candidates = dict()
    for path in paths:
        pathStdDev[path] = path.stdDev

    lowest = min(pathStdDev.values())
    threshold = lowest + error #lowest * error (CANNOT BE A PERCENT, SINCE 0 exists)

    for (k, v) in pathStdDev.items():
        if v <= threshold:
            candidates[k] = v

    return candidates

def maxDemand(paths):
    '''Takes a list of paths and returns the path with highest demand int(demand * ds)'''
    maxDemand = paths[0]
    for path in paths:
        if path.demand > maxDemand.demand:
            maxDemand = path
    return maxDemand

def hasIntersection(paths, routes):  #why is this failing?!
    '''looks at all paths, and returns the ones that intersect a bus route'''
    goodPaths = []
    for route in routes:
        for path in paths:
            for vertex in path.vertices:
                for stop in route.vertices:
                    if vertex.isEqual(stop) == True:
                        if path not in goodPaths:  #okay to use "in" here.
                            goodPaths.append(path)
    return goodPaths

def edgeOverlapLength(paths, routes):
    ''' Returns the path with the least distance of
    overlapping road.  If there are >1, it returns the longest'''
    overlapDict = dict()
    for route in routes:
        for path in paths:   #same edge can be counted twice
            for edge in path:
                if edge in route.edges:
                    overlapDict[path] += edge.length
    minOverlap = min(overlapDict.values())
    
    mins = []
    for key in overlapDict:
        if overlapDict[key] == minOverlap:
            mins.append(key)
    longest = mins[0]
    for path in mins:
        if path.length > longest.length:
            longest = path
    return longest


def uniqueDistances(paths, routes):
#modified on 11.14.11 to now find Unique Distances based on least vertices overlap NOT edge overlap

    '''Returns the path with the most unique vertices not currently
    covered by a bus route'''
    overlapDict = dict()
    for path in paths:
        overlapDict[path] = 0
        for route in routes:   #same edge can be counted twice
            for vertex in path.vertices:
                for vertex2 in route.vertices:
                    if vertex.isEqual(vertex2):
                        print("yes")
                        overlapDict[path] += 1  #count how many vertices overlap

    print(overlapDict)      
    mostUnique = paths[0]
    for path in overlapDict:                            #compare unique vertices of path to others in the dict
        if len(path.vertices) - overlapDict[path] >\
           len(mostUnique.vertices) - overlapDict[mostUnique]:
            mostUnique = path
            #print('greater')
        elif len(path.vertices) - overlapDict[path] ==\
           len(mostUnique.vertices) - overlapDict[mostUnique] and\
           overlapDict[path] < overlapDict[mostUnique]:
            mostUnique = path
            #print('equal')
    for edge in mostUnique.edges:                   
        mostUnique.demand +=edge.demand
             
    return mostUnique                               #return path with minimum vertex intersections with paths in routes


#basically same function as the shit above
'''
def uniqueVertices(paths, routes):
    ''''''Returns the path with the most waypoints that are not currently
    covered by a bus route''''''
    overlapDict = dict()
    for path in paths:
        overlapDict[path] = 0
        for route in routes:   #same edge can be counted twice
            for v in path.vertices:
                for verts in route.vertices:
                    if v.isEqual(verts):
                        overlapDict[path] += 1
                   
    mostUnique = paths[0]
    for path in paths:
        if len(path.vertices) - overlapDict[path] >\
           len(mostUnique.vertices) - overlapDict[mostUnique]:
            mostUnique = path
        elif len(path.vertices) - overlapDict[path] ==\
           len(mostUnique.vertices) - overlapDict[mostUnique] and\
           overlapDict[path] < overlapDict[mostUnique]:
            mostUnique = path
    return mostUnique

'''

def completeRoutes(routes, vertices):
    '''Takes a list of bus routes and vertices, and returns True
    if the bus routes hit every vertex'''
    for v in vertices:
        connected = False
        for route in routes:
            for stop in route.vertices:
                if v.isEqual(stop):
                    connected = True
        if connected == False:
            return False
    return True
            
        
    

def makeRoutes(vertices, edges, Path, error):
    '''Make optimal bus routes, given a set of desired locations/vertices,
    and roads/edges'''
    routes = []

    #get the first route
    paths = find_all_shortest_paths(vertices, Path)  #get all shortest paths k=2verts v=pathobject
    weight_edges(paths, edges)

    paths = list(paths.values())
    for path in paths:
        path.updateDemand(edges)
    candidates = list(thresholdStdDev(paths, error).keys())     #Find set with lowest StdDev
    firstRoute = maxDemand(candidates)          #Find the longest/most demanded
    routes.append(firstRoute)                   #Make a route
    paths.remove(firstRoute)            #remove it so it doesn't pollute thresholdStdDev

    #get the rest of the routes
    while completeRoutes(routes, vertices) == False: #Until all vertices are reached
        candidates = hasIntersection(paths, routes)     #Make sure new route reaches other route
        candidates = list(thresholdStdDev(candidates, error).keys())     #Find set with lowest StdDev
        
        newRoute = uniqueDistances(candidates, routes)       #Find path with most unique distance
        routes.append(newRoute)
        paths.remove(newRoute)
        
    return routes


def makeRoutes2(vertices, edges, edgedict, Path, error):
    '''Make optimal bus routes, given a set of desired locations/vertices,
    and roads/edges'''
    routes = []

    #get the first route
    paths = find_all_shortest_paths(vertices, Path)  #get all shortest paths k=2verts v=pathobject
    weight_edges(paths, edges)
    
    for edge in edges:
        print(edge.demand)
        if (edge.x, edge.y, edge.slope, edge.length) in edgedict:
            edge.demand = edge.demand/edgedict[(edge.x, edge.y, edge.slope, edge.length)]
            print(edgedict[(edge.x, edge.y, edge.slope, edge.length)])
        print(edge.demand)

    paths = list(paths.values())
    for path in paths:
        path.updateDemand(edges)
    candidates = list(thresholdStdDev(paths, error).keys())     #Find set with lowest StdDev
    firstRoute = maxDemand(candidates)          #Find the longest/most demanded
    routes.append(firstRoute)                   #Make a route
    paths.remove(firstRoute)            #remove it so it doesn't pollute thresholdStdDev

    #get the rest of the routes
    while completeRoutes(routes, vertices) == False: #Until all vertices are reached
        candidates = hasIntersection(paths, routes)     #Make sure new route reaches other route
        candidates = list(thresholdStdDev(candidates, error).keys())     #Find set with lowest StdDev
        
        newRoute = uniqueDistances(candidates, routes)       #Find path with most unique distance
        routes.append(newRoute)
        paths.remove(newRoute)
        
    return routes
    


def newEdges(routes, edges):
    new_edges = []
    #print type(edges)
    for route in routes:
        for edge in edges:
            for edge2 in route.edges:
                if edge.isEqual(edge2):
                    if edge not in new_edges:
                        new_edges.append(edge)  
    return new_edges           


def iterateRoutes(vertices, edges, routes, Path, error):
    new_edges = newEdges(routes, edges)
    print(new_edges)
    edgedict = dict()

    for route in routes:
        for edge in route.edges:
            if (edge.x, edge.y, edge.slope, edge.length) in edgedict:
                edgedict[(edge.x, edge.y, edge.slope, edge.length)] += 1
            else:
                edgedict[(edge.x, edge.y, edge.slope, edge.length)] = 1
    
    edges = new_edges
    print(edgedict)
    routes = makeRoutes2(vertices, edges, edgedict, Path, error)
    return routes, edges
    
    


#MapMaker
    #eventually include a map of boston, or a map that we know works well
def simpleGrid(x, y, scale, Vertex):
    vertices = []
    for i in range(x):
        for j in range(y):
            vertices.append(Vertex(i*scale + scale,j*scale + scale))
    return(vertices)
            

#Math
def midpoint(a, b):
    x = ceil((a.x + b.x)/2)
    y = ceil((a.y + b.y)/2)
    return [x, y]

def slope(a, b):
    if b.x != a.x:
        m = (b.y - a.y)/(b.x - a.x)
    else:
        m = 100000000000
    return m

def unitVector(x, y):
    mag = sqrt(x**2 + y**2)
    return ((x/mag), (y/mag))

def Mean(t):
    """Computes the mean of a sequence of numbers.

    Args:
        t: sequence of numbers

    Returns:
        float
    """
    if len(t) == 0:
        return 0
    else:
        return float(sum(t)) / len(t)

def stdDev(t, mu=None):
    """Computes the standard deviation of a sequence of numbers.

    Args:
        t: sequence of numbers

    Returns:
        float
    """
    if mu is None:
        mu = Mean(t)

    # compute the squared deviations, compute mean, and return the stdDev
    dev2 = [(x - mu)**2 for x in t]
    var = Mean(dev2)
    stdDev = sqrt(var)
    return stdDev
    

