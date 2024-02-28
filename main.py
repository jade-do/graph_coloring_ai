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
def MRV(vertices_order, clone_domains):
    vertices_order.sort(key = lambda v: len(clone_domains[v]))
    return vertices_order

# test Most Constrained Vertex on the vertex on the left
# choose the vertex that is involved in more constraints
# because this vertex needs to be freed earlier
def MCV(v):
    vIndex = vertices.index(v)
    return len(constraints[vIndex])

def heuristic_vertices_order(vertices_order, clone_domains):
    # MRV: the vertex with the fewest legal color values remain gets top priority
    # Tie-breaking rule: the vertex that is involved in more constraints will have higher priority
    # Items are retrieved priority order (lowest first)
    vertices_order.sort(key=lambda v: len(clone_domains[v]) - len(constraints[v]))
    return vertices_order
    # return MRV(v) - MCV(v)

def prune_neighbor_domains(vertex, color, clone_domains):
    for neighbor in constraints[vertex]:
        if color in clone_domains[neighbor]:
            clone_domains[neighbor].remove(color)

    return clone_domains


def order_domain_values(vertex, clone_domains):
    # Order colors using heuristic
    # The color with the most inconsistent neighbors - more constrained - will be explored first - fail fast
    # see the heuristic detail in is_consistent(vIndex, color) function below
    domain = clone_domains[vertex]
    domain.sort(key = lambda color: is_consistent(vertex, color), reverse = False)
    return domain


def is_consistent(vertex, color):
    # TODO: a count so is_consistent() returns a number
    # the color that is inconsistent with the most neighbors should be explored first - fail fast
    #   this is the one color that is involved in more constraints
    # the color that is inconsistent with the least neighbors should be explored last
    inconsistent_count = 0

    for neighbor in constraints[vertex]:
        if neighbor in coloring and coloring[neighbor] == color:
            # color is inconsistent with at least 1 neighbor
            inconsistent_count += 1

    return inconsistent_count

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
        colored_vertices = copy.deepcopy(current_vertices)[0: current_vIndex+1]
        uncolored_vertices = copy.deepcopy(current_vertices)[current_vIndex+1: len(current_vertices)]

        if is_consistent(current_vertex, color) == 0:
            # if coloring the vertex with this color does not
            # violate any constraints for the neighbors
            coloring[current_vertex] = color

            # Constraint propagation: Remove the colored color from the neighbors constraints
            heuristic_vertices= colored_vertices + heuristic_vertices_order(uncolored_vertices, clone_domains)
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


    if graph_coloring_util(vertices, 0, domains) == False:
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


    # need to add a select_unassigned_vertices_heuristic and order_domain_value() method as in main3.py