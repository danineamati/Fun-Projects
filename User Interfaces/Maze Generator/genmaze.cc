#include "maze.hh"

#include <cstdlib>
#include <ctime>
#include <iostream>
#include <vector>
#include <cassert>

using namespace std;

// Adds a direction to the vector of possible directions
void addDirectionOption(const Maze &maze, const Location &current, 
	Direction dir, vector<Direction> &v) {

	Location Neighbor = maze.getNeighborCell(current.row, current.col, dir);
	// Check if the Neighbor cell has been visited
	if (!maze.isVisited(Neighbor.row, Neighbor.col)) {
		// If it has not been visited, append to the direction option vector
		v.push_back(dir);
	}
}

// Check has number of walls
int numWalls(const Maze &maze, int cellRow, int cellCol) {
	int Wall_num = 0;

	if (maze.hasWall(cellRow, cellCol, Direction::NORTH))
		Wall_num++;
	if (maze.hasWall(cellRow, cellCol, Direction::EAST))
		Wall_num++;
	if (maze.hasWall(cellRow, cellCol, Direction::SOUTH))
		Wall_num++;
	if (maze.hasWall(cellRow, cellCol, Direction::WEST))
		Wall_num++;

	return Wall_num;
}


// Show usage information for our program
void usage(const char *program) {
	cout << "usage: " << program << " n f" << endl;
	cout << "\tn is an integer of total maze rows." << endl;
	cout << "\tf is an integer of total maze columns." << endl;
}

int main(int argc, char const *argv[])
{
	if (argc < 3) {
		cout << "Too few arguments!" << endl;
		usage(argv[0]);
		return 1;
	}

	else if (argc > 3) {
		cout << "Too many arguments!" << endl;
		usage(argv[0]);
		return 1;
	}
	
	cout << "Maze of " << argv[1] << " rows and " << argv[2] << " columns:";
	srand(time(NULL));
	
	// Variables:
	int rows = atoi(argv[1]);
	int cols = atoi(argv[2]);

	//cout << rows << ' ' << cols << endl;

	Maze m(rows, cols);
	vector<Location> path;

	// Clear the maze
	m.clear();
	//m.print(cout);

	// Fill in all the walls
	m.setAllWalls();
	//m.print(cout);

	// Set start to visited
	m.setVisited(m.getStart().row, m.getStart().col);
	//m.print(cout);

	// Append start of maze onto the path
	path.push_back(m.getStart());

	
	// vector::empty() returns true if vector has no elements
	// vector::back() returns the last element of the vector
	// vector::pop_back() removes thet last element of the vector 
	//     it does not return anything
	// While path is not empty:
	while (!path.empty()) {

		// Add the current location to the path
		Location current = path.back();

		// If the current location is the end we need to backtrack
		// to finish filling the maze
		if (current == m.getEnd()) {
			//cout << "Generator as reached the end of the maze." << endl;
			path.pop_back();
		}

		else {
			// This vector will contain the direction options to expand the 
			// maze from the current Location.
			// IMPORTANT: We want options to reset after every loop
			vector<Direction> options;

			// Check that there is room to the NORTH
			if (current.row > 0)
				addDirectionOption(m, current, Direction::NORTH, options);
			// Also check that there is room to the SOUTH
			if (current.row < m.getNumRows() - 1)
				addDirectionOption(m, current, Direction::SOUTH, options);
			// Also check that there is room to the WEST
			if (current.col > 0)
				addDirectionOption(m, current, Direction::WEST, options);
			// Lastly, check that there is room to the EAST
			if (current.col < m.getNumCols() - 1)
				addDirectionOption(m, current, Direction::EAST, options);

			// Now options should only a max of 4 options. These will exclude walls
			// and locations that have already been visited.
			assert(options.size() <= 4);

			// If options is empty (i.e surrounded by visited/walls):
			// There are no directions we can move from the current cell! We
			// need to backtrack.
			// Note option size cannot be negative.
			if (options.size() == 0)
				path.pop_back();
			// Now we can continue the loop.
			else {
				/*cout << "Of ";
				for (size_t i = 0; i < options.size(); ++i)
				{
					cout << (int) options[i] << ", ";
				} */

				// Choose a random direction! Then, clear the wall in that 
				// direction, and move into the next cell.
				Direction dir_rand = options[rand() % options.size()];
				//cout << "chose " << (int) dir_rand << endl;
				
				// Now, clear the wall in that direction and 
				// move into the next cell.
				m.clearWall(current.row, current.col, dir_rand);
				Location next = m.getNeighborCell(current.row, current.col, 
					dir_rand);
				// Mark the cell at next location as VISITED. 
				// Note that START is already marked as VISITED.
				m.setVisited(next.row, next.col);

				// Append next location onto the path.
				path.push_back(next);
			}
		}
		// cout << "Looped!" << endl;

	}

	assert(numWalls(m, m.getStart().row, m.getStart().col) == 3);
	assert(numWalls(m, m.getEnd().row, m.getEnd().col) == 3);
	assert(m.isVisited(m.getStart().row, m.getStart().col));
	assert(m.isVisited(m.getEnd().row, m.getEnd().col));

	m.print(cout);
	/*
	cout << numWalls(m, m.getStart().row, m.getStart().col) << endl;
	cout << numWalls(m, m.getEnd().row, m.getEnd().col) << endl;
	cout << m.isVisited(m.getEnd().row, m.getEnd().col) << endl;
	cout << true << endl;
	*/

	return 0;
}