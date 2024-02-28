import sys
import copy
import numpy as np
from queue import Queue, PriorityQueue

def readInput(fname):
    global data
    global numColors

    # read the graph
    data = np.loadtxt("inputs/" + fname, delimiter=",", comments="#", skiprows=4, dtype="int")

    # read the color
    myFile = open("inputs/" + fname, 'r')
    substr = "colors = "
    for line in myFile:
        if line.lower().startswith(substr):
            numColors = int(line[len(substr):])
            return
    return


def initVertices():
    global vertices
    vertices = set()
    for r in data:
        for c in r:
            vertices.add(c)
    vertices = sorted(list(vertices))
    return


def initConstraints():
    global constraints
    constraints = []

    for v in vertices:
        subConstraints = []
        for r in data:
            if r[0] == v:
               subConstraints.append(r[1])
            elif r[1] == v:
                subConstraints.append(r[0])
        constraints.append(subConstraints)
    return


def initDomains():
    global domains
    colorList = ["red", "green", "blue", "indigo", "orange", "yellow", "violet", "gray", "maroon", "black", "olive", "cyan", "pink", "magenta", "tan", "teal"]
    if numColors < len(colorList):
        domains = [colorList[:numColors] for v in vertices]
    else:
        print("Not enough color")
    return


def AC3():
    global coloring
    coloring = {}

    # populate the arcsQ with initial arcs
    fillQueue()

    # check if the arcsQ is empty
    while not arcsQ.empty() :
        # queueItem = arcsQ.get()
        # arc = queueItem[1]
        # print(f"queueItem {queueItem}")
        arc = arcsQ.get()

        if revise(arc[0], arc[1]):
            vIndex = vertices.index(arc[0])
            if len(domains[vIndex]) == 0:
                backtrack()
                return False

            neighbors = list(constraints[vIndex])
            neighbors.remove(arc[1])

            for neighbor in neighbors:
                #arcsQ.put((heuristic(neighbor), [neighbor, arc[0]]))
                arcsQ.put([neighbor, arc[0]])

        # if arcsQ.empty():


    print(coloring)
    return True

def is_complete():
    return len(coloring) == len(vertices)

def fillQueue():
    global arcsQ

    # arcsQ = PriorityQueue(maxsize=0)
    arcsQ = Queue(maxsize=0)
    for v in vertices:
        index = vertices.index(v)
        for adj in constraints[index]:
            # arcsQ.put((heuristic(v), [v, adj]))
            arcsQ.put([v, adj])


def revise(v, adj):
    # dictionary of current coloring choices
    revised = False
    vIndex = vertices.index(v)

    # for each color in the domains of the current vertex
    for color in domains[vIndex]:
        # check if adjacent vertex does not have any color assignment yet:
        if adj not in coloring.keys():
            continue

        # if the current color is same as one of the adjacent vertex color assignments (constraint violation)
        if color in coloring[adj]:
            domains[vIndex].remove(color) # remove the violating color
            revised = True

    if not revised and len(domains[vIndex]) > 0:
        coloring[v] = domains[vIndex][0]

    return revised

# test Minimum Remaining Value on the vertex on the left
# the vertex with the fewest legal values remain gets top priority
def MRV(v):
    vIndex = vertices.index(v)
    return len(domains[vIndex])

# test Most Constrained Vertex on the vertex on the left
# choose the vertex that is involved in more constraints
# because this vertex needs to be freed earlier
def MCV(v):
    vIndex = vertices.index(v)
    return len(constraints[vIndex])

def heuristic(v):
    # vertex that has the fewest remaining value
    # and that is involved in more constraints will have higher priority
    # Items are retrieved priority order (lowest first)
    return MRV(v) - MCV(v)

def backtrack_search():
    return backtrack()

def backtrack():
    # base case: if coloring is complete
    if len(coloring) == len(vertices):
        return coloring
    node = select_unassigned_vertices()

    for color in order_domain_values(node):
        if is_consistent(node, color):
            coloring[node] = color
            result = backtrack()
            if result is not None:
                return result
            del coloring[node]

    return None


def select_unassigned_vertices():
    unassigned = [node for node in vertices if node not in coloring]
    return min(unassigned, key = lambda x: heuristic(x))

def order_domain_values(v):
    vIndex = vertices.index(v)
    domain = domains[vIndex]
    domain.sort(key = lambda x: sum(is_consistent(v, x)))

def is_consistent(v, color):
    vIndex = vertices.index(v)
    for neighbor in constraints[vIndex]:
        if neighbor in coloring and coloring[neighbor] == color:
            return False
    return True

if __name__ == '__main__':
    # Read Graph and Color
    readInput("input1.txt")
    print(f"colors: {numColors}")
    print(f"data: \n {data}")

    # Create Variables
    initVertices()
    print(f"variables: \n {vertices}")

    # Create constraints
    initConstraints()
    print(f"constraints: \n {constraints}")

    # Create the domain
    initDomains()
    print(f"domains: \n {domains}")

    AC3()