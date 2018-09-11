#include "maze.hh"
#include <cassert>

using namespace std;


// Initialize a new maze of size rows x cols
Maze::Maze(int rows, int cols) {
	numRows = rows;
	numCols = cols;

	// The maze's "expanded representation"
	cells = new MazeCell[((2 * rows) + 1) * ((2 * cols) + 1)];
	//cout << "Constructor: " << rows << ' ' << cols;
	//cout << ". Max = " << ((2 * rows) + 1) * ((2 * cols) + 1);

	// Set all cells to EMPTY
	clear();

	// Loop through every value in the array
	/*
	for (int i = 0; i < ((2 * numRows) + 1) * ((2 * numCols) + 1); ++i)
	{
		// Initialize all values to empty
        cells[i] = MazeCell::EMPTY;
	}
	*/

    // The start of the maze, in cell coordinates
    start = Location();
    // The end of the maze, in cell coordinates
    end = Location(rows - 1, cols - 1);
}

  
// Make a copy of an existing maze object
Maze::Maze(const Maze &m) {
	numRows = m.numRows;
	numCols = m.numCols;

	cells = new MazeCell[((2 * numRows) + 1) * ((2 * numCols) + 1)];

	// Whereas the constructor set everything to EMPTY,
	// Here, we want to copy the contents of the cells
	for (int i = 0; i < ((2 * numRows) + 1) * ((2 * numCols) + 1); ++i)
	{
		// Initialize all values to empty
        cells[i] = m.cells[i];
	}

	start = m.start;
	end = m.end;

}
    
// Maze destructor
Maze::~Maze() {
	delete[] cells;
}
   
// Maze assignment operator
Maze & Maze::operator=(const Maze &m) {
	// this == &current_maze (not m)
	if (this != &m) {
		delete[] cells;

		numRows = m.numRows;
		numCols = m.numCols;

		cells = new MazeCell[((2 * numRows) + 1) * ((2 * numCols) + 1)];

		// Whereas the constructor set everything to EMPTY,
		// Here, we want to copy the contents of the cells
		for (int i = 0; i < ((2 * numRows) + 1) * ((2 * numCols) + 1); ++i)
		{
			// Initialize all values to empty
    	    cells[i] = m.cells[i];
		}

		start = m.start;
		end = m.end;
	}
	
	return *this;
}










// Take 2D coordinates and compute the corresponding 1D array index
// Input location must be in cell coordinates
int Maze::getExpArrayIndex(const Location &loc) const{
	int r_exp = 2 * loc.row + 1;
	int c_exp = 2 * loc.col + 1;
	int total_cols = 2 * (numCols) + 1;
	//cout << "total_Cols: " << total_cols << '.';
	return (r_exp * total_cols + c_exp);
}

// Take 2D expanded coordinates and compute the corresponding 1D array index
// Input location must be in expanded coordinates
int Maze::getArrayIndex(const Location &loc) const{
	int total_cols = 2 * (numCols) + 1;
	return (loc.row * total_cols + loc.col);
}

// Returns the expanded coordinates of the specified cell coordinates
Location Maze::getCellArrayCoord(int cellRow, int cellCol) const{
	int r_exp = 2 * cellRow + 1;
	int c_exp = 2 * cellCol + 1;
	return Location(r_exp, c_exp);
}

// Returns the expanded coordinates of the wall on a specific side of
// a cell given in cell coordinates
Location Maze::getWallArrayCoord(int cellRow, int cellCol,
	Direction direction) const
{
	// Convert to expanded coordinates
	Location Loc_exp = getCellArrayCoord(cellRow, cellCol);

	if (direction == Direction::NORTH) {
		return Location(Loc_exp.row - 1, Loc_exp.col);
	}
	else if (direction == Direction::SOUTH) {
		return Location(Loc_exp.row + 1, Loc_exp.col);
	}
	else if (direction == Direction::WEST) {
		return Location(Loc_exp.row, Loc_exp.col - 1);
	}
	else  //(direction == Direction::EAST) 
	{
		return Location(Loc_exp.row, Loc_exp.col + 1);
	}
}



// Returns the number of rows in the maze
int Maze::getNumRows() const{
	return numRows;
}
    
// Returns the number of columns in the maze
int Maze::getNumCols() const{
	return numCols;
}

// Returns the starting point in the maze in cell coordinates
Location Maze::getStart() const{
	return start;
}

// Sets the starting point in the maze    
void Maze::setStart(int row, int col) {
	start = Location(row, col);
}

// Returns the ending point in the maze in cell coordinates    
Location Maze::getEnd() const{
	return end;
}
    
// Sets the ending point in the maze
void Maze::setEnd(int row, int col) {
	end = Location(row, col);
}
    

// Sets all cells and walls to be empty, so that the maze is
// completely cleared
void Maze::clear(){
	for (int i = 0; i < ((2 * numRows) + 1) * ((2 * numCols) + 1); ++i)
	{
		// Initialize all values to empty
        cells[i] = MazeCell::EMPTY;
	}
}

// Returns the value of the specified
MazeCell Maze::getCell(int cellRow, int cellCol) const{
	return cells[getExpArrayIndex(Location(cellRow, cellCol))];
}

void Maze::setCell(int cellRow, int cellCol, MazeCell val){
	cells[getExpArrayIndex(Location(cellRow, cellCol))] = val;
}

// Returns the cell-coordinates of the neighboring cell in the specified
// direction.  Trips an assertion if the given cell has no neighbor in the
// specified direction (e.g. the NORTH neighbor of cell (0,5)).
Location Maze::getNeighborCell(int cellRow, int cellCol,
                             Direction direction) const{
	if (direction == Direction::NORTH) {
		assert(cellRow - 1 >= 0);
		return Location(cellRow - 1, cellCol);
	}
	else if (direction == Direction::SOUTH) {
		assert(cellRow + 1 <= numRows);
		return Location(cellRow + 1, cellCol);
	}
	else if (direction == Direction::WEST) {
		assert(cellCol - 1 >= 0);
		return Location(cellRow, cellCol - 1);
	}
	else  //(direction == Direction::EAST) 
	{
		assert(cellCol + 1 <= numCols);
		return Location(cellRow, cellCol + 1);
	}
}

// Returns true if there is a wall in the specified direction from the
// given cell, false otherwise
bool Maze::hasWall(int cellRow, int cellCol, Direction direction) const{
	//Loc_wall is in expanded coordinates
	Location Loc_wall = getWallArrayCoord(cellRow, cellCol, direction);
	int index = getArrayIndex(Loc_wall);
	if (cells[index] == MazeCell::WALL)
		return true;
	return false;
}

// Puts a wall on the specified side of the given cell
void Maze::setWall(int cellRow, int cellCol, Direction direction) {
	Location Loc_wall = getWallArrayCoord(cellRow, cellCol, direction);
	cells[getArrayIndex(Loc_wall)] = MazeCell::WALL;
}


// Removes a wall on the specified side of the given cell
void Maze::clearWall(int cellRow, int cellCol, Direction direction){
	Location Loc_wall = getWallArrayCoord(cellRow, cellCol, direction);
	int index = getArrayIndex(Loc_wall);
	cells[index] = MazeCell::EMPTY;
}

// Places a wall at every location that can be a wall in the maze
void Maze::setAllWalls() {
	for (int r = 0; r < numRows; r++) {
        for (int c = 0; c < numCols; c++) {
            setWall(r, c, Direction::NORTH);
            setWall(r, c, Direction::WEST);
            setWall(r, c, Direction::SOUTH);
            setWall(r, c, Direction::EAST);

            //setCell(r, c, MazeCell::EMPTY);
            }
        }
}



// Returns true if the specified maze cell has been visited.
bool Maze::isVisited(int cellRow, int cellCol) const{
	if (getCell(cellRow, cellCol) == MazeCell::VISITED)
		return true;
	return false;
}

// Changes the cell's value to VISITED
void Maze::setVisited(int cellRow, int cellCol){
	setCell(cellRow, cellCol, MazeCell::VISITED);
}


// Outputs the maze using simple ASCII-art to the specified output stream.
// The output format is as follows, using the example maze from the
// assignment write-up.  (The text to the right of the maze is purely
// explanatory, and you don't need to output it.)
//
// 3 4                 (# of rows and then # of columns)
// +---+---+---+---+   (each cell is 3 spaces wide, with a + at each corner)
// | S     |       |   (walls indicated by --- or |)
// +---+   +   +   +   (start indicated by S, end indicated by E)
// |   |   |   |   |
// +   +   +   +   +
// |           | E |
// +---+---+---+---+
void Maze::print(ostream &os) const{
	// Notify
	cout << endl;
	//cout << "Printing the Maze..." << endl;
	// Print number of rows and number of colums
	cout << numRows << ' ' << numCols << endl;
	assert(cells[0] == MazeCell::EMPTY && "The first cell was not EMPTY.");

	// Print the Top walls
	cout << '+';
	for (int c = 0; c < numCols; ++c) {
		if (hasWall(0, c, Direction::NORTH))
			cout << "---+";
		else
			cout << "   +";
	}
	cout << endl;

	// Print the cells
	
	for (int r = 0; r < numRows; ++ r) {
		// Print right most wall
		//cout << '|';
		if(hasWall(r, 0, Direction::WEST))
			cout << '|';
		else
			cout << ' ';

		for (int c = 0; c < numCols; ++c) {
			if (getStart() == Location(r, c)){
				cout << " S ";
				if (hasWall(r, c, Direction::EAST))
					cout << '|';
				else
					cout << ' ';
			}

			else if (getEnd() == Location(r, c)) {
				cout << " E ";
				if (hasWall(r, c, Direction::EAST))
					cout << '|';
				else
					cout << ' ';
			}

			else if (getCell(r, c) == MazeCell::EMPTY) {
				cout << "   ";
				//cout << r << ',' << c;
				//cout << getExpArrayIndex(Location(r, c)) << ' ';
				if (hasWall(r, c, Direction::EAST))
					cout << '|';
				else
					cout << ' ';
			}
			else if (getCell(r, c) == MazeCell::VISITED) {
				cout << "   ";
				// cout << " V ";
				if (hasWall(r, c, Direction::EAST))
					cout << '|';
				else
					cout << ' ';
			}
			// This last option should not happen...
			else if (getCell(r, c) == MazeCell::WALL) {
				cout << " W ";
				if (hasWall(r, c, Direction::EAST))
					cout << '|';
				else
					cout << ' ';
			}


		// Print the values of the next row of walls
		}
		if (r < numRows - 1) {
			cout << endl;
			cout << '+';
			for (int c = 0; c < numCols; ++c) {
				if (hasWall(r, c, Direction::SOUTH))
					cout << "---+";
				else
					cout << "   +";
			}
		}
		cout << endl;
	}

	// Print the Bottom walls
	cout << '+';
	for (int c = 0; c < numCols; ++c) {
		if (hasWall(numRows - 1, c, Direction::SOUTH))
			cout << "---+";
		else
			cout << "   +";
	}

	
	cout << endl;
}


