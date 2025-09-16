import random

#Defining constants for the remainder of the program
FINISH_SUCCESS = "FINISH_SUCCESS"
FINISH_FAILURE = "FINISH_FAILURE"
NOT_FINISH = "NOT_FINISH"

#Defining a constant that represents the name of the output file that will store the Sudoku solving results
FILE_NAME = "solved_sudoku.txt"


with open(FILE_NAME,"w") as file:
    file.write("Sudoku solving results:\n\n")

#Checks whether the current Sudoku board setup is valid (no duplicates in any row, column, or 3x3 block)
def is_valid_board (sudoku_board: list) -> bool:
    for i in range(9):
        row = []
        for num in sudoku_board[i]: #Checks if there are any duplicates in the row
            if num != -1:
                if num in row:
                    return False
                row.append(num)

        col = []
        for r in range(9): #Checks if there are any duplicates in the column
            if sudoku_board[r][i] != -1:
                if sudoku_board[r][i] in col:
                    return False
                col.append(sudoku_board[r][i])

    for start_row in range(0,9,3): #Checks if there are any duplicates in the 3x3 block
        for start_col in range(0,9,3):
            block = []
            for r in range(start_row, start_row + 3):
                for c in range(start_col, start_col + 3):
                    value = sudoku_board[r][c]
                    if value != -1:
                        if value in block:
                            return False
                        block.append(value)

    return True


def options(sudoku_board: list, loc: tuple):
    i = loc[0]
    j = loc[1]
    full_lst = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    if sudoku_board[i][j] != -1:
        return []
    else:
        for row in sudoku_board[i]:           #checking the row
            if row != -1 and row in full_lst:
                full_lst.remove(row)
        for col in sudoku_board:               #checking the column
            if col[j] != -1 and col[j] in full_lst:
                full_lst.remove(col[j])
        start_row = (i // 3) * 3
        start_col = (j // 3) * 3
        for r in range(start_row , start_row + 3):           #checking the 3X3 box
            for c in range(start_col, start_col + 3):
                if sudoku_board[r][c] != -1 and sudoku_board[r][c] in full_lst:
                    full_lst.remove(sudoku_board[r][c])
        if len(full_lst) == 0:
            return None
        else:
            return full_lst


def possible_digits(sudoku_board: list) -> list:
    #Initialize a 9x9 structure to store possible options for each cell
    possible_options_board = [ [ ] , [ ] , [ ] , [ ] , [ ] , [ ] , [ ] , [ ], [ ] ]
    for i in range(len(sudoku_board)):
        for j in range(len(sudoku_board[i])):
            if sudoku_board[i][j] != -1:
                possible_options_board[i].append([]) #If the cell is already filled, then no further options are needed
            else:
                full_lst = options(sudoku_board,(i,j)) #The cell is empty, so we check valid options by calling the function options

                if full_lst is None: #It means there are no valid digits for the cell
                    possible_options_board[i].append(None)
                else:
                    possible_options_board[i].append(full_lst) #Otherwise, we store the valid digits

    return possible_options_board


#Removes the chosen value from all related rows, columns and 3x3 boxes in the possibilities grid, ensuring no duplications of that digit
def update_possibilities (possibilities: list, row: int, col: int, value: int):

    for c in range(9): #updating the row
        if value in possibilities[row][c]:
            if len(possibilities[row][c]) == 1 and possibilities[row][c][0] == value:
                return FINISH_FAILURE
            else:
                possibilities[row][c].remove(value)

    for r in range(9): #updating the column
        if value in possibilities[r][col]:
            if len(possibilities[r][col]) == 1 and possibilities[r][col][0] == value:
                return FINISH_FAILURE
            else:
                possibilities[r][col].remove(value)

    start_row = (row // 3) * 3
    start_col = (col // 3) * 3
    for r in range(start_row, start_row + 3):  # updating the 3X3 box
        for c in range(start_col, start_col + 3):
            if value in possibilities[r][c]:
                if len(possibilities[r][c]) == 1 and possibilities[r][c][0] == value:
                    return FINISH_FAILURE
                else:
                    possibilities[r][c].remove(value)


def one_stage(sudoku_board: list, possibilities: list):
    #This boolean variable tracks whether we managed to fill any cell during the current iteration
    something_filled = True

    #Keeps filling cells that have exactly one possible digit
    while something_filled:
        something_filled = False
        for i in range(9):
            for j in range(9):
                if sudoku_board[i][j] != -1: #If the cell is already filled
                    continue

                if possibilities[i][j] is None:
                    return FINISH_FAILURE

                if len(possibilities[i][j]) == 1: #If there's exactly one possibility, fill the cell with that value
                    value = possibilities[i][j][0]
                    sudoku_board[i][j] = value
                    possibilities[i][j] = []
                    update_result = update_possibilities(possibilities,i,j,value)
                    if update_result == FINISH_FAILURE:
                        return FINISH_FAILURE
                    something_filled = True #Since we filled a cell, we might be able to fill more cell in the next iteration

    #After no more automatic fills are possible, check if the board is fully filled
    filled_all = True
    for i in range(9):
        for j in range(9):
            if sudoku_board[i][j] == -1:
                filled_all = False
                break
        if not filled_all:
            break

    #If the board is complete, we return success
    if filled_all:
        return FINISH_SUCCESS

    #If the board is incomplete, we find the unfilled cell with the fewest possible options
    min_possibilities = 10
    loc = None
    for i in range(9):
        for j in range(9):
            if sudoku_board[i][j] != -1: #Skip cells that are already filled
                continue

            if sudoku_board[i][j] == -1:
                if possibilities[i][j] is None: #If there are no options for an empty cell, it's a contradiction
                    return FINISH_FAILURE
            if len(possibilities[i][j]) == 0: #If
                return FINISH_FAILURE

            #Update the cell with the least number of possibilities
            if len(possibilities[i][j]) < min_possibilities:
                min_possibilities = len(possibilities[i][j])
                loc = (i,j)

    #If we still didn't find a cell, which shouldn't happen if the board isn't full, it's a failure
    if loc is None:
        return FINISH_FAILURE

    #Return the location with the fewest possibilities
    return loc, NOT_FINISH


def fill_board(sudoku_board: list, possibilities: list):
    while True:
        result = one_stage(sudoku_board,possibilities) #result represents the current state of the Sudoku solving process
        if result == FINISH_SUCCESS:
            return FINISH_SUCCESS
        elif result == FINISH_FAILURE:
            return FINISH_FAILURE
        else: #result = loc, NOT_FINISH
            current_loc, status = result

        print("The board is not finished yet")
        print("In the location:" ,current_loc, "The current possibilities are:" ,possibilities[current_loc[0]][current_loc[1]])
        #presents the user with the current option for a specific location in the board

        try:
            user_answer = int(input("Please choose one number: "))
            while user_answer not in possibilities[current_loc[0]][current_loc[1]]:
                #if the user׳s input is a number but not part of the options

                print("That option does not exists")
                print("In the location:" ,current_loc, "The current possibilities are:" ,possibilities[current_loc[0]][current_loc[1]])
                user_answer = int(input("please choose a valid option: "))

            sudoku_board[current_loc[0]][current_loc[1]] = user_answer #updates the board with the user's answer
            possibilities[current_loc[0]][current_loc[1]] = [] #updates the possibilities board with an empty slot
            update_outcome = update_possibilities(possibilities, current_loc[0],current_loc[1], user_answer)

            if update_outcome == FINISH_FAILURE:
                return FINISH_FAILURE

        except ValueError: #if the user's input is not a number
            print("Invalid input. Please enter a valid number")


def create_random_board (sudoku_board: list):
    for r in range(9): #Resetting the Sudoku board
        for c in range(9):
            if sudoku_board[r][c] != -1:
                sudoku_board[r][c] = -1

    N = random.randrange(10,21)

    positions = []
    for r in range(9): #Creating a list of possible positions
        for c in range(9):
            positions.append((r,c))

    for i in range(N):
        K = random.randrange(1,len(positions)+1)
        R,C = positions[K-1]

        options_for_a_cell = options(sudoku_board,positions[K-1])  #Recieving a list of options for a specific cell

        if not options_for_a_cell: #If the list is empty, go to the next iteration
            continue

        sudoku_board[R][C] = random.choice(options_for_a_cell)

        positions.pop(K-1)


def board_structure(sudoku_board: list):
    result = "---------------------------\n"
    for row in sudoku_board:
        row_board = '|'
        for num in row:
            if num == -1:
                row_board += '  |'
            else:
                row_board += str(num) + ' |'
        result += row_board + '\n'
        result += "---------------------------\n"

    return result


def print_board (sudoku_board: list):
    print(board_structure(sudoku_board))


#This function uses the board_structure function in order to print the Sudoku board into the file
def print_board_to_file (sudoku_board: list, file_name: str):
    with open(file_name,"a") as f:
        f.write("=" *30 + "\n")
        f.write("Here is the solved board:\n")
        f.write(board_structure(sudoku_board) + "\n")

#This function first checks if the board is valid, if it is valid, it continues to solve it and then print it to the file
def process_board (sudoku_board: list, file_name: str):
    if not is_valid_board(sudoku_board): #Checks whether the file is valid or not
        with open(file_name, "a") as f:
            f.write("Board is not legit!\n\n")
    else:
        possibilities_board = possible_digits(sudoku_board) #Returns a grid of valid digit options for each empty cell on the Sudoku board
        result = fill_board(sudoku_board, possibilities_board) #Attempts to solve the board using the current possibilities

        if result == FINISH_FAILURE:
            with open(file_name, "a") as f:
                f.write("Board is unsolvable\n\n")
        elif result == FINISH_SUCCESS:
            print_board_to_file(sudoku_board, file_name)



board = [[5,3,-1,-1,7,-1,-1,-1,-1],
         [6,-1,-1,-1,-1,-1,1,-1,-1],
         [-1,-1,9,-1,-1,-1,-1,6,-1],
         [-1,-1,-1,-1,6,-1,-1,-1,3],
         [-1,-1,-1,8,-1,3,-1,-1,1],
         [-1,-1,-1,-1,-1,-1,-1,-1,-1],
         [-1,6,-1,-1,-1,-1,-1,-1,-1],
         [-1,-1,-1,-1,1,-1,-1,-1,-1],
         [-1,-1,-1,-1,8,-1,-1,-1,9]]

process_board(board,FILE_NAME)


board = [[5,3,4,6,7,8,9,1,2],
         [6,7,2,1,9,5,3,4,8],
         [1,9,8,3,4,2,5,6,7],
         [8,5,9,7,6,1,4,2,3],
         [4,2,6,8,5,3,7,9,1],
         [7,1,3,9,2,4,8,5,6],
         [9,6,1,5,3,7,2,8,4],
         [2,8,7,4,1,9,6,3,5],
         [3,4,5,2,8,6,1,7,9]]

process_board(board,FILE_NAME)


board = [[5,1,6,8,4,9,7,3,2],
         [3,-1,7,6,-1,5,-1,-1,-1],
         [8,-1,9,7,-1,-1,-1,6,5],
         [1,3,5,-1,6,-1,9,-1,7],
         [4,7,2,5,9,1,-1,-1,6],
         [9,6,8,3,7,-1,-1,5,-1],
         [2,5,3,1,8,6,-1,7,4],
         [6,8,4,2,-1,7,5,-1,-1],
         [7,9,1,-1,5,-1,6,-1,8]]

process_board(board,FILE_NAME)


board = [[5,3,4,6,7,8,9,1,2],
         [6,7,2,1,9,5,3,4,9],
         [1,9,8,3,4,2,5,6,7],
         [8,5,9,7,6,1,4,2,3],
         [4,2,6,8,5,3,7,9,1],
         [7,1,3,9,2,4,8,5,6],
         [9,6,1,5,3,7,2,8,4],
         [2,8,7,4,1,9,6,3,5],
         [3,4,5,2,8,6,1,7,9]]

process_board(board,FILE_NAME)


board = [[5,3,4,6,7,8,9,1,2],
         [6,7,2,1,9,5,3,4,8],
         [1,9,8,3,4,2,5,6,7],
         [-1,-1,-1,7,6,1,4,2,3],
         [-1,-1,-1,8,5,3,7,9,1],
         [-1,-1,-1,9,2,4,8,5,6],
         [-1,-1,-1,-1,3,7,2,8,4],
         [-1,-1,-1,-1,1,9,6,3,5],
         [-1,-1,-1,-1,8,6,1,7,9]]

process_board(board,FILE_NAME)


board = [[-1,-1,-1,-1,-1,-1,-1,-1,-1],
         [-1,-1,-1,-1,-1,-1,-1,-1,-1],
         [-1,-1,-1,-1,-1,-1,-1,-1,-1],
         [-1,-1,-1,-1,-1,-1,-1,-1,-1],
         [-1,-1,-1,-1,-1,-1,-1,-1,-1],
         [-1,-1,-1,-1,-1,-1,-1,-1,-1],
         [-1,-1,-1,-1,-1,-1,-1,-1,-1],
         [-1,-1,-1,-1,-1,-1,-1,-1,-1],
         [-1,-1,-1,-1,-1,-1,-1,-1,-1]]

create_random_board(board)

process_board(board,FILE_NAME)
