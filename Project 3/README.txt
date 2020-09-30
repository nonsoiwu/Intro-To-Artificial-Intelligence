How to use proj3.py
Nonso Iwu
CISC481
Project 3

To make a graph:

You have to have vertices first...

v1 = Vertex.new("1", "i")
v2 = Vertex.new("2", "i")
v3 = Vertex.new("3", "o")
v4 = Vertex.new("4", "o")

Where the first parameter is the name and the second is the type

To make the one layer graph from the homework
from these vertices:

g = Graph()
g.connect(v1, 1, v3)
g.connect(v1, 1, v4)
g.connect(v2, 1, v3)
g.connect(v2, 1, v4)

The Graph will automatically layer the vertices that you are trying to connect.
If you're connections are inconsistent, an Exception will be thrown

In order to classify on the graph, there are two options:

classify(g, [0,0])
classify(g, [0,0], True)

Where the "True" specifies if the logit function will be used instead of threshold

and similarly, you can update the weights using:

backProp(g, [0,0]) 
or
backProp(g, [0,0], True)

where the "True" specifies if the logit function will be used instead of threshold

After all this, you can see the results of the neural network by classifying the network again, and showing the output:

classify(g, [0,0])
g.showOutput()
or
classify(g, [0,0])
g.showOutput(True)

where the "True" specifies if the logit function will  be used instead of threshold

So a complete test would look like:

g = Graph()
v1 = Vertex.new("1", "i")
v2 = Vertex.new("2", "i")
v3 = Vertex.new("3", "o")
v4 = Vertex.new("4", "o")
g.connect(v1, 1, v3).connect(v1, 1, v4)
g.connect(v2, 1, v3).connect(v2, 1, v4)

g.show()
for i in range(5):
    classify(g, [0,0])
    backProp(g, [0,0])
    
    classify(g, [0,1])
    backProp(g, [0,1])

    classify(g, [1,0])
    backProp(g, [0,1])

    classify(g, [1,1])
    backProp(g, [1,0])

classify(g, [0,0])
g.showOutput()

classify(g, [0,1])
g.showOutput()

classify(g, [1,0])
g.showOutput()

classify(g, [1,1])
g.showOutput()