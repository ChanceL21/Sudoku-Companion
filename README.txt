This is an all-encompassing Sudoku Companion program. It is written in Python using the Tkinter module.

The functions of this program include:
  -Creating randomized new puzzles of easy, medium, and hard difficulty
  -Allowing users to input their own sudoku puzzles
  -Checking if a current puzzle is in a solved state
  -Solving the puzzle, whether it is randomly generated or input by user
  -Clearing input numbers for convenience

Once the program is launched, it greets the user and by default loads an easy puzzle.
In sudoku there are two kinds of number in a cell: clues (in black) that cannot be changed,
and guesses by the user (empty or in red). The radio buttons on the right of the screen
indicate which number (1 through 9) is currently selected. Left clicking a cell will
fill it with that number, and will overwrite it if it is already filled. Right clicking
a cell will erase the value. In the main state of the program, clues (in black) will not
be altered by either left clicks or right clicks to avoid user mistakes. Pressing the Clear
button will erase all non-clues (in red) on the Sudoku grid. Pressing the Solve button
will solve the puzzle by filling in the empty spaces with the correct numbers (in red).
Pressing the Check button will tell the user whether the puzzle is in a solved state
(black + red numbers) so the user can check their work if they solve the puzzle manually for fun.

Pressing the New... button allows the generation of a easy, medium, hard, or custom puzzle.
Difficulty is determined by the number of clues given.
When a custom puzzle is chosen, the entire grid is erased and the user can now place clues (in black)
instead of guesses (in red). These values can be changed with left click and right click as if they were guesses,
and the clear function clears the whole grid. Finish can be pressed when the puzzle is complete, but
the program will reject this if the puzzle is not solvable. If it is solvable, it returns to the main user and
acts as if a randomly generated puzzle was created. The Go Back button takes the user to their previous puzzle
in case they cannot create a custom one so they are not locked in the edit menu.

Have fun!
