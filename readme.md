# Sardines on a Train

#### To Run:
Install PyGame
Run trafficView.py

### Description of Project:
This simplified simulation describes bus route systems using graphes and aims to reduce over/under-use of bus seating by predicting the number of passengers that will use each leg of a bus route and designing individual routes with consistent usage between each stop. This allows one bus size to fit the demands of a route.

Graph Nodes = Bus Stops
Graph Edges = Passages between stops


To begin optimizing for consistent bus usage, we define new graph theory terms called "edge demand" and "relative demand consistency" of a path, or set of edges.

Edge demand is equal to the number of shortest paths that an edge is part of. It is assumed that these edges will be used more in travel.

Relative demand consistency is a measure of how little variance there is in the demand of edge's in a path. It is defined using the set of all shortest paths in the graph:

![Relative Path Demand Consistency](https://github.com/Ondross/sardines_on_trains/blob/master/rdc.gif?raw=true)

Using these terms, bus routes are chosen in the following manner (12/25/12: I can't remember if this is 100% accurate. It is something like this.):

#### Defining the bus routes
The most consistent bus routes will obviously be those of path length 1. We did not want to complicate the system and obfuscate our concepts, but we did want to make the simulation somewhat realistic. Therefore, we developed a simple set of rules for selecting consistent bus routes of reasonable length. I'm especially happy to hear feedback on this part.

##### For the first route:
1. Find all shortest paths
2. Find the relative path demand consistency of the longest shortest path. 
3. Throw out shortest paths that have less consistency than this value.
4. The first bus route is the route that, of the remaining routes, has the highest total demand.

##### For the rest of the routes:
1. Use steps 1-3 of the above process
2. Filter out paths that do not intersect at least once with existing routes
3. The next bus route is the route that, of the remaining routes, has the highest total demand, not counting where it overlaps other routes.

Ostensibly, this leads to bus routes that can optimally use a single size of bus without it being undercrowded or overutilized. HOWEVER!

### Iterating on Bus Routes:
Once bus routes are selected on the graph, edge demands have changed, because only bus routes are paths, rather than any edges. Some edges will not have bus routes, so more traffic will be routed along other edges. Some edges will have two bus routes, halving the effective demand of each route on that edge. This recalculation of demand necessitates redrawing of bus routes. As this simulation shows, sometimes this leads to convergence, and other times it leads to cycling.

### Future Direction:
Many things could have been done differently in this project, particularly in the bus route selection algorithm. Additionally, one could combine this with current transit design algorithms.

The application is designed to be expandable to include measurement systems that include people and buses that traverse the graph. These people could report on their length of travel time and measure the success of different algorithms.

Much theoretical work is left undone. For example, one could prove that different kinds of graphs lead to converging routes or cycling routes.