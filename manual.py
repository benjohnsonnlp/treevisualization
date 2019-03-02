import pydot

graph = pydot.Dot(graph_type="graph")

for i in range(3):
    # we can get right into action by "drawing" edges between the nodes in our graph
    # we do not need to CREATE nodes, but if you want to give them some custom style
    # then I would recomend you to do so... let's cover that later
    # the pydot.Edge() constructor receives two parameters, a source node and a destination
    # node, they are just strings like you can see
    edge = pydot.Edge("king", "lord%d" % i)
    # and we obviosuly need to add the edge to our graph
    graph.add_edge(edge)

# now let us add some vassals
vassal_num = 0
for i in range(3):
    # we create new edges, now between our previous lords and the new vassals
    # let us create two vassals for each lord
    for j in range(2):
        edge = pydot.Edge("lord%d" % i, "vassal%d" % vassal_num)
        graph.add_edge(edge)
        vassal_num += 1

# ok, we are set, let's save our graph into a file
graph.write_png('example1_graph.png')