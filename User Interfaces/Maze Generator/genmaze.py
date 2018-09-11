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

def usage(name):
    ''' Show usage imformation for our program'''
    print("usage:", name, "n f")
    print("n is an integer of total maze rows")
    print("f is an integer of total maze columns")

def main():
    ''' This function generates the maze'''
    if len(sys.argv) < 3:
        print("Too Few Arguments!")
        usage(sys.argv[0])
        # print(sys.argv)

    elif len(sys.argv) > 3:
        print("Too Many Arguments!")
        usage()
        # print(sys.argv)

    else:
        m = Maze(int(sys.argv[1]), int(sys.argv[2]))
        m.clear()
        m.setAllWalls()
        m.setVisited(m.start[0], m.start[1])
        
        path = []

        path.append(m.start)

        # m.print()

        while not len(path) == 0:
            # Add current location to the path
            (current_r, current_c) = path[len(path) - 1]

            # If the current location is the end we need to backtrack
            # to finish filling the maze
            if (current_r, current_c) == m.end:
                p = path.pop()
                
            # This list will contain the direction options to expand the 
            # maze from the current Location.
            # IMPORTANT: We want options to reset after every loop
            else:
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

                # Append next location onto the path.
                    path.append((next_row, next_col))
        m.print()




main()
