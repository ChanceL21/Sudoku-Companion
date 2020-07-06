from tkinter import Tk, Frame, Menu, Label
import copy
from random import randint, shuffle

counter = 0

class Cell:

    """ Cell object that contains a sudoku square. a 9x9 array of these objects will be made for program """

    def __init__(self, row, column, board, boxes, game, saved_boards):
        #create label that is put into specific box of sudoku frame
        self.label = Label(boxes[row//3][column//3], text="", fg="red", bg="white", width = 2, height = 1, font=('Sans','30'), borderwidth=1, relief="solid")
        #bind label functions
        self.label.bind("<Button-1>", self.left_click)
        #put label in specific location of box frame
        self.label.grid(row=row%3, column=column%3)
        self.row = row
        self.column = column
        #not a clue
        self.mutable = True

    # make current number appear when left click is hit if the cell is not a clue. also Modifies 2D array
    def left_click(self, event):
        if self.mutable:
            if game.current != None:
                game.current.label.configure(bg="white")
            if game.current == self:
                game.current = None
            else:
                game.current = self
                self.label.configure(bg="gold")
            #update(board, saved_boards, game)

class State:

    """ Contains game information on difficulty, version, and which square is selected, which can be modified directly through this object """

    def __init__(self):
        self.difficulty = None
        self.version = 0
        self.current = None

#solves the 2D array and the gui grid and prints out relative statement in gui window
def solve(board, grid, top_label, saved_boards, game):
    if check(board):
        top_label.config(text="The puzzle has already been solved")
    else:
        for i in range(9):
            for j in range(9):
                if grid[i][j].mutable:
                    board[i][j] = 0
        solve_grid(board)
        if counter == 1:
            top_label.config(text="The puzzle has now been solved")
            filled = 0
            while filled == 0:
                fill_grid(board)
                filled = 1
                for row in board:
                    if 0 in row:
                        filled = 0
        else:
            top_label.config(text="The puzzle is not solvable")
    if counter == 1:
        decrease_counter()

    for i in range(9):
        for j in range(9):
            if grid[i][j].mutable:
                grid[i][j].label.config(text=str(board[i][j]))

    update(board, saved_boards, game)

def clear(board, grid, top_label, saved_boards, game):
    top_label.config(text="Cleared")
    for i in range(9):
        for j in range(9):
            if grid[i][j].mutable:
                grid[i][j].label.configure(text="")
                board[i][j] = 0
    update(board, saved_boards, game)

#Based on Sudoku Generator Algorithm - www.101computing.net/sudoku-generator-algorithm/
#makes a new, random puzzle. takes in int number of spaces to be removed from a completed puzzle
def new_puzzle(attempts, board, grid):
    for i in range(9):
        for j in range(9):
            board[i][j] = 0
            grid[i][j].mutable = True
            grid[i][j].label.config(fg="red")
    fill_grid(board)
    global counter
    order = random_order()
    i = 0
    while attempts > 0 and i < 41:
      row1 = order[i][0]
      col1 = order[i][1]
      row2 = 8 - order[i][0]
      col2 = 8 - order[i][1]

      #Remember its cell value in case we need to put it back
      backup1 = board[row1][col1]
      backup2 = board[row2][col2]
      board[row1][col1] = 0
      board[row2][col2] = 0

      #Take a full copy of the grid
      #copyGrid = copy.deepcopy(board)
      #copyGrid = []
     # for r in range(9):
        # copyGrid.append([])
        # for c in range(9):
        #    copyGrid[r].append(board[r][c])

      #Count the number of solutions that this grid has (using a backtracking approach implemented in the solve_grid() function)
      solve_grid(board)

      #If the number of solution is different from 1 then we need to cancel the change by putting the value we took away back in the grid
      if counter != 1:
        board[row1][col1]=backup1
        board[row2][col2]=backup2
        #We could stop here, but we can also have another attempt with a different cell just to try to remove more numbers
      else:
          attempts -= 2
      i += 1
      counter = 0


#A backtracking/recursive function to check all possible combinations of numbers until a solution is found
#Based on Sudoku Generator Algorithm - www.101computing.net/sudoku-generator-algorithm/
def fill_grid(board):
    numberList = [1,2,3,4,5,6,7,8,9]
    #Find next empty cell
    for i in range(81):
        row = i//9
        col = i%9
        if board[row][col] == 0:
            shuffle(numberList)
            for value in numberList:
                #Check that this value has not already be used on this row
                if not value in board[row]:
                    #Check that this value has not already be used on this column
                    if not value in (board[0][col], board[1][col], board[2][col], board[3][col], board[4][col], board[5][col], board[6][col], board[7][col], board[8][col]):
                        #Identify which of the 9 squares we are working on
                        square = []
                        if row < 3:
                            if col < 3:
                                square = [board[i][0:3] for i in range(0, 3)]
                            elif col < 6:
                                square = [board[i][3:6] for i in range(0, 3)]
                            else:
                                square = [board[i][6:9] for i in range(0, 3)]
                        elif row < 6:
                            if col < 3:
                                square = [board[i][0:3] for i in range(3, 6)]
                            elif col < 6:
                                square = [board[i][3:6] for i in range(3, 6)]
                            else:
                                square = [board[i][6:9] for i in range(3, 6)]
                        else:
                            if col < 3:
                                square = [board[i][0:3] for i in range(6, 9)]
                            elif col < 6:
                                square = [board[i][3:6] for i in range(6, 9)]
                            else:
                                square = [board[i][6:9] for i in range(6, 9)]
                        #Check that this value has not already be used on this 3x3 square
                        if not value in (square[0] + square[1] + square[2]):
                            board[row][col] = value
                            if check(board):
                                return True
                            else:
                                if fill_grid(board):
                                    return True
            break
    board[row][col] = 0


#A backtracking/recursive function to check all possible combinations of numbers until a solution is found
#Based on Sudoku Generator Algorithm - www.101computing.net/sudoku-generator-algorithm/
def solve_grid(board):
    global counter
    #Find next empty cell
    for i in range(81):
        if counter > 1:
            return False
        row = i//9
        col = i%9
        if board[row][col] == 0:
            for value in range(1, 10):
                #Check that this value has not already be used on this row
                if not value in board[row]:
                    #Check that this value has not already be used on this column
                    if not value in (board[0][col], board[1][col], board[2][col], board[3][col], board[4][col], board[5][col], board[6][col], board[7][col], board[8][col]):
                        #Identify which of the 9 squares we are working on
                        square = []
                        if row < 3:
                            if col < 3:
                                square = [board[i][0:3] for i in range(0, 3)]
                            elif col < 6:
                                square = [board[i][3:6] for i in range(0, 3)]
                            else:
                                square = [board[i][6:9] for i in range(0, 3)]
                        elif row < 6:
                            if col < 3:
                                square = [board[i][0:3] for i in range(3, 6)]
                            elif col < 6:
                                square = [board[i][3:6] for i in range(3, 6)]
                            else:
                                square = [board[i][6:9] for i in range(3, 6)]
                        else:
                            if col < 3:
                                square = [board[i][0:3] for i in range(6, 9)]
                            elif col < 6:
                                square = [board[i][3:6] for i in range(6, 9)]
                            else:
                                square = [board[i][6:9] for i in range(6, 9)]
                        #Check that this value has not already be used on this 3x3 square
                        if not value in (square[0] + square[1] + square[2]):
                            board[row][col] = value
                            if check(board):
                                counter+=1
                                break
                            else:
                                if solve_grid(board):
                                    return True
            break
    board[row][col] = 0


#randomly decides the order in which cells will be erased to create a new puzzle
def random_order():
    order = []
    for i in range(9):
        for j in range(i, 9):
            if i != j or i < 5:
                order.append((i, j))
    shuffle(order)
    return order

def check(board):
    #check that each row and column has 1 through 9
    for i in range(9):
        row_freq_array = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        col_freq_array = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for j in range(9):
            row_freq_array[board[i][j]] += 1
            col_freq_array[board[j][i]] += 1
        for freq in range(1,10):
            if row_freq_array[freq] == 0:
                return False
        for freq in range(1,10):
            if col_freq_array[freq] == 0:
                return False

    #check that each box has 1 through 9
    for x in range(3):
        for y in range(3):
            box_freq_array = [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            for i in range(3 * x, 3 * x + 3):
                for j in range(3 * y, 3* y + 3):
                    box_freq_array[board[i][j]] += 1
            for freq in range(1,10):
                if box_freq_array[freq] == 0:
                    return False
    return True

def check_duplicate(board):
    #check that each row and column has 1 through 9
    for i in range(9):
        row_freq_array = [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        col_freq_array = [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for j in range(9):
            row_freq_array[board[i][j]] += 1
            col_freq_array[board[j][i]] += 1
        for freq in range(1,10):
            if row_freq_array[freq] > 1:
                return True
        for freq in range(1,10):
            if col_freq_array[freq] > 1:
                return True

    #check that each box has 1 through 9
    for x in range(3):
        for y in range(3):
            box_freq_array = [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            for i in range(3 * x, 3 * x + 3):
                for j in range(3 * y, 3* y + 3):
                    box_freq_array[board[i][j]] += 1
            for freq in range(1,10):
                if box_freq_array[freq] > 1:
                    return True
    return False


#called by check button in gui
def check_gui(board, top_label):
    if check(board):
        top_label.config(text="Solved")
    else:
        top_label.config(text="Not solved")

#makes created clues immutable once puzzle creation mode is exited in gui
def finalize_new_puzzle(board, grid):
    for i in range(9):
        for j in range(9):
            if board[i][j] > 0:
                grid[i][j].label.configure(text=str(board[i][j]), fg = 'black')
                grid[i][j].mutable = False
            else:
                grid[i][j].label.configure(text="")

#called by easy button
def easy(board, grid, game, top_label, bottom_label, saved_boards):
    saved_boards.clear()
    game.version = 0
    game.difficulty = "Easy"
    if game.current != None:
        game.current.label.config(bg="white")
    game.current = None
    top_label.config(text="")
    bottom_label.config(text="Puzzle Difficulty: " + game.difficulty)
    global counter
    new_puzzle(30, board, grid)
    finalize_new_puzzle(board, grid)
    saved_boards.append(copy.deepcopy(board))

#called by medium button
def medium(board, grid, game, top_label, bottom_label, saved_boards):
    saved_boards.clear()
    game.version = 0
    game.difficulty = "Medium"
    if game.current != None:
        game.current.label.config(bg="white")
    game.current = None
    top_label.config(text="")
    bottom_label.config(text="Puzzle Difficulty: " + game.difficulty)
    global counter
    new_puzzle(40, board, grid)
    finalize_new_puzzle(board, grid)
    saved_boards.append(copy.deepcopy(board))

#called by hard button
def hard(board, grid, game, top_label, bottom_label, saved_boards):
    saved_boards.clear()
    game.version = 0
    game.difficulty = "Hard"
    if game.current != None:
        game.current.label.config(bg="white")
    game.current = None
    top_label.config(text="")
    bottom_label.config(text="Puzzle Difficulty: " + game.difficulty)
    global counter
    new_puzzle(50, board, grid)
    finalize_new_puzzle(board, grid)
    saved_boards.append(copy.deepcopy(board))

#called by custom button
def custom(root, board, grid, game, top_label, bottom_label, board_backup, saved_boards):
    saved_boards.clear()
    game.version = 0
    if game.current != None:
        game.current.label.config(bg="white")
    game.current = None
    top_label.config(text="")
    bottom_label.config(text="Creating Custom Puzzle")
    edit_menu = Menu(root)
    root.config(menu=edit_menu)
    edit_menu.add_command(label="Back", command=lambda: back(root, board, grid, game, top_label, bottom_label, saved_boards))
    edit_menu.add_command(label="Finish", command=lambda: finish(root, board, grid, game, top_label, bottom_label, saved_boards))
    edit_menu.add_command(label="Clear", command=lambda: clear(board, grid, top_label, saved_boards, game))
    edit_menu.add_command(label="Undo", command=lambda: undo(saved_boards, board, grid, top_label))
    edit_menu.add_command(label="Redo", command=lambda: redo(saved_boards, board, grid, top_label))

    for i in range(9):
        for j in range(9):
            if grid[i][j].mutable:
                board[i][j] = 0
    for i in range(9):
        for j in range(9):
            board_backup[i][j] = board[i][j]
    for i in range(9):
        for j in range(9):
            board[i][j] = 0
            grid[i][j].label.config(text="", fg="black")
            grid[i][j].mutable = True

    saved_boards.append(copy.deepcopy(board))

#activated in puzzle creation mode to revert back to previous puzzle and main menu
def back(root, board, grid, game, top_label, bottom_label, saved_boards):
    saved_boards.clear()
    game.version = 0
    if game.current != None:
        game.current.label.config(bg="white")
    game.current = None
    top_label.config(text="Reverted to previous puzzle")
    bottom_label.config(text="Puzzle Difficulty: " + game.difficulty)
    for i in range(9):
        for j in range(9):
            board[i][j] = board_backup[i][j]
            if board[i][j] != 0:
                grid[i][j].label.config(text=str(board[i][j]))
                grid[i][j].mutable = False
            else:
                grid[i][j].label.config(text="", fg="red")

    saved_boards.append(copy.deepcopy(board))

    #redisplay main menu
    create_main_menu(root, board, grid, top_label, bottom_label, game, board_backup, saved_boards)

#called by finish button in edit menu. Saves created puzzle and exits edit mode if the puzzle is solvable.
#otherwise, prints out in gui window that the puzzle cannot be solved.
def finish(root, board, grid, game, top_label, bottom_label, saved_boards):
    global counter
    if solvable(board, top_label, bottom_label):
        game.difficulty = "Custom"
        bottom_label.config(text="Puzzle Difficulty: " + game.difficulty)
        top_label.config(text="")
        for i in range(9):
            for j in range(9):
                if board[i][j] > 0:
                    grid[i][j].mutable = False
                else:
                    grid[i][j].label.config(fg='red')
        game.version = 0
        if game.current != None:
            game.current.label.config(bg="white")
        game.current = None
        saved_boards.clear()
        saved_boards.append(copy.deepcopy(board))

        create_main_menu(root, board, grid, top_label, bottom_label,game, board_backup, saved_boards)

def decrease_counter():
    global counter
    counter = 0

#checks if a given puzzle can be solved. does not edit final puzzle
def solvable(board, top_label, bottom_label):
    if check_duplicate(board):
        top_label.config(text="That puzzle is not solvable")
        return False
    global counter
    solve_grid(board)
    if counter == 1:
        decrease_counter()
        return True
    top_label.config(text="That puzzle is not solvable")
    decrease_counter()
    return False


def create_main_menu(root, board, grid, top_label, bottom_label,game, board_backup, saved_boards):
    menu = Menu(root)
    root.config(menu=menu)

    menu.add_command(label="Solve", command=lambda: solve(board, grid, top_label, saved_boards, game))
    menu.add_command(label="Check", command=lambda: check_gui(board, top_label))
    menu.add_command(label="Clear", command=lambda: clear(board, grid, top_label, saved_boards, game))
    menu.add_command(label="Undo", command=lambda: undo(saved_boards, board, grid, top_label))
    menu.add_command(label="Redo", command=lambda: redo(saved_boards, board, grid, top_label))

    new_menu = Menu(menu, tearoff=0)
    menu.add_cascade(label="New...", menu=new_menu)
    new_menu.add_command(label="Easy", command=lambda: easy(board, grid, game, top_label, bottom_label, saved_boards))
    new_menu.add_command(label="Medium", command=lambda: medium(board, grid, game, top_label, bottom_label, saved_boards))
    new_menu.add_command(label="Hard", command=lambda: hard(board, grid, game, top_label, bottom_label, saved_boards))
    new_menu.add_command(label="Custom", command=lambda: custom(root, board, grid, game, top_label, bottom_label, board_backup, saved_boards))

def undo(saved_boards, board, grid, top_label):
    if game.version == 0:
        top_label.config(text="No action to undo")
    else:
        top_label.config(text="Action undone")
        game.version -= 1
        revert_board(saved_boards, board, grid)

def redo(saved_boards, board, grid, top_label):
    if game.version >= len(saved_boards)-1:
        top_label.config(text="No action to redo")
    else:
        top_label.config(text="Action redone")
        game.version += 1
        revert_board(saved_boards, board, grid)

def revert_board(saved_boards, board, grid):
    for i in range(9):
        for j in range(9):
            board[i][j] = saved_boards[game.version][i][j]
            if board[i][j] == 0:
                grid[i][j].label.config(text="")
            else:
                grid[i][j].label.config(text=str(board[i][j]))

def update(board, saved_boards, game):
    if not saved_boards or board != saved_boards[game.version]:
        del saved_boards[game.version+1:]
        saved_boards.append(copy.deepcopy(board))
        game.version += 1

def one(board, saved_boards, game):
    if game.current != None:
        game.current.label.configure(text="1")
        board[game.current.row][game.current.column] = 1
        update(board, saved_boards, game)

def two(board, saved_boards, game):
    if game.current != None:
        game.current.label.configure(text="2")
        board[game.current.row][game.current.column] = 2
        update(board, saved_boards, game)

def three(board, saved_boards, game):
    if game.current != None:
        game.current.label.configure(text="3")
        board[game.current.row][game.current.column] = 3
        update(board, saved_boards, game)

def four(board, saved_boards, game):
    if game.current != None:
        game.current.label.configure(text="4")
        board[game.current.row][game.current.column] = 4
        update(board, saved_boards, game)

def five(board, saved_boards, game):
    if game.current != None:
        game.current.label.configure(text="5")
        board[game.current.row][game.current.column] = 5
        update(board, saved_boards, game)

def six(board, saved_boards, game):
    if game.current != None:
        game.current.label.configure(text="6")
        board[game.current.row][game.current.column] = 6
        update(board, saved_boards, game)

def seven(board, saved_boards, game):
    if game.current != None:
        game.current.label.configure(text="7")
        board[game.current.row][game.current.column] = 7
        update(board, saved_boards, game)

def eight(board, saved_boards, game):
    if game.current != None:
        game.current.label.configure(text="8")
        board[game.current.row][game.current.column] = 8
        update(board, saved_boards, game)

def nine(board, saved_boards, game):
    if game.current != None:
        game.current.label.configure(text="9")
        board[game.current.row][game.current.column] = 9
        update(board, saved_boards, game)

def delete(board, saved_boards, game):
    if game.current != None:
        game.current.label.configure(text="")
        board[game.current.row][game.current.column] = 0
        update(board, saved_boards, game)



#creating gui window
root = Tk()
root.title("Sudoku Companion")


outer_frame = Frame(root, bg="lightblue")
outer_frame.pack()

#add a nice space on left side of puzzle
left_label = Label(outer_frame, text="", bg="lightblue")
left_label.grid(row=1, column=0)

right_label = Label(outer_frame, text="", bg="lightblue")
right_label.grid(row=1, column=2)


#creating sudoku frame
frame = Frame(outer_frame, highlightbackground='black', highlightthickness=2)
frame.grid(row=1, column=1)
num = 1

#creating 3x3 array of boxes (9x9 cells) for sudoku puzzle.
boxes = []
for i in range(3):
    box_row = []
    for j in range(3):
        box = Frame(frame, highlightbackground='black', highlightthickness=1)
        box.grid(row=i, column=j)
        box_row.append(box)
    boxes.append(box_row)
board = [] #for 2D array
board_backup = []
grid = [] #for gui. translates input to the 2D array (board) for algorithms
game = State()
saved_boards = []
for i in range(9):
    board_row = []
    board_backup_row = []
    grid_row = []
    for j in range(9):
        #create 9x9 array of cells
        grid_row.append(Cell(i, j, board, boxes, game, saved_boards))
        #create backup puzzle for later
        board_row.append(0)
        board_backup_row.append(0)
    board.append(board_row)
    board_backup.append(board_backup_row)
    grid.append(grid_row)

#create top label. This will be the main output label
top_label = Label(outer_frame, bg="lightblue", font=('Sans','15','bold'))
top_label.grid(row=0, column=1)

#label1 is the bottom label. It displays puzzle difficulty. By default it displays easy
difficulty = ["Easy"]
bottom_label = Label(outer_frame, bg="lightblue", font=('Sans','15','bold'))
bottom_label.grid(row=2, column=1)
#creates easy puzzle in gui by default. Same function that is called by the easy button in the gui
easy(board, grid, game, top_label, bottom_label, saved_boards)
#establish welcoming statement here since easy function would have erased it if initialized above
top_label.config(text="Welcome to Sudoku Companion!")


#creating main menu
create_main_menu(root, board, grid, top_label, bottom_label, game, board_backup, saved_boards)

#bind 1-9 and backspace to updated selected square
root.bind('1', lambda event: one(board, saved_boards, game))
root.bind('2', lambda event: two(board, saved_boards, game))
root.bind('3', lambda event: three(board, saved_boards, game))
root.bind('4', lambda event: four(board, saved_boards, game))
root.bind('5', lambda event: five(board, saved_boards, game))
root.bind('6', lambda event: six(board, saved_boards, game))
root.bind('7', lambda event: seven(board, saved_boards, game))
root.bind('8', lambda event: eight(board, saved_boards, game))
root.bind('9', lambda event: nine(board, saved_boards, game))
root.bind('<BackSpace>', lambda event: delete(board, saved_boards, game))


#continuously display window until red x is hit at top right
root.mainloop()
