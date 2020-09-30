#Project 3 - CISC481
#University of Delaware
#Author: Nonso Iwu
import copy
from proj3 import *


#==========================================================
#                   SINGLE LAYER NETWORK
#==========================================================
print("==========================================================")
print("                   SINGLE LAYER NETWORK")
print("==========================================================")

#Simple 1 layer network
g = Graph()
v1 = Vertex.new("1", "i")
v2 = Vertex.new("2", "i")
v3 = Vertex.new("3", "o")
v4 = Vertex.new("4", "o")
g.connect(v1, 1, v3).connect(v1, 1, v4)
g.connect(v2, 1, v3).connect(v2, 1, v4)

gs = copy.deepcopy(g)

print("===================BEFORE===================")
g.lshow()
for i in range(5):
    classify(g, [0,0])
    backProp(g, [0,0])
    
    classify(g, [0,1])
    backProp(g, [0,1])

    classify(g, [1,0])
    backProp(g, [0,1])

    classify(g, [1,1])
    backProp(g, [1,0])

print("===================AFTER: THRESHOLD===================")
g.lshow()

print("\nInputs: 0, 0")
classify(g, [0,0])
g.showOutput()
print("Inputs: 0, 1")
classify(g, [0,1])
g.showOutput()
print("Inputs: 1, 0")
classify(g, [1,0])
g.showOutput()
print("Inputs: 1, 1")
classify(g, [1,1])
g.showOutput()

#==========================================================
#                   MULTILAYER NETWORK
#==========================================================
print("==========================================================")
print("                   MULTILAYER NETWORK")
print("==========================================================")

g2 = Graph()
v1 = Vertex.new("1", "i")
v2 = Vertex.new("2", "i")
v3 = Vertex.new("3", "h")
v4 = Vertex.new("4", "h")
v5 = Vertex.new("5", "o")
v6 = Vertex.new("6", "o")
g2.connect(v1, 1, v3).connect(v1, 1, v4)
g2.connect(v2, 1, v3).connect(v2, 1, v4)
g2.connect(v3, 1, v5).connect(v3, 1, v6)
g2.connect(v4, 1, v5).connect(v4, 1, v6)

g2s = copy.deepcopy(g2)

print("===================BEFORE===================")
g2.lshow()

for i in range(100):
    classify(g2, [0,0])
    backProp(g2, [0,0])
    
    classify(g2, [0,1])
    backProp(g2, [0,1])

    classify(g2, [1,0])
    backProp(g2, [0,1])

    classify(g2, [1,1])
    backProp(g2, [1,0])

for i in range(1000):
    classify(g2s, [0,0], True)
    backProp(g2s, [0,0], True)
    #g.show()
    classify(g2s, [0,1], True)
    backProp(g2s, [0,1], True)
    #g.show()
    classify(g2s, [1,0], True)
    backProp(g2s, [0,1], True)
    #g.show()
    classify(g2s, [1,1], True)
    backProp(g2s, [1,0], True)

print("===================AFTER: THRESHOLD===================")
g2.lshow()

print("\nInputs: 0, 0")
classify(g2, [0,0])
g2.showOutput()
print("Inputs: 0, 1")
classify(g2, [0,1])
g2.showOutput()
print("Inputs: 1, 0")
classify(g2, [1,0])
g2.showOutput()
print("Inputs: 1, 1")
classify(g2, [1,1])
g2.showOutput()

print("===================AFTER: LOGIT===================")
g2s.lshow()

print("\nInputs: 0, 0")
classify(g2s, [0,0], True)
g2s.showOutput(True)
print("Inputs: 0, 1")
classify(g2s, [0,1], True)
g2s.showOutput(True)
print("Inputs: 1, 0")
classify(g2s, [1,0], True)
g2s.showOutput(True)
print("Inputs: 1, 1")
classify(g2s, [1,1], True)
g2s.showOutput(True)
