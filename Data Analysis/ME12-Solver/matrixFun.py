# Test for Matrix solving for ME 12
# By: Daniel Neamati and Paulina Ridland



'''   Version two
1) Allow z component
2) Prompt for Magnitude
3) Manage Magniture (determine what it needs to solve for)
4) Read from csv
    - Column head would be the name
    - each row under head is the mag, x, y, z
5) Allow fractions, powers, etc.
6) Solve for angle instead of magnitude
    - Requires figuring out the unknowns
7) Determine Momemts, etc.
8) Make Unit Vectors
'''


import numpy as np
import sympy
import pandas as pd




def solveSys(matrixA, names):
    '''Solves a system of equations and matches the name of 
    the results.
    Input:  matrixA is an n x m matrix
            names is a list of the name of forces
    Output: [(name 1, force value 1), ...]'''
    matrixA = np.matrix(matrixA)
    
    matrixA = matrixA.transpose()
    row, col = matrixA.shape

    rrefA = sympy.Matrix(matrixA).rref()
    rrefA = rrefA[0]
    print(rrefA)
    print(rrefA[1,1])
    print(row, col)
    print(len(names))
    print(rrefA[:,col - 1])

    result = []
    for i in range(row):
        result.append((names[i], rrefA[i, col - 1]))

    return result

def inputForces():
    numForces = int(input("How many forces? "))
    names = []
    matrixA = []
    for force in range(numForces):
        names.append(input("What is the name of the {} force?   ".format(force + 1)))
    for force in names:
        curr_force_dir = []
        for dim in ['x','y','z']:
                lamdaDim = float(input("What is the {} component of force {}? ".format(dim, force)))
                curr_force_dir.append(lamdaDim)
        curr_force_dir = makeUnitVector(curr_force_dir)
        print(curr_force_dir)
        magnitude = float(input(\
                "What is the magnitude of force {}? ".format(force)))
        curr_force_dir = magnitude * curr_force_dir
        matrixA.append(curr_force_dir)

    return matrixA, names

def printResult(result):
    print("############################")
    print("###        Result        ###")
    print("############################")
    for out in result:
        print(out[0], " = ", -out[1])
def makeUnitVector(vector):
        '''
        Takes a vector and makes it a unit vector.
        '''
        vector = np.array(vector)
        vector_normalized = vector / np.linalg.norm(vector)
        return vector_normalized


if __name__ == '__main__':
    matrixA, names = inputForces()
    result = solveSys(matrixA, names)
    print("Result: ", result)
    printResult(result)
