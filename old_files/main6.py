import sys
import copy
import numpy as np
from queue import Queue, PriorityQueue

class GraphState:
    def __init__(self, nodeIndex, constraints, domains, coloring, parent):
        self.nodeIndex = nodeIndex

        self.constraints = constraints
        self.domains = domains
        self.coloring = coloring
        self.parent = parent

        if nodeIndex >= len(vertices):
            self.node = None
        else:
            self.node = vertices[nodeIndex]

    def is_goal(self):
        return len(self.coloring) == len(vertices)

    def order_domain_values(self, clone_domains):
        # Order domain values using heuristic
        # see the heuristic detail in is_consistent(vIndex, color) function below
        domain = clone_domains[self.node]
        domain.sort(key=lambda color: self.is_consistent(color), reverse=True)
        return domain

    def is_consistent(self, color):
        # TODO: a count so is_consistent() returns a number
        # the color that is inconsistent with the most neighbors should be explored first - fail fast
        #   this is the one color that is involved in more constraints
        # the color that is inconsistent with the least neighbors should be explored last
        inconsistent_count = 0

        for neighbor in self.constraints[self.node]:
            if neighbor in self.coloring and self.coloring[neighbor] == color:
                # color is inconsistent with at least 1 neighbor
                inconsistent_count += 1

        return inconsistent_count

    def update_neighbor_constraints(self, color, clone_domains):

        for neighbor in self.constraints[self.node]:
            if color in clone_domains[neighbor]:
                clone_domains[neighbor].remove(color)

        return clone_domains


    def successors(self):

        successors = []
        clone_domains = copy.deepcopy(self.domains)
        current_domain_heuristic = self.order_domain_values(clone_domains)

        for color in current_domain_heuristic:

            if self.is_consistent(color) == 0:
                # if coloring the vertex with this color does not violate any constraints for the neighbors
                new_coloring = self.coloring.copy()
                new_coloring[self.node] = color
                # TODO: Constraint propagation: Remove the colored color from the neighbors constraints
                clone_domains = self.update_neighbor_constraints(color, copy.deepcopy(self.domains))

                successors.append(GraphState(self.nodeIndex + 1, self.constraints, clone_domains, new_coloring, self))

        return successors

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
    # vertices = sorted(list(vertices))
    vertices = sorted(list(vertices))
    return


def initConstraints():
    global constraints
    constraints = {}

    for v in vertices:
        subConstraints = []
        for r in data:
            if r[0] == v:
               subConstraints.append(r[1])
            elif r[1] == v:
                subConstraints.append(r[0])
        constraints[v] = subConstraints
    return

def initDomains():

    global domains
    colorList = ["red", "green", "blue", "indigo", "orange", "yellow", "violet", "gray", "maroon", "black", "olive", "cyan", "pink", "magenta", "tan", "teal"]
    domains = {}
    if numColors < len(colorList):
        for v in vertices:
            domains[v] = colorList[:numColors]
    else:
        print("Not enough color")
    return

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


def order_unassigned_vertices(startIndex):
    # order the remaining unassigned vertices using heuristic
    unassigned = [node for node in vertices[startIndex: len(vertices)] if node not in coloring]
    unassigned.sort(key = lambda node: heuristic(node))
    return unassigned


def is_complete():
    return len(coloring) == len(vertices)

def print_path(path):
    for p in path:
        print(f"-> node: {p.node}\ncoloring: {p.coloring}\n domains: {p.domains}")

def a_star_search(initial_state):

    frontier = Queue()
    frontier.put(initial_state)
    # came_from = {initial_state: None}

    while not frontier.empty():
        current_state = frontier.get()

        if current_state.is_goal():
            # Reconstruct path
            print(f"Found goal! Coloring: {current_state.coloring}")

            return True
            # return len(path) - 1  # Number of steps excluding the initial state

        if current_state.nodeIndex < len(vertices):
            # print_path(current_state.successors())

            for next_state in current_state.successors():
                frontier.put(next_state)

    print("No path!")


    return False

def graph_coloring():
    global coloring
    coloring = {}

    initialState = GraphState(0, constraints, domains, coloring, None)
    steps = a_star_search(initialState)

    print(steps)
    # if graph_coloring_util(0, domains) == False:
    #     print("No solution exists")


if __name__ == '__main__':
    # Read Graph and Color
    readInput("input3.txt")
    print(f"colors: {numColors}")
    print(f"graph: \n {data}")

    # Create Variables
    initVertices()
    print(f"vertices: \n {vertices}")

    # Create constraints
    initConstraints()
    print(f"constraints: \n {constraints}")

    # Create the domain
    initDomains()
    print(f"domains: \n {domains}")


    # AC3()
    graph_coloring()

    # need to add a select_unassigned_vertices_heuristic and order_domain_value() method as in main3.py