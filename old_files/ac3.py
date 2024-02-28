import sys;
import copy;

#lists of states
variables = [ "WA",  "NT", "SA", "Q", "NSW", "V", "T",]

# adjacent states of element at matching index of variables in list
constraints = [ ["NT", "SA"], [ "WA", "SA", "Q"], ["WA", "NT", "Q", "NSW", "V"], ["SA", "NT", "NSW"], ["SA", "Q", "V"], ["NSW", "SA"], []]

#domains
d = [ ["red", "green", "blue"], ["red", "green", "blue"], ["red", "green", "blue"], ["red", "green", "blue"], ["red", "green", "blue"], ["red", "green", "blue"], ["red", "green", "blue"]]

assignments = { }
arcs = []

def AC3():

    #fill queue with initial arcs
    fillQueue()

    # check if arcs is empty
    while arcs:
        arcVars = arcs.pop(0)
        if (revise(arcVars[0], arcVars[1])):

            dIIndex = variables.index(arcVars[0])
            if len(d[dIIndex]) == 0:
                print ("No solution")
                return False
            neighbors = list(constraints[dIIndex])
            neighbors.remove(arcVars[1])

            for xk in neighbors:
                arcs.append([xk, arcVars[0]])

        print(assignments)
        return True;

def fillQueue():

    for var in variables:
        varIndex = variables.index(var)
        for arc in constraints[varIndex]:
            arcs.append([var, arc])

def revise(Xi, Xj):
    revised = False

    Iindex = variables.index(Xi)

    # for each value in the domain:
    for x in d[Iindex]:
        if Xj not in constraints[Iindex]:
            break

        if Xj not in assignments:
            break

        if x in assignments[Xj]:
            d[Iindex].remove(x) # remove x from Di
            revised = True

    if not revised and len(d[Iindex]) > 0:
        assignments[Xi] = d[Iindex][0]

    return revised

AC3()