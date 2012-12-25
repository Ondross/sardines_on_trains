Requires PyGame

Run trafficView.py

Graph Objects:
Nodes = Necessary Bus Stops
Edges = Roads between stops


This simplified simulation optimizes one aspect of bus route efficiency by defining new graph theory terms called "edge demand" and "relative path demand consistency."

An edge's demand is equal to the number of shortest paths that it is a part of, because it is assumed that these edges will be used more in travel.

Relative path demand consistency is defined using the set of all shortest paths in the graph:

RPDC = 1 - 
<u>Standard_Deviation(edge_demand_in_path)</u>
(greatest_standard_deviation_among_shortest_paths)



Consistent paths are paths with little variance in edge demand. In this simulation, bus routes are chosen by selecting paths with high demand consistency, and using a reasonable number of total routes(the most consistent route is, after all, one edge long, but this leads to an unreasonable number of routes). The practical result is that optimal bus size is constant at each point on the route. This can be calculated to avoid overcrowding or underutilization of the bus. Once bus routes are selected on the graph, edge demand can be recalculated, using bus routes as paths, rather than edges. Many edges will have different importances. Some edges will not have bus routes, so more traffic will be routed along other edges. Some edges will have two bus routes, halving the effective demand of each route on that edge. This recalculation of demand necessitates redrawing of bus routes. This can be repeated until convergence or cycling occurs.