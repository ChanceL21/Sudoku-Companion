from tkinter import *
import tkinter.ttk
import copy
from random import randint, shuffle

counter = 0

class Cell:

    """ Cell object that contains a sudoku square. a 9x9 array of these objects will be made for program """

    def __init__(self, master, row, column, board, boxes):
        #create button that is put into specific box of sudoku frame
        self.button = Button(boxes[row//3][column//3], text="", fg="red", width = 4, height = 2, font=20)
        #bind button functions
        self.button.bind("<Button-1>", self.left_click)
        self.button.bind("<Button-3>", self.right_click)
        #put button in specific location of box frame
        self.button.grid(row=row%3, column=column%3)
        self.row = row
        self.column = column
        self.board = board
        self.num = 1
        #not a clue
        self.mutable = True

    # make current number appear when left click is hit if the cell is not a clue. also Modifies 2D array
    def left_click(self, event):
        if self.mutable:
            self.button.configure(text=str(self.num))
            self.board[self.row][self.column] = self.num

    #make current number disappear when right click is hit if the cell is not a clue. Also modifies 2D array
    def right_click(self, event):
        if self.mutable:
            self.button.configure(text="")
            self.board[self.row][self.column] = 0

#activated by radiobutton 1
def one():
    for row in grid:
        for cell in row:
            cell.num = 1

#activated by radiobutton 2
def two():
    for row in grid:
        for cell in row:
            cell.num = 2

#etc
def three():
    for row in grid:
        for cell in row:
            cell.num = 3

def four():
    for row in grid:
        for cell in row:
            cell.num = 4

def five():
    for row in grid:
        for cell in row:
            cell.num = 5

def six():
    for row in grid:
        for cell in row:
            cell.num = 6

def seven():
    for row in grid:
        for cell in row:
            cell.num = 7

def eight():
    for row in grid:
        for cell in row:
            cell.num = 8

def nine():
    for row in grid:
        for cell in row:
            cell.num = 9

#solves the 2D array and the gui grid and prints out relative statement in gui window
def solve():
    if check(board):
        label2.config(text="This puzzle has already been solved")
    else:
        for i in range(9):
            for j in range(9):
                if grid[i][j].mutable:
                    board[i][j] = 0
        solveGrid(board)
        if counter == 1:
            label2.config(text="The puzzle has now been solved")
            filled = 0
            while filled == 0:
                fillGrid()
                filled = 1
                for row in board:
                    if 0 in row:
                        filled = 0
        else:
            label2.config(text="The puzzle is not solvable")
    if counter == 1:
        decrease_counter()

    for i in range(9):
        for j in range(9):
            if grid[i][j].mutable:
                grid[i][j].button.config(text=str(board[i][j]))

def clear():
    label2.config(text="Cleared")
    for i in range(9):
        for j in range(9):
            if grid[i][j].mutable:
                grid[i][j].button.configure(text="")
                board[i][j] = 0

#Based on Sudoku Generator Algorithm - www.101computing.net/sudoku-generator-algorithm/
#makes a new, random puzzle. takes in int number of spaces to be removed from a completed puzzle
def new_puzzle(attempts):
    for i in range(9):
        for j in range(9):
            board[i][j] = 0
            grid[i][j].mutable = True
            grid[i][j].button.config(fg="red")
    fillGrid()
    global counter
    order = random_order()
    i = 0
    while attempts > 0 and i < 81:
      row = order[i][0]
      col = order[i][1]

      #Remember its cell value in case we need to put it back
      backup = board[row][col]
      board[row][col]=0

      #Take a full copy of the grid
      copyGrid = []
      for r in range(0,9):
         copyGrid.append([])
         for c in range(0,9):
            copyGrid[r].append(board[r][c])

      #Count the number of solutions that this grid has (using a backtracking approach implemented in the solveGrid() function)
      solveGrid(copyGrid)

      #If the number of solution is different from 1 then we need to cancel the change by putting the value we took away back in the grid
      if counter != 1:
        board[row][col]=backup
        #We could stop here, but we can also have another attempt with a different cell just to try to remove more numbers
      else:
          attempts -= 1
      i += 1
      counter = 0


#A backtracking/recursive function to check all possible combinations of numbers until a solution is found
#Based on Sudoku Generator Algorithm - www.101computing.net/sudoku-generator-algorithm/
def fillGrid():
  numberList=[1,2,3,4,5,6,7,8,9]
  #Find next empty cell
  for i in range(0,81):
    row=i//9
    col=i%9
    if board[row][col]==0:
      shuffle(numberList)
      for value in numberList:
        #Check that this value has not already be used on this row
        if not(value in board[row]):
          #Check that this value has not already be used on this column
          if not value in (board[0][col],board[1][col],board[2][col],board[3][col],board[4][col],board[5][col],board[6][col],board[7][col],board[8][col]):
            #Identify which of the 9 squares we are working on
            square=[]
            if row<3:
              if col<3:
                square=[board[i][0:3] for i in range(0,3)]
              elif col<6:
                square=[board[i][3:6] for i in range(0,3)]
              else:
                square=[board[i][6:9] for i in range(0,3)]
            elif row<6:
              if col<3:
                square=[board[i][0:3] for i in range(3,6)]
              elif col<6:
                square=[board[i][3:6] for i in range(3,6)]
              else:
                square=[board[i][6:9] for i in range(3,6)]
            else:
              if col<3:
                square=[board[i][0:3] for i in range(6,9)]
              elif col<6:
                square=[board[i][3:6] for i in range(6,9)]
              else:
                square=[board[i][6:9] for i in range(6,9)]
            #Check that this value has not already be used on this 3x3 square
            if not value in (square[0] + square[1] + square[2]):
              board[row][col]=value
              if check(board):
                return True
              else:
                if fillGrid():
                  return True
      break
  board[row][col]=0


#A backtracking/recursive function to check all possible combinations of numbers until a solution is found
#Based on Sudoku Generator Algorithm - www.101computing.net/sudoku-generator-algorithm/
def solveGrid(board):
  global counter
  #Find next empty cell
  for i in range(0,81):
    if counter > 1:
      return False
    row=i//9
    col=i%9
    if board[row][col]==0:
      for value in range (1,10):
        #Check that this value has not already be used on this row
        if not(value in board[row]):
          #Check that this value has not already be used on this column
          if not value in (board[0][col],board[1][col],board[2][col],board[3][col],board[4][col],board[5][col],board[6][col],board[7][col],board[8][col]):
            #Identify which of the 9 squares we are working on
            square=[]
            if row<3:
              if col<3:
                square=[board[i][0:3] for i in range(0,3)]
              elif col<6:
                square=[board[i][3:6] for i in range(0,3)]
              else:
                square=[board[i][6:9] for i in range(0,3)]
            elif row<6:
              if col<3:
                square=[board[i][0:3] for i in range(3,6)]
              elif col<6:
                square=[board[i][3:6] for i in range(3,6)]
              else:
                square=[board[i][6:9] for i in range(3,6)]
            else:
              if col<3:
                square=[board[i][0:3] for i in range(6,9)]
              elif col<6:
                square=[board[i][3:6] for i in range(6,9)]
              else:
                square=[board[i][6:9] for i in range(6,9)]
            #Check that this value has not already be used on this 3x3 square
            if not value in (square[0] + square[1] + square[2]):
              board[row][col]=value
              if check(board):
                counter+=1
                break
              else:
                if solveGrid(board):
                  return True
      break
  board[row][col]=0


#randomly decides the order in which cells will be erased to create a new puzzle
def random_order():
    order = []
    for i in range(9):
        for j in range(9):
            order.append((i, j))
    shuffle(order)
    return order

def check(board):
    #check that each row and column has 1 through 9
    for i in range(9):
        row_freq_array = [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        col_freq_array = [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
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

def check_duplicate():
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
def check_gui():
    if check(board):
        label2.config(text="Solved")
    else:
        label2.config(text="Not Solved")

#makes created clues immutable once puzzle creation mode is exited in gui
def finalize_new_puzzle():
    for i in range(9):
        for j in range(9):
            if board[i][j] > 0:
                grid[i][j].button.configure(text=str(board[i][j]), fg = 'black')
                grid[i][j].mutable = False
            else:
                grid[i][j].button.configure(text="")

#called by easy button
def easy():
    difficulty[0] = "Easy"
    label1.config(text="Puzzle Difficulty: " + difficulty[0])
    label2.config(text="")
    global counter
    new_puzzle(30)
    finalize_new_puzzle()

#called by medium button
def medium():
    difficulty[0] = "Medium"
    label1.config(text="Puzzle Difficulty: " + difficulty[0])
    label2.config(text="")
    global counter
    new_puzzle(40)
    finalize_new_puzzle()

#called by hard button
def hard():
    difficulty[0] = "Hard"
    label1.config(text="Puzzle Difficulty: " + difficulty[0])
    label2.config(text="")
    global counter
    new_puzzle(50)
    finalize_new_puzzle()

#called by custom button
def custom():
    label1.config(text="Creating Custom Puzzle")
    label2.config(text="")
    edit_menu = Menu(root)
    root.config(menu=edit_menu)
    edit_menu.add_command(label="Go Back", command=go_back)
    edit_menu.add_command(label="Finish", command=finish)
    edit_menu.add_command(label="Clear", command=clear)

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
            grid[i][j].button.config(text="", fg="black")
            grid[i][j].mutable = True

#activated in puzzle creation mode to revert back to previous puzzle and main menu
def go_back():
    label2.config(text="Reverted to previous puzzle")
    label1.config(text="Puzzle Difficulty: " + difficulty[0])
    for i in range(9):
        for j in range(9):
            board[i][j] = board_backup[i][j]
            if board[i][j] != 0:
                grid[i][j].button.config(text=str(board[i][j]))
                grid[i][j].mutable = False
            else:
                grid[i][j].button.config(text="", fg="red")

    #redisplay main menu
    menu = Menu(root)
    root.config(menu=menu)

    menu.add_command(label="Solve", command=solve)
    menu.add_command(label="Check", command=check_gui)
    menu.add_command(label="Clear", command=clear)

    new_menu = Menu(menu, tearoff=0)
    menu.add_cascade(label="New...", menu=new_menu)
    new_menu.add_command(label="Easy", command=easy)
    new_menu.add_command(label="Medium", command=medium)
    new_menu.add_command(label="Hard", command=hard)
    new_menu.add_command(label="Custom", command=custom)

def decrease_counter():
    global counter
    counter = 0

#checks if a given puzzle can be solved. does not edit final puzzle
def solvable():
    if check_duplicate():
        label2.config(text="That puzzle is not solvable")
        return False
    global counter
    solveGrid(board)
    if counter == 1:
        decrease_counter()
        return True
    label2.config(text="That puzzle is not solvable")
    decrease_counter()
    return False

#called by finish button in edit menu. Saves created puzzle and exits edit mode if the puzzle is solvable.
#otherwise, prints out in gui window that the puzzle cannot be solved.
def finish():
    global counter
    if solvable():
        label1.config(text="Puzzle Difficulty: Custom")
        label2.config(text="Custom puzzle created")
        for i in range(9):
            for j in range(9):
                if board[i][j] > 0:
                    grid[i][j].mutable = False
                else:
                    grid[i][j].button.config(fg='red')

        menu = Menu(root)
        root.config(menu=menu)

        menu.add_command(label="Solve", command=solve)
        menu.add_command(label="Check", command=check_gui)
        menu.add_command(label="Clear", command=clear)

        new_menu = Menu(menu, tearoff=0)
        menu.add_cascade(label="New...", menu=new_menu)
        new_menu.add_command(label="Easy", command=easy)
        new_menu.add_command(label="Medium", command=medium)
        new_menu.add_command(label="Hard", command=hard)
        new_menu.add_command(label="Custom", command=custom)

#creating gui window
root = Tk()
root.title("Sudoku Companion")

#creating main menu
menu = Menu(root)
root.config(menu=menu)

menu.add_command(label="Solve", command=solve)
menu.add_command(label="Check", command=check_gui)
menu.add_command(label="Clear", command=clear)

new_menu = Menu(menu, tearoff=0)
menu.add_cascade(label="New...", menu=new_menu)
new_menu.add_command(label="Easy", command=easy)
new_menu.add_command(label="Medium", command=medium)
new_menu.add_command(label="Hard", command=hard)
new_menu.add_command(label="Custom", command=custom)

#creating sudoku frame
frame = Frame(root, highlightbackground='black', highlightthickness=2)
frame.grid(row=1, column=0)
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
grid = [] #for gui

for i in range(9):
    board_row = []
    board_backup_row = []
    grid_row = []
    for j in range(9):
        #create 9x9 array of cells
        grid_row.append(Cell(frame, i, j, board, boxes))
        #create backup puzzle for later
        board_row.append(0)
        board_backup_row.append(0)
    board.append(board_row)
    board_backup.append(board_backup_row)
    grid.append(grid_row)

v = StringVar()
v.set("1") # initialize

#create frame for radio buttons
radio_frame = Frame(root)
radio_frame.grid(row=1, column=1)

#make radio buttons that appear on right side of gui. Clicking one unclicks the other
#These call a unique function that sets the left click change value to their corresponding number
Radiobutton(radio_frame, command=one, text='1', font=20, variable=v, value='1').grid(row=0)
Label(radio_frame, text="", font=20).grid(row=1)
Radiobutton(radio_frame, command=two, text='2', font=20, variable=v, value='2').grid(row=2)
Label(radio_frame, text="", font=20).grid(row=3)
Radiobutton(radio_frame, command=three, text='3', font=20, variable=v, value='3').grid(row=4)
Label(radio_frame, text="", font=20).grid(row=5)
Radiobutton(radio_frame, command=four, text='4', font=20, variable=v, value='4').grid(row=6)
Label(radio_frame, text="", font=20).grid(row=7)
Radiobutton(radio_frame, command=five, text='5', font=20, variable=v, value='5').grid(row=8)
Label(radio_frame, text="", font=20).grid(row=9)
Radiobutton(radio_frame, command=six, text='6', font=20, variable=v, value='6').grid(row=10)
Label(radio_frame, text="", font=20).grid(row=11)
Radiobutton(radio_frame, command=seven, text='7', font=20, variable=v, value='7').grid(row=12)
Label(radio_frame, text="", font=20).grid(row=13)
Radiobutton(radio_frame, command=eight, text='8', font=20, variable=v, value='8').grid(row=14)
Label(radio_frame, text="", font=20).grid(row=15)
Radiobutton(radio_frame, command=nine, text='9', font=20, variable=v, value='9').grid(row=16)

#create top label. This will be the main output label
label2 = Label(root, text="Welcome to Sudoku Companion!")
label2.grid(row=0, column=0)

#label1 is the bottom label. It displays puzzle difficulty. By default it displays easy
difficulty = ["Easy"]
label1 = Label(root, text="Puzzle Difficulty: " + difficulty[0])
label1.grid(row=2, column=0)
#creates easy puzzle in gui by default. Same function that is called by the easy button in the gui
easy()
#reestablish welcoming statement since easy function erases it
label2.config(text="Welcome to Sudoku Companion!")

#continuously display window until red x is hit at top right
root.mainloop()
