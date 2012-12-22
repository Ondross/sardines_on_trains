#Andrew Heine 11/19/11
#The user can place intersections, roads, people, and buses.
#The people are given destinations, and the buses have different
#algorithms for taking the people to their destination.
#At the end, the people's happiness is evaluated based on
#actual travel time vs ideal travel time.

import pygame
from graphStuff import *
from pygame.locals import *


# initialise screen
pygame.init()
fpsClock = pygame.time.Clock()
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption('Bus Route Simulation')

# fill background
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill(white)

# display some text
font = pygame.font.Font(None, 24)
text = font.render("", 1, (10, 10, 10))
textpos = text.get_rect()
textpos.centerx = background.get_rect().centerx
background.blit(text, textpos)

# blit everything to the screen
screen.blit(background, (0, 0))
pygame.display.flip()

vertices = []
edges = []
buses = []
people = []
routes = []
buttons = [Button("Play  "), Button("Person/Dest"),\
           Button("Vertex/Edge"), Button("Bus"), Button("Make Routes"),\
           Button("Clear"), Button("+Thresh"), Button ("-Thresh")]
edgeon = False
time = 0
play = False
personWaiting = False
firstIteration = True
action = "graph"
lastButton = Button("Null")
error = 1
# event loop
while 1:
    buttonpress = False
    xoffset = 0
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            raise SystemExit
        if event.type == MOUSEBUTTONUP:
            if event.button == 3:
                if action == "graph":
                    for vertex in vertices:
                        if sqrt((event.pos[0] - vertex.x)**2 + (event.pos[1] - vertex.y)**2) < 5:
                            if edgeon == True:
                                edgeon = False
                                edges.append(Edge(vertex, myVertex))
                                myVertex = 0
                            else:
                                edgeon = True
                                myVertex = vertex
                elif action == "person":
                    if personWaiting == True:
                        for vertex in vertices:
                            if sqrt((event.pos[0] - vertex.x)**2 + (event.pos[1] - vertex.y)**2) < 5:
                                myPerson.destination = vertex
                                myPerson.findPath(vertex)
                                people.append(myPerson)
                                personWaiting = False
            else:
                for button in buttons:
                    if event.pos[0] > button.x and event.pos[0] < button.x + button.width\
                    and event.pos[1] > button.y and event.pos[1] < button.y + button.height:
                        if button.text != "Play  " and button.text != "Pause":
                            button.color = blue
                            lastButton.color = grey
                            lastButton = button
                        action = button.text
                        buttonpress = True
                        if button.text == "Play  ":
                                play = True
                                button.text = "Pause"
                        elif button.text == "Pause":
                                play = False
                                button.text = "Play  "
                        elif button.text == "Person/Dest":
                                action = "person"
                        elif button.text == "Vertex/Edge":
                                action = "graph"
                                firstIteration = True
                        elif button.text == "Bus":
                                action = "bus"
                        elif button.text == "+Thresh":
                                error += 1
                        elif button.text == "-Thresh":
                                error -= 1
                        elif button.text == "Make Routes":
                                if firstIteration == True:
                                    routes = []
                                    routes = makeRoutes(vertices, edges, Path, error)
                                    firstIteration = False
                                else:
                                    routes, edges1 = iterateRoutes(vertices, edges, routes, Path, error)
                        elif button.text == "Clear":
                                vertices = []
                                edges = []
                                buses = []
                                people = []
                                routes = []
                if buttonpress == False:
                    if action == "graph":
                        vertices.append(Vertex(event.pos[0], event.pos[1]))
                    elif action == "person":
                        for vertex in vertices:
                            if sqrt((event.pos[0] - vertex.x)**2 + (event.pos[1] - vertex.y)**2) < 5:
                                myPerson = Person(vertex, vertex)
                                personWaiting = True
                    elif action == "bus":
                        for vertex in vertices:
                            if sqrt((event.pos[0] - vertex.x)**2 + (event.pos[1] - vertex.y)**2) < 5:
                                buses.append(Bus(vertex))
        elif event.type == KEYDOWN:
            if event.key == K_b and len(vertices) > 0:
                buses.append(Bus(vertices[0]))
            if event.key == K_s and len(vertices) > 0:
                people.append(Person(choice(vertices),choice(vertices)))
            if event.key == K_r:
                print(pathfind(vertices[0], vertices[1]))
            if event.key == K_t:
                for vertex in simpleGrid(3,3,120, Vertex):
                    vertices.append(vertex)
            if event.key == K_ESCAPE:
                pygame.event.post(pygame.event.Event(QUIT))

    #Update Positions
    if play == True:
        for bus in buses:
            passengers = False
            if isinstance(bus.location, Vertex):
                for person in people:
                    if bus.location.x == person.location.x\
                       and bus.location.y == person.location.y and person.next != None:
                        passengers = True
                        bus.takeVote(person.next)
                if passengers == True:
                    nextStop = max(bus.votes,key = lambda a: bus.votes.get(a))
                else:
                    nextStop = choice(bus.location.neighbors)
            bus.advance(dt, nextStop)   #on to the next stop!

    #Draw Stuff
    screen.blit(background, (0, 0))
    for vertex in vertices:
        pygame.draw.circle(screen, black, (vertex.x, vertex.y), RADIUS, WIDTH)
        
    if edgeon == True:
        pygame.draw.circle(screen, yellow, (myVertex.x, myVertex.y), RADIUS + 2, WIDTH + 5)
        
    for edge in edges:
        pygame.draw.line(screen, black, (edge.a.x, edge.a.y), (edge.b.x, edge.b.y), 1)
        text = font.render(str(edge.demand), True, black, white)
        textRect = (edge.x, edge.y)
        screen.blit(text,textRect)
        
    for bus in buses:
        pygame.draw.circle(screen, (0, 0, 255), (round(bus.x), round(bus.y)), RADIUS, WIDTH)
    i = 0
    for route in routes:
        for edge in route.edges:
            pygame.draw.line(screen, colors[i%6], (edge.a.x, edge.a.y + 2 * (i + 1)), (edge.b.x, edge.b.y + 2 * (i + 1)), 3)
        print(route.stdDev)
        i += 1
    for button in buttons:
        text = font.render(button.text, True, (0,0,0), button.color)
        textRect = (10 + xoffset, 10)
        button.x = (10 + xoffset)
        button.y = (10)
        button.width = text.get_rect()[2]
        button.height = text.get_rect()[3]
        screen.blit(text, textRect)
        xoffset += button.width + 10
    text = font.render("Threshold: "+ str(error), True, black, white)
    textRect = (10, 35)
    screen.blit(text, textRect)
    lineup = 0
    for person in people:
        pygame.draw.rect(screen, (255, 0, 0), (person.x + 5 * sin(lineup), person.y + 5 * cos(lineup), RADIUS, RADIUS))
        lineup += 1

        
    fpsClock.tick(100/dt)
    time += dt
    pygame.display.flip()

