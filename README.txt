This is an all-encompassing Sudoku Companion program. It is written in Python using the Tkinter module.

The functions of this program include:
  -Randomized generation of rotationally symmetrical puzzles of easy, medium, and hard difficulty
  -Solving the puzzle
  -Checking if a current puzzle is in a solved state
  -Clearing input numbers for convenience
  -Undo/Redo options
  -A Puzzle creation mode for the user to input a custom puzzle and interact with using above functions

Once the program is launched, it greets the user and by default loads an easy puzzle.
In sudoku there are two kinds of numbers in a cell: clues (in black) that cannot be changed,
and guesses by the user (empty or in red). The user can left click a cell to highlight it and select it.
Once selected, a red guess can be filled in by typing any number between 1-9 in the keyboard. Typing a new
number will override the original. The number can also be deleted by hitting backspace. In the main state
of the program, clues (in black) cannot be selected or altered. Pressing the Clear button will erase all
non-clues (in red) on the Sudoku grid. Pressing the Solve button will solve the puzzle by filling in the
empty spaces with the correct numbers (in red). Pressing the Check button will tell the user whether the
puzzle is in a solved state (black + red numbers) so the user can check their work if they solve the puzzle
manually for fun.

Pressing the New... button allows the generation of a easy, medium, hard, or custom puzzle.
Difficulty is determined by the number of clues given.
When a custom puzzle is chosen, the entire grid is erased and the user can now place clues (in black)
instead of guesses (in red). These values can be changed with left click and keyboard input as if they were
guesses, and the Clear function now clears the whole grid. Finish can be pressed when the puzzle is complete,
but the program will reject this if the puzzle is not solvable. If it is solvable, it returns to the main user and
acts as if a randomly generated puzzle was created. The Go Back button takes the user to their previous puzzle
in case they cannot create a custom one so they are not locked in the edit menu.

Have fun!
