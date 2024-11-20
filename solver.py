# Uses a MILP to solve the sudoku puzzle
from imports import *
from ortools.sat.python import cp_model

def solve_sudoku(board):
    
    # Create the model
    model = cp_model.CpModel()

    # Create the variables, for every cell in the board, we have a variable that can be between 1 and 9
    variables = {}
    height, width = board.shape
    for i in range(height):
        for j in range(width):
            variables[(i, j)] = model.NewIntVar(1, 9, f'x_{i}_{j}')

            
    # Now that we have the variables, need to add the constraints

    # First, add the constraint that for every element in the board that has a value (not 0), the variable must be equal to that value
    for i in range(height):
        for j in range(width):
            if board[i][j] != 0:
                model.Add(variables[(i, j)] == board[i][j])

    # Now, each row must have the numbers 1 through 9 exactly once
    for i in range(height):
        model.AddAllDifferent([variables[(i, j)] for j in range(width)])

    # Each column must have the numbers 1 through 9 exactly once
    for j in range(width):
        model.AddAllDifferent([variables[(i, j)] for i in range(height)])

    # Each 3x3 subgrid must have the numbers 1 through 9 exactly once
    for i in range(0, height, 3):
        for j in range(0, width, 3):
            model.AddAllDifferent([variables[(i+k, j+l)] for k in range(3) for l in range(3)])

    # Now, we need to solve the model
    solver = cp_model.CpSolver()
    solver.Solve(model)

    # Extract the new solution
    new_board = np.zeros((height, width), dtype=np.int32)
    for i in range(height):
        for j in range(width):
            new_board[i][j] = solver.Value(variables[(i, j)])

    return new_board