import copy

"""

Author: Nonso Iwu
CISC481 Fall 2019 - Project 1

The scripts to run certain problems are commented out on the bottom of this
    file
"""

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

#==================================================================================
#                                    VERTEX CLASS
#==================================================================================

class vertex:
    """
    This class is used to build the connectivity list
    It has 3 attributes:
    
    name (a String to indentify the vertex)
    left (array of other Vertex classes)
    right (array of other Vertex classes)
    """
    def __init__(self):
        self.name = "None"
        self.left = []
        self.right = []

    def addLeft(self, newVertex):
        """
        Adds vertex 'newVertex' as a left connection to this vertex

        Returns true if it sucessfully added the new vertex
        Returns false otherwise
        """
        typeCheck(newVertex, vertex(), 'newVertex is not of type \'vertex\'')
        if self.name == newVertex.name:
            return False
        for s in self.left:
            if s.name == newVertex.name:
                return False
        self.left.append(newVertex)
        return True

    def addRight(self, newVertex):
        """
        Adds vertex 'newVertex' as a right connection to this vertex

        Returns true if it sucessfully added the new vertex
        Returns false otherwise
        """
        typeCheck(newVertex, vertex(), 'newVertex is not of type \'vertex\'')
        if self.name == newVertex.name:
            return False
        for s in self.right:
            if s.name == newVertex.name:
                return False
        self.right.append(newVertex)
        return True

    def leftToString(self):
        """
        Formats the left connections list into a string
        """
        temp = "["
        for s in self.left:
            temp += (s.name + ", ")
        
        if len(self.left)>0:
            temp = temp[:-2]

        temp += "]"
        return temp

    def rightToString(self):
        """
        Formats the right connections list into a string
        """
        temp = "["
        for s in self.right:
            temp += (s.name + ", ")
        
        if len(self.right)>0:
            temp = temp[:-2]

        temp += "]"
        return temp

#==================================================================================
#                                    CONNECTIVITYLIST CLASS
#==================================================================================

class connectivityList:
    """
    This is a framework that sits on top of a web of vertex class

    It is mainly an interface for manipulating and collecting information
        on a vertex.

    Characteristics:
        Only contains unique vertex classes
        Handles connecting 2 different vertex classes

    It only has the attribute 'vertices' which is an array of vertex classes
        because it is an interface rather than its own full entity 
    """
    
    def __init__(self):
        self.vertices = []

    def getVertex(self, vertexName):
        """
        Returns a vertex within the list with the name specified by 'vertexName'
        Returns None if there was no vertex found with that name
        """
        if type(vertexName) != type(""):
            raise Exception('vertexName not of type \'string\'')
        for s in self.vertices:
            if s.name == vertexName:
                return s
        return None

    def clearVertex(self, vertexName):
        """
        Removes the vertex specified by 'vertexName' and all of its connections within
            the connectivityList
        """
        temp = self.getVertex(vertexName)
        i = 0
        if temp == None:
            return False
        else:
            self.vertices.remove(temp)

            for s in self.vertices:
                s.left.remove(temp)
                s.right.remove(temp)
        return True
    
    def addVertex(self, vertexName):
        """
        Adds a new vertex with the name 'vertexName' to the connectivity list
        """
        if type(vertexName)!=type(""):
            raise Exception('vertexName not of type \'string\'')

        newVertex = self.getVertex(vertexName)
        if(newVertex == None):
            #Create new vertex
            newVertex = vertex()
            newVertex.name = vertexName
            self.vertices.append(newVertex)
            return True
        return False

    def connectLeft(self, vertexName, connectName):
        """
        Adds the vertex with name specified by connectName to the left list
            for the vertex specified by vertexName
        """
        if type(vertexName)!=type(""):
            raise Exception('vertexName not of type \'string\'')
        if type(connectName)!=type(""):
            raise Exception('connectName not of type \'string\'')

        thisVertex = self.getVertex(vertexName)
        connectVertex = self.getVertex(connectName)
        if(thisVertex == None or connectVertex == None):
            return False
        else:
            thisVertex.addLeft(connectVertex)
            return True

    def connectRight(self, vertexName, connectName):
        """
        Adds the vertex with name specified by connectName to the right list
            for the vertex specified by vertexName
        """
        if type(vertexName)!=type(""):
            raise Exception('vertexName not of type \'string\'')
        if type(connectName)!=type(""):
            raise Exception('connectName not of type \'string\'')

        thisVertex = self.getVertex(vertexName)
        connectVertex = self.getVertex(connectName)
        if(thisVertex == None or connectVertex == None):
            return False
        else:
            thisVertex.addRight(connectVertex)
            return True
        
    def show(self):
        """
        Prints the vertices and their connections within the connectivity list 
        """
        temp = []
        rName = ""
        lName = ""

        string = ""
        for s in self.vertices:
            print(s.name+" -> L: "+s.leftToString()+" R: "+s.rightToString())

    def equals(self, oCL):

        if len(self.vertices) != len(oCL.vertices):
            return False

        for i in range(len(self.vertices)):
            if(self.vertices[i].name != oCL.vertices[i].name):
                return False
            if(len(self.vertices[i].left) != len(oCL.vertices[i].left)):
                return False
            if(len(self.vertices[i].right) != len(oCL.vertices[i].right)):
                return False

            #Go through left lists
            for j in range(len(self.vertices[i].left)):
                if(self.vertices[i].left[j] != oCL.vertices[i].left[j]):
                    return False
            
            #Go through right lists
            for k in range(len(self.vertices[i].left)):
                if(self.vertices[i].left[k] != oCL.vertices[i].left[k]):
                    return False
                
        return True
    
def cList():
    """
    A shorter initializer for a connectivityList class
    """
    return connectivityList()

#==================================================================================
#                                    CAR CLASS
#==================================================================================

class car:
    
    """
        A class that I used to hold information on a car on a track
        This was mainly created so I steer clear of any semantic errors
    """
    
    def __init__(self):
        self.name = ""
        self.position = None

    def setPosition(self, vertexObj):
        typeCheck(vertexObj, vertex(), 'vertexObj is not of type \'vertex\'')
        self.position = vertexObj

    def setName(self, newName):
        typeCheck(newName, "", 'newName is not of type \'string\'')
        self.name = newName

    def equals(self, oCar):
        typeCheck(oCar, car(), 'oCar is not of type \'car\'')
        if(self.name !=  oCar.name):
            return False

        if(self.position.name != oCar.position.name):
            return False
        return True

#==================================================================================
#                                       STATE CLASS
#==================================================================================

class state:

    """
    The state class has 5 attributes:

    yardImage (an Array) a 'picture' of the tracks in a specific yard
    yardVSize (an Int) the amount of vertex classes from the yard that generates
        the state
    yardCSize (an Int) the amount of car classes from the yard that generates the state
    enginePosition (a String) telling the name of the vertex class the engine is on
    rules (a ConnectivityList) giving a guidelines for a move from a state

    A state class should never be constructed on it's own.
    In this program, it is generated by the yard object 
    """
    
    def __init__(self):
        self.yardImage = []
        self.yardVSize = 0
        self.yardCSize = 0
        self.enginePosition = None
        self.rules = None

    def show(self):
        for y in self.yardImage:
            temp = []
            for yt in y[1]:
                temp.append(yt.name)
            print(y[0]+" | "+str(temp))

    def validateAction(self, action):
        typeCheck(action, ("a","tuple"), "action is not of type \'tuple\'")

        #Check length
        if(len(action)!=3):
            return False
        
        #Check contents
        if (action[0]!="L" and action[0]!="R"):
            return False

        found1 = False
        found2 = False
        for t in self.yardImage:
            if t[0] == action[1]:
                found1 = True
            if t[0] == action[2]:
                found2 = True
            if found1 and found2:
                return True
        
        return False

    def equals(self, otherState):
        typeCheck(otherState, state(), "otherState is not of type \'state\'")

        if(self.yardVSize != otherState.yardVSize):
            #print("yardVSize")
            return False

        if(self.yardCSize != otherState.yardCSize):
            #print("yardCSize")
            return False

        if self.enginePosition != otherState.enginePosition:
            #print("enginePosition")
            return False

        if len(self.yardImage) != len(otherState.yardImage):
            #print("yardImage Size")
            return False

        #Go through each index of yard image in both states and see if they are
        #same

        for i in range(len(self.yardImage)):
            if(self.yardImage[i][0]!=otherState.yardImage[i][0]):
                #print(str(self.yardImage[i][0]) + " vs " +  str(otherState.yardImage[i][0]))
                return False
            if(len(self.yardImage[i][1]) != len(otherState.yardImage[i][1])):
                #print(str(self.yardImage[i][1]) + " vs " +  str(otherState.yardImage[i][1]))
                return False
            for j in range(len(self.yardImage[i][1])):
                if not self.yardImage[i][1][j].equals(otherState.yardImage[i][1][j]):
                    #print(str(self.yardImage[i][1][j]) + " vs " +  str(otherState.yardImage[i][1][j]))
                    return False
        return True

    def deepEquals(self, otherState):
        typeCheck(otherState, state(), "otherState is not of type \'state\'")

        if(not self.equals(otherState)):
            return False

        return self.rules.equals(otherState.rules)

    def generateYard(self):
        y = yard(self.rules)
        for t in self.yardImage:
            #print("done")
            #y.tracks.append(t)
            for tt in t[1]:
                if(tt.name == "*"):
                    y.setEngine(t[0])
                else:
                    y.addCar(tt.name,t[0])
        return y
        
#==================================================================================
#                                    YARD CLASS
#==================================================================================

class yard:

    """
    The main class of this project
    The yard class contains 3 attributes:
        connectivityList (a ConnectivityList) the guidelines for the yard movements
        cars (a list of Cars) the cars on this yard
        tracks (a list of lists of cars) a high level representation of the cars in
            the yard

    A state can be generated from this yard
    """
    
    def __init__(self, cList):
        self.connectivityList = cList
        self.cars = [car()]
        self.cars[0].setName("*")
        self.tracks = []
        for v in self.connectivityList.vertices:
            self.tracks.append((v.name,[]))

    def getCar(self, carName):
        """
        Returns a car within the list with the name specified by 'carName'
        Returns None if there was no car found with that name
        """
        typeCheck(carName, "", 'carName not of type \'string\'')
        for c in self.cars:
            if c.name == carName:
                return c
        return None
    
    def addCar(self, carName, vertexName):
        typeCheck(carName, "", 'carName not of type \'string\'')
        typeCheck(vertexName, "", 'vertexName not of type \'string\'')

        initVertex = self.connectivityList.getVertex(vertexName)

        if(self.getCar(carName) != None):
            print("Car with name '"+carName+"' already exists")
            return False
        if(initVertex == None):
            print("Vertex with name '"+vertexName+"' does not exist")
            return False

        if carName == "*":
            print("Car name '*' is reserved for engine car")
            return False

        newCar = car()
        newCar.setName(carName)
        newCar.setPosition(initVertex)
        self.cars.append(newCar)
        for t in self.tracks:
            if(t[0] == initVertex.name):
                t[1].append(newCar)
                break
        return True

    def setEngine(self, vertexName):
        typeCheck(vertexName, "", 'vertexName not of type \'string\'')
        
        vert = self.connectivityList.getVertex(vertexName)
        if vert == None:
            print("Vertex with name '"+vertexName+"' does not exist")
            return False
        
        engine = self.getCar("*")
        engine.setPosition(vert)
        for t in self.tracks:
            if(t[0] == vert.name):
                t[1].append(engine)
                break
        return True

    def getTrack(self, vertexName):
        typeCheck(vertexName, "", 'vertexName not of type \'string\'')
        vert = self.connectivityList.getVertex(vertexName)
        if vert == None:
            print("Vertex with name '"+vertexName+"' does not exist")
            return None

        for t in self.tracks:
            if t[0] == vertexName:
                return t
            
    def moveLeft(self, y, x):
        typeCheck(y, "", 'y not of type \'string\'')
        typeCheck(x, "", 'x not of type \'string\'')

        tracky = self.getTrack(y)
        trackx = self.getTrack(x)
        #Check if inputs are valid
        if(tracky == None):
            print("Track '"+y+"' does not exist")
            return False
        if(trackx == None):
            print("Track '"+x+"' does not exist")
            return False
        engine = self.getCar("*")
        if(engine.position.name != y and engine.position.name != x):
            print("Engine '*' is not on either track '"+y+"' or '"+x+"'.")
            return False

        if(len(tracky[1])>0):
            moveCar = tracky[1].pop(0)
            moveCar.position = self.connectivityList.getVertex(trackx[0])
            trackx[1].append(moveCar)
        else:
            print("Track '"+y+"' is empty")            
        return True

    def moveRight(self, x, y):
        typeCheck(y, "", 'y not of type \'string\'')
        typeCheck(x, "", 'x not of type \'string\'')

        trackx = self.getTrack(x)
        tracky = self.getTrack(y)
        #Check if inputs are valid
        if(tracky == None):
            print("Track '"+y+"' does not exist")
            return False
        if(trackx == None):
            print("Track '"+x+"' does not exist")
            return False
        engine = self.getCar("*")
        if(engine.position.name != y and engine.position.name != x):
            print("Engine '*' is not on either track '"+y+"' or '"+x+"'.")
            return False

        if(len(trackx[1])>0):
            moveCar = trackx[1].pop(-1)
            moveCar.position = self.connectivityList.getVertex(tracky[0])
            tracky[1].insert(0, moveCar)
        else:
            print("Track '"+x+"' is empty")
        return True

    def generateState(self):
        s = state()

        s.yardVSize = len(self.connectivityList.vertices)
        s.yardCSize = len(self.cars)
        s.rules = self.connectivityList
        s.enginePosition = self.getCar("*").position.name
        for t in self.tracks:
            s.yardImage.append(t)
        return s

    def show(self):

        for t in self.tracks:
            temp = []
            for tt in t[1]:
                temp.append(tt.name)
            print(t[0]+" | "+str(temp))
        
#==================================================================================
#                                    SCRIPT FUNCTIONS
#==================================================================================

def generateYard1():
    """
    Generates Yard 1
    """
    cl = cList()
    cl.addVertex("1")
    cl.addVertex("2")
    cl.addVertex("3")
    cl.addVertex("4")
    cl.addVertex("5")
    cl.addVertex("6")
    cl.connectLeft("6","5")
    cl.connectLeft("6","2")
    cl.connectLeft("5","4")
    cl.connectLeft("5","3")
    cl.connectLeft("3","1")
    cl.connectLeft("2","1")
    cl.connectRight("1","2")
    cl.connectRight("1","3")
    cl.connectRight("2","6")
    cl.connectRight("3","5")
    cl.connectRight("4","5")
    cl.connectRight("5","6")
    y = yard(cl)
    y.setEngine("1")
    y.addCar("b","4")
    y.addCar("c","4")
    y.addCar("a","4")
    y.addCar("d","6")
    y.addCar("e","2")
    return y

def generateYard2():
    """
    Generates Yard 2
    """
    cl = cList()
    cl.addVertex("1")
    cl.addVertex("2")
    cl.addVertex("3")
    cl.addVertex("4")
    cl.addVertex("5")
    cl.connectLeft("5","1")
    cl.connectLeft("4","2")
    cl.connectLeft("3","2")
    cl.connectLeft("2","1")
    cl.connectRight("1","5")
    cl.connectRight("1","2")
    cl.connectRight("2","3")
    cl.connectRight("2","4")
    y = yard(cl)
    y.setEngine("1")
    y.addCar("a","4")
    y.addCar("b","3")
    y.addCar("c","5")
    y.addCar("d","2")
    y.addCar("e","4")
    return y

def generateYard3():
    """
    Generates Yard 3
    """
    cl = cList()
    cl.addVertex("1")
    cl.addVertex("2")
    cl.addVertex("3")
    cl.connectLeft("2","1")
    cl.connectLeft("3","1")
    cl.connectRight("1","2")
    cl.connectRight("1","3")
    y = yard(cl)
    y.setEngine("1")
    y.addCar("a","2")
    y.addCar("b","3")
    return y

def generateYard4():
    """
    Generates Yard 4
    """
    cl = cList()
    cl.addVertex("1")
    cl.addVertex("2")
    cl.addVertex("3")
    cl.addVertex("4")
    cl.connectLeft("2","1")
    cl.connectLeft("3","1")
    cl.connectLeft("4","1")
    cl.connectRight("1","2")
    cl.connectRight("1","3")
    cl.connectRight("1","4")
    y = yard(cl)
    y.setEngine("1")
    y.addCar("a","2")
    y.addCar("b","3")
    y.addCar("c","3")
    y.addCar("d","4")
    return y

def generateYard5():
    """
    Generates Yard 5
    """
    cl = cList()
    cl.addVertex("1")
    cl.addVertex("2")
    cl.addVertex("3")
    cl.addVertex("4")
    cl.connectLeft("2","1")
    cl.connectLeft("3","1")
    cl.connectLeft("4","1")
    cl.connectRight("1","2")
    cl.connectRight("1","3")
    cl.connectRight("1","4")
    y = yard(cl)
    y.setEngine("1")
    y.addCar("a","2")
    y.addCar("c","3")
    y.addCar("b","3")
    y.addCar("d","4")
    return y

def goalStateP4():
    """
    Generates the goal state for Problem 4 (Yard 2)
    """
    cl = cList()
    cl.addVertex("1")
    cl.addVertex("2")
    cl.addVertex("3")
    cl.addVertex("4")
    cl.addVertex("5")
    cl.connectLeft("5","1")
    cl.connectLeft("4","2")
    cl.connectLeft("3","2")
    cl.connectLeft("2","1")
    cl.connectRight("1","5")
    cl.connectRight("1","2")
    cl.connectRight("2","3")
    cl.connectRight("2","4")
    y = yard(cl)
    y.setEngine("1")
    y.addCar("a","1")
    y.addCar("b","1")
    y.addCar("c","1")
    y.addCar("d","1")
    y.addCar("e","1")
    return y.generateState()

def goalStateY3():
    """
    Generates the goal state for Yard 3 
    """
    cl = cList()
    cl.addVertex("1")
    cl.addVertex("2")
    cl.addVertex("3")
    cl.connectLeft("2","1")
    cl.connectLeft("3","1")
    cl.connectRight("1","2")
    cl.connectRight("1","3")
    y = yard(cl)
    y.setEngine("1")
    y.addCar("a","1")
    y.addCar("b","1")
    return y.generateState()

def goalStateY45():
    """
    Generates the goal state for Yard 4 and 5
    """
    cl = cList()
    cl.addVertex("1")
    cl.addVertex("2")
    cl.addVertex("3")
    cl.addVertex("4")
    cl.connectLeft("2","1")
    cl.connectLeft("3","1")
    cl.connectLeft("4","1")
    cl.connectRight("1","2")
    cl.connectRight("1","3")
    cl.connectRight("1","4")
    y = yard(cl)
    y.setEngine("1")
    y.addCar("a","1")
    y.addCar("b","1")
    y.addCar("c","1")
    y.addCar("d","1")
    return y.generateState()

#==================================================================================
#                                       PROBLEM 1
#==================================================================================

def possibleActions(thisYard, thisState):
    """
    Params:
        thisYard (a yard)
        thisState (a state)

    Returns:
        Returns a list of the possible actions in the form of tuples

        Left from 2 to 1: ("L", "2", "1")
        Right from 3 to 2: ("R", "3", "2")
    """
    typeCheck(thisYard, yard(connectivityList()), 'thisYard is not of type \'yard\'')
    typeCheck(thisState, state(), 'thisState is not of type \'state\'')

    #Find the engine in the state
    currVert = thisYard.getCar("*").position
    
    if(currVert == None):
        print("Engine position has not been established")
        return None
    else:
        Lactions = []
        Ractions = []
        for s in currVert.left:
            if(len(thisYard.getTrack(s.name)[1])>0):
                Ractions.append(("R", s.name, currVert.name))
            Lactions.append(("L", currVert.name, s.name))
        for s in currVert.right:
            if(len(thisYard.getTrack(s.name)[1])>0):
                Lactions.append(("L", s.name, currVert.name))
            Ractions.append(("R", currVert.name, s.name))
        actionsResolve = Lactions + Ractions

        #if(len(actionsResolve)==0):
        #    print("No possible moves")
        #else:
        #    print(str(len(actionsResolve))+" actions:")
        #    for a in actionsResolve:
        #        print(a[0]+" "+a[1]+" "+a[2])
    return actionsResolve

#==================================================================================
#                                    PROBLEM 2
#==================================================================================


def result(thisAction, thisState):

    """
    Params:
        thisAction (a tuple) in the form ("L", "2", "1")
        thisState (a state)

    Returns:
        Returns the resulting state from an action on the state 'thisState'
    """
    
    typeCheck(thisAction, (1,1), "thisAction is not of type \'tuple\'")
    typeCheck(thisState, state(), "thisState is not of type \'state\'")

    if not thisState.validateAction(thisAction):
        print("thisAction: '"+str(thisAction)+"' is invalid")
        return None

    #Find the engine
    currVertName = thisState.enginePosition
    newState = copy.deepcopy(thisState)
    tracky = None
    trackx = None
    for t in newState.yardImage:
        if t[0]==thisAction[1]:
            tracky = t
    for t in newState.yardImage:
        if t[0]==thisAction[2]:
            trackx = t
    
    if(thisAction[0] == "L"):
        if(len(tracky[1])>0):
            moveCar = tracky[1].pop(0)
            moveCar.position = newState.rules.getVertex(trackx[0])
            trackx[1].append(moveCar)
    else:
        if(len(tracky[1])>0):
            moveCar = tracky[1].pop(-1)
            moveCar.position = newState.rules.getVertex(trackx[0])
            trackx[1].insert(0, moveCar)
    return newState
    
#==================================================================================
#                                    PROBLEM 3
#================================================================================== 

def expand(thisState, thisYard):
    """
    Params:
        thisState (a state)
        thisYard (a yard)

    Return:
        a list of all the possible resulting states from 'thisState'
    """
    typeCheck(thisYard, yard(connectivityList()), "thisYard is not of type \'yard\'")
    typeCheck(thisState, state(), "thisState is not of type \'state\'")

    routes = possibleActions(thisYard, thisState)
    possibilities = []
    for r in routes:
        possibilities.append(result(r, thisState))
            
    return possibilities

def smartExpand(thisState, thisYard):
    """
    Params:
        thisState (a state)
        thisYard (a yard)

    Return:
        a list of tuples of all the possible resulting states from 'thisState' and
            the move that created them

        Example: ( ("L","2","1") , newState )
    """
    typeCheck(thisYard, yard(connectivityList()), "thisYard is not of type \'yard\'")
    typeCheck(thisState, state(), "thisState is not of type \'state\'")

    routes = possibleActions(thisYard, thisState)
    smartPossibilities = []
    for r in routes:
        smartPossibilities.append((r, result(r, thisState)))
    return smartPossibilities

#==================================================================================
#                                    PROBLEM 4
#==================================================================================    
        
def bfsSolve(thisYard, initState, goalState, iters):
    """
    Params:
        thisYard (a yard)
        initState (a state)
        goalState (a state)
        iters (an int) the iteration cap for the breadth first search

    Usage:
        if iters = -1 then the algorithm will run until it finds a solution with
            no cap on the amount of iterations

        if iteration >= 0 then the algorithm will try to find the first solution
            with an amount of moves under the iteration cap
    Returns:
        a list of moves that will reach the goal state if it is found
        if the goal state is not found within the amount of iterations, None
            will be returned
    """
    typeCheck(thisYard, yard(connectivityList()), "thisYard is not of type \'yard\'")
    typeCheck(initState, state(), "initState is not of type \'state\'")
    typeCheck(goalState, state(), "goalState is not of type \'state\'")
    typeCheck(iters, int(1), "iters is not of type \'int\'")

    if iters < -1 :
        raise Exception("'iters' can not be less than -1'")

    class nodeQueue:
        def __init__(self):
            self.data = []
            self.history = []

        def push(self, element):
            self.data.append(element)

        def pop(self):
            d = self.data.pop(0)
            self.history.append(d[1])
            return d

        def exists(self, thisNode):
            for d in self.data:
                if d[1].equals(thisNode[1]):
                    return True
            return False

        def visited(self, aNode):
            for s in self.history:
                if s.equals(aNode[1]):
                    return True
            return False

        def getLength(self):
            return len(self.data)

        def isEmpty(self):
            return len(self.data)==0

    nQ = nodeQueue()
    
    #Implementing Breadth First Search
    def continueQuery(iters):
        decision = input("Would you like to continue? Iteration: " + str(iters))
        if(decision == "n"):
            return False
        else:
            return True

    nQ.push(([],initState))
    if(iters == -1):
        #infinite mode
        while not nQ.isEmpty():
            node = nQ.pop()
            batch = smartExpand(node[1], node[1].generateYard())
            for candidate in batch:
                newNode = (node[0] + [candidate[0]], candidate[1])
                if (not nQ.visited(newNode)) and (not nQ.exists(newNode)):
                    if newNode[1].equals(goalState):
                        return newNode[0]
                    nQ.push(newNode)
        return None
            
    else:
        while not nQ.isEmpty():
            node = nQ.pop()
            batch = smartExpand(node[1], node[1].generateYard())
            for candidate in batch:
                newNode = (node[0] + [candidate[0]], candidate[1])
                if (not nQ.visited(newNode)) and (not nQ.exists(newNode)):
                    if newNode[1].equals(goalState):
                        return newNode[0]
                    nQ.push(newNode)
    return None

def bfsDebug(thisYard, initState, goalState, iters):
    """
    Params:
        thisYard (a yard)
        initState (a state)
        goalState (a state)
        iters (an int) the iteration cap for the breadth first search

    Usage:
        if iters = -1 then the algorithm will run until it finds a solution with
            no cap on the amount of iterations

        if iteration >= 0 then the algorithm will try to find the first solution
            with an amount of moves under the iteration cap

        This function is the same as bfsSolve, however, this function allows
            the user to step through the process of finding a solution
    Returns:
        a list of moves that will reach the goal state if it is found
        if the goal state is not found within the amount of iterations, None
            will be returned
    """
    typeCheck(thisYard, yard(connectivityList()), "thisYard is not of type \'yard\'")
    typeCheck(initState, state(), "initState is not of type \'state\'")
    typeCheck(goalState, state(), "goalState is not of type \'state\'")
    typeCheck(iters, int(1), "iters is not of type \'int\'")

    if iters < -1 :
        raise Exception("'iters' can not be less than -1'")

    class nodeQueue:
        def __init__(self):
            self.data = []
            self.history = []

        def push(self, element):
            self.data.append(element)

        def pop(self):
            d = self.data.pop(0)
            self.history.append(d[1])
            return d

        def exists(self, thisNode):
            for d in self.data:
                if d[1].equals(thisNode[1]):
                    return True
            return False

        def visited(self, aNode):
            for s in self.history:
                if s.equals(aNode[1]):
                    return True
            return False

        def getLength(self):
            return len(self.data)

        def isEmpty(self):
            return len(self.data)==0

    nQ = nodeQueue()
    
    #Implementing Breadth First Search
    def continueQuery(iters):
        decision = input("Would you like to continue? Iteration: " + str(iters))
        if(decision == "n"):
            return False
        else:
            return True

    nQ.push(([],initState))
    iteration = 0
    if(iters == -1):
        #infinite mode
        while not nQ.isEmpty():
            node = nQ.pop()
            if iteration < len(node[0]):
                iteration += 1
                if not continueQuery(iteration):
                    print("Iteration: " + str(iteration))
                    print("Paths: " + len(nodeList))
                    break
                
            batch = smartExpand(node[1], node[1].generateYard())
            for candidate in batch:
                newNode = (node[0] + [candidate[0]], candidate[1])
                if (not nQ.visited(newNode)) and (not nQ.exists(newNode)):
                    if newNode[1].equals(goalState):
                        return newNode[0]
                    nQ.push(newNode)
        return None
            
    else:
        print("Iteration: " + str(iteration))
        while not nQ.isEmpty():
            node = nQ.pop()
            if iteration < len(node[0]):
                if(iteration >= iters):
                    return None
                iteration += 1
                if not continueQuery(iteration):
                    print("Iteration: " + str(iteration))
                    print("Paths: " + len(nodeList))
                    break
                
            batch = smartExpand(node[1], node[1].generateYard())
            for candidate in batch:
                newNode = (node[0] + [candidate[0]], candidate[1])
                if (not nQ.visited(newNode)) and (not nQ.exists(newNode)):
                    if newNode[1].equals(goalState):
                        return newNode[0]
                    nQ.push(newNode)
    return None

#==================================================================================
#                                    PROBLEM 5
#==================================================================================

"""
Q. How big is the search space for c cars on t tracks [i.e. how many possible
    states]??

A. (T^c)*c!    
"""

#==================================================================================
#                                    PROBLEM 6
#================================================================================== 

def aStarSolve(thisYard, initState, goalState, iters):

    """
    Params:
        thisYard (a yard)
        initState (a state)
        goalState (a state)
        iters (an int) the iteration cap for the breadth first search

    Usage:
        if iters = -1 then the algorithm will run until it finds a solution with
            no cap on the amount of iterations

        if iteration >= 0 then the algorithm will try to find the first solution
            with an amount of moves under the iteration cap

        This A* algorithm incorporates a priority queue that pops the node with
            the least f = g + h value. The heuristic for this algorithm is
            calculated by getting the amount of cars on the wrong track
            
    Returns:
        a list of moves that will reach the goal state if it is found
        if the goal state is not found within the amount of iterations, None
            will be returned
    """
    
    typeCheck(thisYard, yard(connectivityList()), "thisYard is not of type \'yard\'")
    typeCheck(initState, state(), "initState is not of type \'state\'")
    typeCheck(goalState, state(), "goalState is not of type \'state\'")
    typeCheck(iters, int(1), "iters is not of type \'int\'")

    if iters < -1 :
        raise Exception("'iters' can not be less than -1'")

    class nodePriorityQueue:
        def __init__(self):
            self.data = []
            self.history = []
            
        def push(self, element):
            #Assign priority to object
            self.data.append((element, self.getPriority(element)))

        def pop(self):
            val = -1
            ind = -1
            for i in range(len(self.data)):
                if self.data[i][1] < val or ind == -1:
                    val = self.data[i][1]
                    ind = i
            d = self.data.pop(ind)
            self.history.append(d[0][1])
            return d[0]

        def exists(self, thisNode):
            for d in self.data:
                if d[0][1].equals(thisNode[1]):
                    return True
            return False

        def visited(self, aNode):
            for s in self.history:
                if s.equals(aNode[1]):
                    return True
            return False

        def getLength(self):
            return len(self.data)

        def isEmpty(self):
            return len(self.data)==0

        def getPriority(self, aNode):
            """
                This will return the f value for the equation:
                f = g + h
                for a given node
            """

            gMultiplier = 1
            gUnit = 1
            
            hMultiplier = 1
            hUnit = 1
            
            #How many moves are taken
            g = gMultiplier * gUnit * len(aNode[0])

            sTracks = aNode[1].yardImage
            gTracks = goalState.yardImage

            sCars = []
            gCars = []
            for sT in sTracks:
                sCars += sT[1]

            for gT in gTracks:
                gCars += gT[1]

            h = 0
            for sC in sCars:
                found = False
                for gC in gCars:
                    if sC.name == gC.name:
                        #Check if right position
                        if sC.position.name == gC.position.name:
                            gCars.remove(gC)
                            found = True
                            break
                if not found:
                    h += hUnit * hMultiplier
                
            f = g + h 
            return f
    
    nQ = nodePriorityQueue()
    
    #Implementing Breadth First Search
    nQ.push(([],initState))
    if(iters == -1):
        #infinite mode
        while not nQ.isEmpty():
            node = nQ.pop()
            batch = smartExpand(node[1], node[1].generateYard())
            for candidate in batch:
                newNode = (node[0] + [candidate[0]], candidate[1])
                if (not nQ.visited(newNode)) and (not nQ.exists(newNode)):
                    if newNode[1].equals(goalState):
                        return newNode[0]
                    nQ.push(newNode)
        return None
            
    else:
        while not nQ.isEmpty():
            node = nQ.pop()
            batch = smartExpand(node[1], node[1].generateYard())
            for candidate in batch:
                newNode = (node[0] + [candidate[0]], candidate[1])
                if (not nQ.visited(newNode)) and (not nQ.exists(newNode)):
                    if newNode[1].equals(goalState):
                        return newNode[0]
                    nQ.push(newNode)
    return None

#==================================================================================
#                                    Scripts
#==================================================================================

#Set Up
y2 = generateYard2()
y3 = generateYard3()
y4 = generateYard4()
y5 = generateYard5()

#Problem 1
#print(possibleActions(y2, y2.generateState))

#Problem 2
#es = result(possibleActions(y2, y2.generateState)[0], y2.generateState)
#es.show()

#Problem 3
#expand(y2.generateState(), y2)

#Problem 4
#print(bfsSolve(y3, y3.generateState(), goalStateY3(), -1))
#print(bfsSolve(y4, y4.generateState(), goalStateY45(), -1))
#print(bfsSolve(y5, y5.generateState(), goalStateY45(), -1))
print(bfsSolve(y2, y2.generateState(), goalStateP4(), -1))

#Problem 6
#print(aStarSolve(y3, y3.generateState(), goalStateY3(), -1))
#print(aStarSolve(y4, y4.generateState(), goalStateY45(), -1))
#print(aStarSolve(y5, y5.generateState(), goalStateY45(), -1))
print(aStarSolve(y2, y2.generateState(), goalStateP4(), -1))

