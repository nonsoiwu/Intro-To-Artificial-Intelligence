#Project 3 - CISC481
#University of Delaware
#Author: Nonso Iwu
from math import *

#=================================================
#                   UTILITY
#=================================================
def typeCheck(obj, typeObj, message):
    """
    Simple function for checking if an object is of a certain type

    Checks if obj is the same type as typeObj, if not, it will raise
        an exception with the message parameter
    """
    if type(message) != type(""):
        raise Exception('message not of type \'string\'')
    if type(obj) != type(typeObj):
        raise Exception(message)
    
class Queue:
    """
    Simple queue for program functions
    """
    def __init__(self):
        self.data = []

    def push(self, element):
        self.data.append(element)

    def pop(self):
        d = self.data.pop(0)
        return d

    def getLength(self):
        return len(self.data)

    def isEmpty(self):
        return len(self.data)==0
            
    def show(self):
        for d in self.data:
            print(d)

#=================================================
#                   VERTEX
#=================================================

class Vertex:
    """
    This class is used to build the Graph

    Attributes:
        name (str) to indentify the vertex
        edges (list) a collection of tuples: (weight (int), destination (Vertex)
        parents (int) amount of parent connections to the vertex
        edges (dict) connections to other Vertices
    """

    @staticmethod
    def new(name, t):
        """
        Factory method for creating a new Vertex

        Created mainly because messing with __init__ is unhealthy
        """
        typeCheck(name, "", "name is not of type 'str'")
        typeCheck(t, "", "t is not of type 'str'")
        v = Vertex()
        v.name = name
        if(t != "i" and t != "o" and t != "h"):
            return None
        v.type = t
        return v
    
    def __init__(self):
        self.name = ""
        self.type = "i"
        self.parents = 0
        self.edges = {}

    def addEdge(self, weight, newVertex):
        """
        Adds vertex 'newVertex' as a left connection to this vertex

        Returns true if it sucessfully added the new vertex
        Returns false otherwise
        """
        typeCheck(newVertex, Vertex(), 'newVertex is not of type \'Vertex\'')
        typeCheck(weight, 1, 'weight is not of type \'int\'')
        if self.name == newVertex.name:
            return False

        if self.edges.get(newVertex.name, None) == None:
            #Add new connection
            self.edges[newVertex.name] = (weight, newVertex)
            newVertex.parents+=1
            
            return True
        return False

    def show(self):
        """
        Prints this Vertex classes contents
        """
        buff = []
        for v in self.edges.values():
            buff.append((v[0], v[1].name))
        print(self.name+"("+str(self.parents)+")"+self.type+":", buff)

#=================================================
#                   GRAPH
#=================================================
class Graph:
    """
    Graph for representing the neural network

    Attributes:
        vertices (dict) collection of vertices in the graph
        input (list) collection of vertices of type [Input] "i"
        hidden (list) collection of vertices of type [Hidden] "h"
        output (list) collection of vertices of type [Output] "o"
        outputLayer (int) the layer where the output vertices reside
            Note: outputLayer is an ordinal value
        bias (Vertex) the arbitrary bias input for hidden/output vertices
    """
    def __init__(self):
        self.vertices = {}
        self.input = []
        self.hidden = []
        self.output = []
        self.outputLayer = -1
        self.bias = Vertex.new("bias", "i")
        self.vertices[self.bias.name] = (self.bias, [1], 0)

    def ghash(self, vert):
        """
        Used to get a hashed value of a Vertex class
        Params:
            vert (Vertex)
        Returns:
            (str) name of Vertex
        """
        typeCheck(vert, Vertex(), 'vert is not of type \'Vertex\'')
        return vert.name

    def get(self, vert):
        """
        Finds the data for a given Vertex class
        Params:
            vert (Vertex)
        Returns:
            (tuple) if vertex exists in the Graph
            None otherwise
        """
        typeCheck(vert, Vertex(), 'vert is not of type \'Vertex\'')
        return self.vertices.get(self.ghash(vert), None)
    
    def connect(self, v1, w, v2):
        typeCheck(v1, Vertex(), 'v1 is not of type \'Vertex\'')
        typeCheck(w, 1, 'weight is not of type \'int\'')
        typeCheck(v2, Vertex(), 'v2 is not of type \'Vertex\'')

        if v2.type == "i":
            raise Exception("Invalid Edge: Incoming edge to vertex of type 'i' [Input]")
        if v1.type == "o":
            raise Exception("Invalid Edge: Outgoing edge from vertex of type 'o' [Output]")
        
        v1result = self.vertices.get(self.ghash(v1), None)
        v2result = self.vertices.get(self.ghash(v2), None)
        if v1result == None:
            v1result = (v1, [], -1)
            self.vertices[self.ghash(v1)] = v1result

            #Add to inputs array
            if v1.type == "i":
                self.input.append(v1)
            else:
                self.bias.addEdge(1, v2)
                self.hidden.append(v1)

        if v2result == None:
            v2result = (v2, [], -1)
            self.vertices[self.ghash(v2)] = v2result

            #Add to outputs array
            self.bias.addEdge(1, v2)
            if v2.type == "o":
                self.output.append(v2)
            else:
                self.hidden.append(v2)

        #Checks to see if Nodes have been set up right
        leftLayer = v1result[2]
        rightLayer = v2result[2]
        if leftLayer == -1:
            if rightLayer == -1:
                #Both are not connected
                if v1.type == "i" and v2.type == "o":
                    #Set layering
                    v1result = (v1result[0], v1result[1], 0)
                    v2result = (v2result[0], v2result[1], 1)
                    self.vertices[self.ghash(v1result[0])] = v1result
                    self.vertices[self.ghash(v2result[0])] = v2result
                    self.outputLayer = 1

                elif v1.type == "h" and v2.type == "o":
                    #Complete network could have been made
                    v1.addEdge(w, v2)
                    #Try to assign layering
                    if not self.assignLayering():
                        raise Exception("Invalid Edge: Inconsistent layering in assignLayering()")
            else:
                #Left is not connected, Right is
                if v2.type == "o":
                    #connecting to an output
                    if v1.type == "i" and rightLayer>1:
                        raise Exception("Invalid Edge: Inconsistent Layering")
                v1result = (v1result[0], v1result[1], v2result[2]-1)
                self.vertices[self.ghash(v1result[0])] = v1result
        else:
            if rightLayer == -1:
                #Left is connected, Right is not connected
                if v2.type == "o":
                    if v1.type == "i":
                        if self.outputLayer != 1:
                            raise Exception("Invalid Edge: Breaking single layer structure")
                        self.outputLayer = leftLayer + 1
                    elif v1.type == "h":
                        if self.outputLayer != leftLayer+1:
                            raise Exception("Invalid Edge: Added output too soon.")
                    v2result = (v2result[0], v2result[1], leftLayer +1)
                    self.vertices[self.ghash(v2result[0])] = v2result
                if v2.type == "h":
                    v2result = (v2result[0], v2result[1], leftLayer +1)
                    self.vertices[self.ghash(v2result[0])] = v2result
                    #Recursively apply layering through child nodes
                    if not self.refactor(v2result[0]):
                        raise Exception("Invalid Edge: Inconsistent layering in refactor")
            else:
                #Left is connected, right is connected
                if leftLayer + 1 != rightLayer:
                    raise Exception("Invalid Edge: Jump from layer "+str(leftLayer)+" to layer "+str(rightLayer)+".")
        v1.addEdge(w, v2)
        return self

    def assignLayering(self):
        """
        Recursively assign layering starting from input vertices and
        flowing through children

        Returns:
            True, if no inconsistent layering was found
            False otherwise
        """
        for i in self.input:
            inputData = self.get(i)
            if i.name == "bias" or (inputData[2] != -1):
                continue
            self.vertices[self.ghash(i)] = (inputData[0], inputData[1], 0)
            if not self.refactor(i):
                return False
        return True
    
    def refactor(self, v):
        """
        Recusrively update layering starting from v and flowing through
            children
        Param:
            v (Vertex) vertex to start from
        Returns:
            True, if no inconsistent layering was found
            False, otherwise
        """
        vdata = self.get(v)
        if vdata == None:
            return True
        for childData in vdata[0].edges.values():
            c = self.get(childData[1])
            if c != None:
                if c[2] != -1 and c[2] != vdata[2]+1:
                    return False
                if c[0].type == "o":
                    if self.outputLayer != -1 and self.outputLayer != vdata[2]+1:
                        print("sheesh")
                        return False
                    self.outputLayer = vdata[2]+1
                self.vertices[self.ghash(c[0])] = (c[0], c[1], vdata[2]+1)
                #Recursive Call on child
                if not self.refactor(c[0]):
                    print("stopped")
                    return False
        return True

    def lshow(self):
        """
        Prints the graph in a layer by layer format
        This will not show parts of the graph that are unconnected or do not
            resemble a network
        """
        #Bias
        buff = []
        print("Bias:")
        b = self.get(self.bias)
        for e in b[0].edges.values():
            buff.append((round(e[0],4), e[1].name))
        print(b[0].name+"("+str(b[0].parents)+"):", buff, "Inputs:", b[1])

        for i in range(self.outputLayer+1):
            print("Layer "+str(i)+":")
            for v in self.vertices.values():
                if(v[0].name == "bias"):
                    continue
                if v[2] == i:
                    buff = []
                    for e in v[0].edges.values():
                        buff.append((round(e[0],4), e[1].name))
                    print(v[0].name+"("+str(v[0].parents)+"):", buff, "Inputs:", v[1])
    def show(self):
        """
        Prints the contents of a graph
        This will show vertices regardless of their connectivity
        """
        #Bias
        buff = []
        print("Bias:")
        b = self.get(self.bias)
        for e in b[0].edges.values():
            buff.append((round(e[0],4), e[1].name))
        print(b[0].name+"("+str(b[0].parents)+"):", buff, "Inputs:", b[1])  

        #Input Nodes
        print("Inputs:")
        for i in self.input:
            i = self.get(i)
            buff = []
            for e in i[0].edges.values():
                buff.append((round(e[0],4), e[1].name))
            print(i[0].name+"("+str(i[0].parents)+"):", buff, "Inputs:", i[1], i[2])

        #Hidden Nodes
        print("Hiddens:")
        for h in self.hidden:
            h = self.get(h)
            buff = []
            for e in h[0].edges.values():
                buff.append((round(e[0],4), e[1].name))
            print(h[0].name+"("+str(h[0].parents)+"):", buff, "Inputs:", h[1], h[2])

        #Output Nodes
        print("Outputs:")                
        for o in self.output:
            o = self.get(o)
            buff = []
            for e in o[0].edges.values():
                buff.append((round(e[0],4), e[1].name))
            print(o[0].name+"("+str(o[0].parents)+"):", buff, "Inputs:", o[1], o[2])
        print()

    def showOutput(self, sigmoid=False):
        """
        Shows the activated values of the outut nodes
        param:
            sigmoid: if True, the function will print the sigmoid activation value
                Otherwise, it is threshold activation
        """
        result = []
        print("Result:")
        for o in self.output:
            output = self.get(o)
            if sigmoid:
                print(output[0].name+":", logit(output[1]))
            else:
                print(output[0].name+":", activate(output[1]))
            result.append(sum(output[1]))
        
#=================================================
#               ACTIVATION FUNCS
#=================================================
def activate(inputs):
    if sum(inputs) >= 0:
        return 1
    return 0

def logit(inputs, deriv=False):
    if deriv:
        return logDeriv(inputs)
    return (1/(1+exp(-sum(inputs))))

def logDeriv(inputs):
    return logit(inputs)*(1-logit(inputs))

#=================================================
#               WEIGHT UPDATE
#=================================================

def weightUpdate(vert, outvert, In, outvertOut, expected, sigmoid=False):
    typeCheck(vert, Vertex(), 'vert is not of type \'Vertex\'')
    typeCheck(outvert, Vertex(), 'outvert is not of type \'Vertex\'')
    edge = vert.edges.get(outvert.name, None)
    if edge == None:
        return False
    difference = expected - outvertOut
    if sigmoid:
        newWeight = edge[0] + (difference * logit([outvertOut],True) * In)
    else:
        newWeight = edge[0] + (difference * In)
    vert.edges[outvert.name] = (newWeight, edge[1])
    return True

def classify(network, inputs, sigmoid=False):
    typeCheck(network, Graph(), 'network is not of type \'Graph\'')
    typeCheck(inputs, [], "inputs is not of type 'list'")

    #Check if inputs is the same size as the amount of inputs
    if len(inputs) != len(network.input):
        raise Exception("Input length inconsistency. Expected "+str(len(network.input))+", but got "+str(len(inputs))+".")
    
    #Empty read values
    for v in network.vertices.values():
        v[1].clear()

    #Create Queue
    q = Queue()

    #Apply Bias
    bias = network.get(network.bias)
    bias[1].append(1)
    q.push(network.bias)
    
    #Apply input values
    for i in range(len(inputs)):
        #Read values into inputs
        inp = network.get(network.input[i])
        inp[1].append(inputs[i])
        q.push(network.input[i])
    
    #Run through queue
    while not q.isEmpty():
        vert = q.pop()
        node = network.get(vert)
        #vert.show()

        #Use inputs and produce output
        if node[0].type == "i":
            out = sum(node[1])
        else:
            if(sigmoid):
                out = logit(node[1])
            else:
                out = activate(node[1])
        #out = activate(node[1])
        for e in vert.edges.values():
            dest = network.get(e[1])
            
            #Add weighted sum
            dest[1].append(e[0]*out)

            #Add to queue if all inputs have been received
            if len(dest[1]) == dest[0].parents:
                if(dest[0].type != "o"):
                    q.push(dest[0])
                    
    result = []
    for o in network.output:
        output = network.get(o)
        result.append(sum(output[1]))
    return result

def updateWeights(network, outputs):
    typeCheck(network, Graph(), 'network is not of type \'Graph\'')
    typeCheck(outputs, [], "outputs is not of type 'list'")

    #Check if size of output nodes is the same size as given outputs
    if len(outputs) != len(network.output):
        raise Exception("Output length inconsistency. Expected "+str(len(network.output))+", but got "+str(len(outputs))+".")
    
    #Fill the output dictionary
    expected = {}
    for i in range(len(outputs)):
        expected[network.output[i].name] = outputs[i]

    for v in network.vertices.values():
        vert = v[0]
        if(vert.type == "i"):
            vertOut = sum(v[1])
        else:
            vertOut = activate(v[1])
        #vertOut = sum(v[1])
        for e in vert.edges.values():
            if e[1].type == "o":
                dest = e[1]
                unweightedInput = vertOut
                expectedOutput = expected.get(e[1].name, None)
                actualOutput = activate(network.get(e[1])[1])
                weightUpdate(vert, dest, unweightedInput, actualOutput, expectedOutput)
                
    return network

def backProp(network, outputs, sigmoid=False):
    typeCheck(network, Graph(), 'network is not of type \'Graph\'')
    typeCheck(outputs, [], "outputs is not of type 'list'")

    #Check if size of output nodes is the same size as given outputs
    if len(outputs) != len(network.output):
        raise Exception("Output length inconsistency. Expected "+str(len(network.output))+", but got "+str(len(outputs))+".")

    if network.outputLayer == -1:
        return None

    errorVector = {}
    #Fill the error vector with output error delta
    for i in range(len(outputs)):
        deriv = 1
        if(sigmoid):
            vertOutput = logit(network.get(network.output[i])[1])
            deriv = logit(network.get(network.output[i])[1], True)
        else:
            vertOutput = activate(network.get(network.output[i])[1])
        error = outputs[i] - vertOutput
        errorVector[network.ghash(network.output[i])] = deriv * error
        
    # in_j = Summation of all the weighted activated inputs going into j
    # a = activate(in) or logit(in)
    # delta_output = logit_d(in_output) * error
    # delta_hidden = logit_d(in_hidden) * summation of all connections: weight to connection * delta of the connection

    #Find errors for hidden layer nodes
    for layer in reversed(range(1, network.outputLayer)):
        for v in network.vertices.values():
            #Find nodes in current layer
            if v[2] == layer:
                vert = v[0]

                #Get derivative
                deriv = 1
                if(sigmoid):
                    deriv = logit(v[1], True)
                totalError = []
                
                #Find the errors of node
                for e in v[0].edges.values():
                    errorVal = errorVector.get(network.ghash(e[1]))
                    #print(errorVal)
                    weightedError = e[0] * errorVal
                    totalError.append(weightedError)
                    
                #Place calculated error for this node in error dictionary
                errorVector[network.ghash(vert)] = deriv * sum(totalError)

    #Go through every node in network and update weights
    for v in network.vertices.values():
        vert = v[0]
        weightedInputs = v[1]
        
        #Retrieve this vertex output
        if vert.type == "i":
            vertOut = sum(v[1])
        else:
            if sigmoid:
                vertOut = logit(v[1])
            else:
                vertOut = activate(v[1])
                
        for e in v[0].edges.values():
            # new weight = curr_weight + 1 * a * delta(vertex)
            curr_weight = e[0]
            error = errorVector.get(network.ghash(e[1]), None)
            new_weight = curr_weight + (1 * vertOut * error)
            vert.edges[network.ghash(e[1])] = ( new_weight , e[1] )
    return network

