from maze import *
import random
import sys

def addDirectionOption(Maze, row, column, direction, dir_list):
    ''' Adds a direction to the list of possible directions'''
    (neighbor_row, neighbor_col) = Maze.getNeighborCell(row, column, direction)

    if not Maze.isVisited(neighbor_row, neighbor_col):
        dir_list.append(direction)

def numWalls(Maze, cellRow, cellCol):
    ''' Check has number of walls'''
    wall_num = 0

    if Maze.hasWall(cellRow, cellCol, "North"):
        wall_num += 1
    if Maze.hasWall(cellRow, cellCol, "East"):
        wall_num += 1
    if Maze.hasWall(cellRow, cellCol, "South"):
        wall_num += 1
    if Maze.hasWall(cellRow, cellCol, "West"):
        wall_num += 1

    return wall_num

def findFurthestSharedCell(Maze):
    '''We want to find the furthest cell from the exit that appears more than
    once. '''
    # We first want to sort the list to put the higher numbers (cells further
    # from the exit) at the front of the list
    cellNumList = sorted(Maze.cellNumToExit)[::-1]

    for cell in cellNumList:
        # If the cell is repeated, then we found our candidate
        if cellNumList.count(cell) >= 2:
            return cell 
    # If there is no candidate, then there is only one path in the entire
    # maze. Notify the calling function.
    return -1

def findAllIndices(inList, val):
    '''Return a list of all the indices which contain the given value 'val' '''
    indexList = []

    for index, item in enumerate(inList):
        if item == val:
            indexList.append(index)

    return indexList
        


def usage(name):
    ''' Show usage imformation for our program'''
    print("usage:", name, "n f")
    print("n is an integer of total maze rows")
    print("f is an integer of total maze columns")

def genMaze():
    ''' This function generates the maze'''
    if len(sys.argv) < 3:
        print("Too Few Arguments!")
        usage(sys.argv[0])

    elif len(sys.argv) > 3:
        print("Too Many Arguments!")
        usage()

    else:
        m = Maze(int(sys.argv[1]), int(sys.argv[2]))
        m.clear()
        m.setAllWalls()
        # m.setVisited(m.start[0], m.start[1])
        m.setVisited(m.end[0], m.end[1])

        path = []

        path.append(m.end)

        while not len(path) == 0:
            # Add current location to the path
            (current_r, current_c) = path[len(path) - 1]

                
            # This list will contain the direction options to expand the 
            # maze from the current Location.
            # IMPORTANT: We want options to reset after every loop
            options = []
            
            # Check that there is room to the NORTH
            if current_r > 0:
                addDirectionOption(m, current_r, current_c, "North", options)

            # Also check that there is room to the SOUTH
            if current_r < m.numRows - 1:
                addDirectionOption(m, current_r, current_c, "South", options)

            # Also check that there is room to the WEST
            if current_c > 0:
                addDirectionOption(m, current_r, current_c, "West", options)

            # Lastly, check that there is room to the EAST
            if current_c < m.numColumns - 1:
                addDirectionOption(m, current_r, current_c, "East", options)

            # Now options should only a max of 4 options. These will exclude
            # walls and locations that have already been visited.
            assert(len(options) <= 4)

            # If options is empty (i.e surrounded by visited/walls):
            # There are no directions we can move from the current cell! We
            # need to backtrack.
            # Note option size cannot be negative.
            if len(options) == 0:
                path.pop()

            # Now we can continue the loop.
            else:

            # Choose a random direction! Then, clear the wall in that 
            # direction, and move into the next cell.
                dir_rand = random.choice(options)

            # Now, clear the wall in that direction and 
            # move into the next cell.
                m.clearWall(current_r, current_c, dir_rand)
                (next_row, next_col) = m.getNeighborCell(current_r, \
                                                         current_c, \
                                                         dir_rand)

            # Mark the cell at next location as VISITED. 
            # Note that START is already marked as VISITED.
                m.setVisited(next_row, next_col)
                m.setCellNum(next_row, next_col, len(path))

            # Append next location onto the path.
                path.append((next_row, next_col))

    # Return the competed maze
    return m
        
        

def main(numPlayers):

    # We first want to generate the maze
    m = genMaze()

    m.print()
    testlist = sorted(m.cellNumToExit)
    print("Sorted List:", testlist[len(testlist):len(testlist) - 10:-1])
    print(findFurthestSharedCell(m))

    # Now we want to designate the start values given the results of the
    # two shared locations that are furthest away.
    furthestSharedNum = findFurthestSharedCell(m)
    sharedCells = findAllIndices(m.cellNumToExit, furthestSharedNum)

    for player in range(numPlayers):
        playerCell = m.getCoordFromIndex(sharedCells[player])
        m.start.append(playerCell)
        # indexNum = m.cellNumToExit.index(furthestSharedNum)
        # playerCell = m.getCoordFromIndex(indexNum)
        # m.start.append(playerCell)
        print(playerCell)

    m.print(verbose = False)


if __name__ == '__main__':
    main(2)
