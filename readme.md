Requires PyGame

Run trafficView.py

Graph Objects:
Nodes = Necessary Bus Stops
Edges = Roads between stops

This simplified simulation optimizes one aspect of bus route efficiency, by defining new graph theory terms called "edge importance" and "path consistency." An edge's importance is equal to the number of shortest paths that it is a part of, because it is assumed that these edges will be used more in travel. Consistent paths are paths with little variance in edge importance. In this simulation, bus routes are chosen by selecting paths with high consistency, and using a reasonable number of total routes(the most consistent route is, after all, one edge long, but this leads to an unreasonable number of routes). The practical result is that optimal bus size is constant at each point on the route. This can be calculated to avoid overcrowding or underutilization of the bus. Once bus routes are selected on the graph, edge importance can be recalculated, using bus routes as paths, rather than edges. Many edges will have different importances. Some edges will not have bus routes, so more traffic will be routed along other edges. Some edges will have two bus routes, halving the effective importance of each route on that edge. This recalculation of importance necessitates redrawing of bus routes. This can be repeated until convergence or cycling occurs.