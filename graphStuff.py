from trafficControl import *


#Drawing Values
yellow = (255,255,0)
green  = (0, 255, 0)
blue = (0, 0, 255)
red = (255, 0, 0)
white = (255, 255, 255)
grey = (159, 182, 205)
black = (0, 0, 0)
colors = [yellow, green, blue, red, grey, black]
RADIUS = 5
WIDTH = 0

#Time Constants
dt = .03


#Graph Classes
class Vertex():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.neighbors = []
        self.occupants = []  #Just count the number

    def pos():
        return [x, y]

    def isEqual(self, other):
        if isinstance(other, Vertex):
            if self.x == other.x and self.y == other.y:
                return True
            else:
                return False
        else:
            False

    def notEqual(self,other):
        if self == other:
            return False
        else:
            return True

class Edge():
    '''Takes two vertices and returns an edge, with attributes:
        x, y, slope, length'''
    def __init__(self, a, b):
        if a.x < b.x:
            self.a = a
            self.b = b
        elif a.x == b.x:
            if a.y < b.y:
                self.a = a
                self.b = b
            else:
                self.a = b
                self.b = a
        else:
            self.a = b
            self.b = a
        self.length = sqrt((a.x - b.x)**2 + (a.y - b.y)**2)
        self.speed = 35    #pixels per second
        self.waitTime = self.length / self.speed
        self.x = midpoint(a, b)[0]
        self.y = midpoint(a, b)[1]
        self.slope = slope(self.a, self.b)
        self.demand = 0
        
        #update vertices
        a.neighbors.append(self)
        b.neighbors.append(self)

    def isEqual(self, other):
        if isinstance(other, Edge):
            if self.a.isEqual(other.a) and self.b.isEqual(other.b):  #relies on vertice comparators being overridden
                return True
            else:
                return False
        else:
            return False

    def notEqual(self, other):
        if self == other:
            return False
        else:
            return True

class Path():
    def __init__(self, edges):
        '''takes a list of edges and creates a path object, with attributes:
        length, demand, edges, vertices, stdDev
        '''
        
        #calculate totals
        self.length = 0
        self.demand = 0
        self.stdDev = None

        vertices = []
        for edge in edges:
            if edge.a not in vertices:
                vertices.append(edge.a)
            if edge.b not in vertices:
                vertices.append(edge.b)
        
        #assign attributes    
        self.edges = edges
        self.vertices = vertices  #to ensure that we hit every vertex


    def updateDemand(self, edgelist):
        for edge in self.edges:
            for e in edgelist:
             if e.isEqual(edge):
                self.length += e.length
                self.demand += e.length * e.demand
            
        demands = []
        for edge in self.edges:
            for e in edgelist:
                if e.isEqual(edge):
                    demands.append(e.demand)
        self.stdDev = stdDev(demands)

class BusRoute(Path):  #fix inheritance
    def __init__(self, path):
        self.path = path
            

#Traffic Classes
class Bus():
    def __init__(self, location):
        self.location = location
        self.timeSpent = 0  #increment this, and check it every loop, if on edge
        self.x = location.x
        self.y = location.y
        self.timer = 0
        self.oldlocation = location
        self.votes = dict()

    def advance(self, dt, nextStop):
        if isinstance(self.location, Vertex):
            if len(self.location.neighbors) > 0:
                self.x = self.location.x
                self.y = self.location.y
                self.timer = 0
                self.oldlocation = self.location    # help figure out which way to go on the edge
                self.location = nextStop  #go to edge
                self.votes = dict()  #we've left, no more voting
        else:
            self.timer += dt
            if self.oldlocation.x == self.location.a.x and self.oldlocation.y == self.location.a.y: #this hack is used because for some reason, the vertex gets copied every once in a while, and is not actually equal.  Should be actually fixed, I think.
                direction = 1
            else:
                direction = -1
            heading = unitVector(1 * direction, self.location.slope * direction)
            xVelocity = heading[0] * self.location.speed
            yVelocity = heading[1] * self.location.speed
            self.x += xVelocity * dt
            self.y += yVelocity * dt
            if self.timer >= self.location.length/self.location.speed:
                if direction == 1:
                    self.location = self.location.b
                else:
                    self.location = self.location.a

    def takeVote(self, edge):
        if edge in self.votes:
            self.votes[edge] += 1
        else:
            self.votes[edge] = 1
            


class Person():
    def __init__(self, location, destination):
        self.location = location
        self.x = location.x
        self.y = location.y
        self.destination = destination
        waitTime = 0
        path = pathfind(location, destination)
        self.expectedTime = path[0]
        if path[1] != None:
            self.next = path[1][0]
        else:
            self.next = None
        self.riding = False
        self.bus = None

    def findPath(self, destination):
        path = pathfind(self.location, destination)
        self.expectedTime = path[0]
        if path[1] != None:
            self.next = path[1][0]
        else:
            self.next = None

    def travel(self):
        if location == destination:
            self.riding = False
    #A bus arrives, and a hashmap is filled with votes for each edge.
    #The max votes wins, and the bus calls nextStop.
    #self.location is then equal to self.bus.location, until the bus
    #gets to a vertex.  When it does, we call pathfind again.

    def nextEdge(self):
        '''Sets the next edge for getting to the destination'''
        self.next = pathfind(location, destination)[1][0]
        #If the person is strict about the path, we don't have to recalculate
        #this.
    
    def nextStop(self, bus, nextStop):
        '''Determines whether the person will ride the bus, given the stop'''
        if nextStop == self.next:  #Do you want to get on the bus?
            self.riding = True
            self.bus = bus
            self.location = self.bus.location  #or x/y?
            #we have to run Person.updatePosition method every turn
            # There we can check if the bus has arrived at a vertex.  If so
            # He needs to get off and revote, but make sure not to miss it
            # if he wins the vote.
            
            


# Buttons
class Button():

    def __init__(self, text):
        self.pressed = False
        self.x = 50
        self.y = 50
        self.width = 50
        self.height = 50
        self.color = grey
        self.text = text
    
