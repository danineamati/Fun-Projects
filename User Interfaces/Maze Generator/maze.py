MazeCell = ["Empty", "Wall", "Visited"]
Direction = ["North", "East", "South", "West"]

class Maze:
    '''Provides all necessary methods to make a maze.'''
    def __init__(self, rows, columns):
        self.numRows = rows
        self.numColumns = columns
        self.cells = []
        self.clear()
        self.start = (0,0)
        self.end = (rows - 1, columns - 1)


    def getExpArrayIndex(self, cellRow, cellColumn):
        '''Take 2D coordinates and compute the corresponding 1D array index.
        Input location must be in cell coordinates'''
        exp_r = 2 * cellRow + 1
        exp_c = 2 * cellColumn + 1
        total_col = 2 * self.numColumns + 1
        return(exp_r * total_col + exp_c)


    def getArrayIndex(self, row, column):
        '''Take 2D expanded coordinates and compute the corresponding 1D array
        index. Input location must be in expanded coordinates'''
        total_cols = 2 * self.numColumns + 1
        return (row * total_cols + column)


    def getCellArrayCoord(self, cellRow, cellColumn):
        '''Returns the expanded coordinates of the specified cell coordinates'''
        exp_r = 2 * cellRow + 1
        exp_c = 2 * cellColumn + 1
        return (exp_r, exp_c)


    def getWallArrayCoord(self, cellRow, cellColumn, direction):
        '''Returns the expanded coordinates of the wall on a specific side of
        a cell given in cell coordinates'''
        (exp_row, exp_col) = self.getCellArrayCoord(cellRow, cellColumn)
        if direction == "North":
            return (exp_row - 1, exp_col)
        elif direction == "South":
            return (exp_row + 1, exp_col)
        elif direction == "West":
            return (exp_row, exp_col - 1)
        elif direction == "East":
            return (exp_row, exp_col +1)


    def clear(self):
        '''Sets all cells and walls to be empty, so that the maze is
        completely cleared'''
        for row in range(2 * self.numRows + 1):
            for column in range(2 * self.numColumns + 1):
                self.cells.append(MazeCell[0])


    def getCell(self, cellRow, cellColumn):
        '''Returns the value of the specified'''
        return self.cells[self.getExpArrayIndex(cellRow, cellColumn)]


    def setCell(self, cellRow, cellColumn, MazeCell_val):
        '''Puts maze cell val at designated row and column'''
        self.cells[self.getExpArrayIndex(cellRow, cellColumn)] = MazeCell_val


    def getNeighborCell(self, cellRow, cellCol, direction):
        '''Returns the cell-coordinates of the neighboring cell in the specified
        direction. Trips an assertion if the given cell has no neighbor in the
        specified direction (e.g. the NORTH neighbor of cell (0,5))'''
        if direction == "North":
            assert(cellRow - 1 >= 0)
            return (cellRow - 1, cellCol)
        elif direction == "South":
            assert(cellRow + 1 <= self.numRows)
            return (cellRow + 1, cellCol)
        elif direction == "West":
            assert(cellCol - 1 >= 0)
            return (cellRow, cellCol - 1)
        elif direction == "East":
            assert(cellCol + 1 <= self.numColumns)
            return (cellRow, cellCol + 1)


    def hasWall(self, cellRow, cellCol, direction):
        '''Returns true if there is a wall in the specified direction from the
        given cell, false otherwise'''
        (exp_row, exp_col) = self.getWallArrayCoord(cellRow, cellCol, direction)
        index = self.getArrayIndex(exp_row, exp_col)
        if self.cells[index] == "Wall":
            return True
        return False


    def setWall(self, cellRow, cellCol, direction):
        '''Puts a wall on the specified side of the given cell'''
        (exp_row, exp_col) = self.getWallArrayCoord(cellRow, cellCol, direction)
        self.cells[self.getArrayIndex(exp_row, exp_col)] = "Wall"


    def clearWall(self, cellRow, cellCol, direction):
        '''Removes a wall on the specified side of the given cell'''
        (exp_row, exp_col) = self.getWallArrayCoord(cellRow, cellCol, direction)
        index = self.getArrayIndex(exp_row, exp_col)
        self.cells[index] = "Empty"


    def setAllWalls(self):
        '''Places a wall at every location that can be a wall in the maze'''
        for r in range(self.numRows):
            for c in range(self.numColumns):
                self.setWall(r, c, "North")
                self.setWall(r, c, "West")
                self.setWall(r, c, "South")
                self.setWall(r, c, "East")


    def isVisited(self, cellRow, cellCol):
        '''Returns true if the specified maze cell has been visited'''
        if self.getCell(cellRow, cellCol) == "Visited":
            return True
        return False


    def setVisited(self, cellRow, cellCol):
        '''Changes the cell's value to VISITED'''
        self.setCell(cellRow, cellCol, "Visited")


    def print(self):
        '''Outputs the maze using simple ASCII-art to the specified output.
        The output format is as follows, using the example maze from the
        assignment write-up.  (The text to the right of the maze is purely
        explanatory, and you don't need to output it.)
        
        3 4               (# of rows and then # of columns)
        +---+---+---+---+ (each cell is 3 spaces wide, with a + at each corner)
        | S     |       |   (walls indicated by --- or |)
        +---+   +   +   +   (start indicated by S, end indicated by E)
        |   |   |   |   |
        +   +   +   +   +
        |           | E |
        +---+---+---+---+
        '''
        print()
        print(self.numRows, self.numColumns)

        top_wall = '+'
        for c in range(self.numColumns):
            if self.hasWall(0, c, "North"):
                top_wall += '---+'
            else:
                top_wall += '   +'
        print(top_wall)

        def print_cell(content, r, c):
            '''Prints the cell and the wall for a given content'''
            current = content
            if self.hasWall(r, c, "East"):
                current += '|'
            else:
                current += ' '
            return current
        
        for r in range(self.numRows):
            current_row = ''

            if self.hasWall(r, 0, "West"):
                current_row += '|'
            else:
                current_row += ' '
            
            for c in range(self.numColumns):
                if self.start == (r, c):
                    current_row += print_cell(' S ', r, c)
                        
                elif self.end == (r, c):
                    current_row += print_cell(' E ', r, c)

                elif self.getCell(r, c) == "Empty":
                    current_row += print_cell('   ', r, c)

                elif self.getCell(r, c,) == "Visited":
                    current_row += print_cell('   ', r, c)
                        
                elif self.getCell(r, c,) == "Wall":
                    current_row += print_cell(' W ', r, c)

            print(current_row)

            current_floor = '+'
            if r < self.numRows:
                for c in range(self.numColumns):
                    if self.hasWall(r, c, "South"):
                        current_floor += '---+'
                    else:
                        current_floor += '   +'
                print(current_floor)
        

    

