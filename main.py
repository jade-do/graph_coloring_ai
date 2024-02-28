import copy
import numpy as np
from queue import Queue, PriorityQueue

def readInput(fname):
    global data
    global numColors

    # read the graph
    data = np.loadtxt(fname, delimiter=",", comments="#", skiprows=4, dtype="int")

    # read the color
    myFile = open(fname, 'r')
    substr = "colors = "
    for line in myFile:
        if line.lower().startswith(substr):
            numColors = int(line[len(substr):])
            myFile.close()
            return

    myFile.close()
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


def minimum_remaining_color(vertex, clone_domains):
    # MRV: the vertex with the fewest legal color values remain will have higher priority
    return len(clone_domains[vertex])

def most_constrained_vertex(vertex):
    # Tie-breaking: the vertex that is involved in more constraints will have higher priority
    return len(constraints[vertex])

def heuristic_vertices_order(vertices_order, clone_domains):
    # Items are retrieved priority order (lower number = higher priority)
    vertices_order.sort(key=lambda v: minimum_remaining_color(v, clone_domains) - most_constrained_vertex(v))
    return vertices_order


def prune_neighbor_domains(vertex, color, clone_domains):
    for neighbor in constraints[vertex]:
        if color in clone_domains[neighbor]:
            clone_domains[neighbor].remove(color)

    return clone_domains


def is_consistent(vertex, color):
    for neighbor in constraints[vertex]:
        if neighbor in coloring and coloring[neighbor] == color:
            return False
    return True


def is_complete():
    return len(coloring) == len(vertices)


def graph_coloring_util(current_vertices, current_vIndex, current_domains):
    # Base case: All vertices colored, print the solution
    if is_complete():
        print(f"Coloring: {coloring}")
        return True

    current_vertex = current_vertices[current_vIndex]

    for color in current_domains[current_vertex]:
        clone_domains = copy.deepcopy(current_domains)

        if is_consistent(current_vertex, color):
            # if coloring the vertex with this color does not
            # violate any constraints for the neighbors
            coloring[current_vertex] = color

            # Heuristic: Order vertices and decide which one to color first
            colored_vertices = copy.deepcopy(current_vertices)[0: current_vIndex + 1]
            uncolored_vertices = copy.deepcopy(current_vertices)[current_vIndex + 1: len(current_vertices)]
            heuristic_vertices= colored_vertices + heuristic_vertices_order(uncolored_vertices, clone_domains)

            # Constraint propagation: Remove the colored color from the neighbors constraints
            pruned_domains = prune_neighbor_domains(current_vertex, color, clone_domains)

            # Recursively color the remaining vertices
            if graph_coloring_util(heuristic_vertices, current_vIndex+1, pruned_domains):
                return True

            # Backtrack if assigning color c does not lead to a solution
            del coloring[current_vertex]

    return False


def graph_coloring():
    global coloring
    coloring = {}

    heuristic_vertices = heuristic_vertices_order(copy.deepcopy(vertices), domains)

    if graph_coloring_util(heuristic_vertices, 0, domains) == False:
        print("No solution exists")
        return False

    return True

def test_coloring():
    for node, neighbors in constraints.items():
        color = coloring[node]
        # print(color)
        for neighbor in neighbors:
            # print(coloring[neighbor])
            if coloring[neighbor] == color:
                print(f"Failed to color graph!")
                return False
    return True


def start_coloring(fname):

    # Read Graph and Color
    readInput("inputs/" + fname)
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

    result1 = graph_coloring()

    if not result1:
        # No solution
        print(f"Sorry no color found!")
        return "no solution"

    else:
        result2 = test_coloring()
        if result2:
            print(f"Congratulations! Your graph is now colored!")
            return "correct solution"

    return "incorrect solution"

if __name__ == '__main__':

    start_coloring("input5.txt")
