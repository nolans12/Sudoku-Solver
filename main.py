from imports import *
from image_process import process_sudoku_image
from solver import solve_sudoku

if __name__ == "__main__":

    # Create and configure the tkinter root window
    root = tk.Tk()
    root.withdraw()
    root.attributes('-topmost', True)  # Make window topmost
    
    # Get current working directory
    current_dir = os.getcwd()
    
    # Open file dialog starting from current directory
    image_path = filedialog.askopenfilename(
        title="Select Sudoku Image",
        initialdir=current_dir,
        filetypes=[("Image files", "*.png *.jpg *.jpeg")]
    )
    
    if image_path == "":
        print("No file selected. Exiting...")
        exit()
        
    initial_board = process_sudoku_image(image_path)
    # print(initial_board)

    # Now that we have the board, optimize using MILP
    solved_board = solve_sudoku(initial_board)

    # Print the solved board, highlighting new values in red
    # Clear terminal screen
    print("\033[H\033[J", end="", flush=True)
    print("Solved Board:\n")
    for i in range(9):
        if i % 3 == 0 and i != 0:
            print('-' * 22)
        for j in range(9):
            if j % 3 == 0 and j != 0:
                print('|', end=' ')
            
            # If the value is new (different from initial), print in red
            if initial_board[i][j] != solved_board[i][j]:
                print('\033[91m{}\033[0m'.format(solved_board[i][j]), end=' ')
            else:
                print(solved_board[i][j], end=' ')
        print()
    print()
