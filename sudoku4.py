import sys
import clingo
from sudoku_board import Sudoku
 
SUDOKU_ENCODING = """
% Generate: assign exactly one number to each cell
{ sudoku(R,C,1..9) } = 1 :- R = 1..9, C = 1..9.
 
% Constraint: respect initial values
:- initial(R,C,V), not sudoku(R,C,V).
 
% Constraint: no duplicate in a row
:- sudoku(R,C1,V), sudoku(R,C2,V), C1 != C2.
 
% Constraint: no duplicate in a column
:- sudoku(R1,C,V), sudoku(R2,C,V), R1 != R2.
 
% Constraint: no duplicate in a 3x3 box
:- sudoku(R1,C1,V), sudoku(R2,C2,V),
   R1 != R2, C1 != C2,
   ((R1-1)/3) == ((R2-1)/3),
   ((C1-1)/3) == ((C2-1)/3).
 
#show sudoku/3.
"""
 
class SudokuApp(clingo.Application):
    def __init__(self):
        self.program_name = "sudoku4"
 
    def print_model(self, model, printer):
        sudoku = Sudoku.from_model(model)
        print(sudoku, end="")
 
    def main(self, ctl, files):
        ctl.add("base", [], SUDOKU_ENCODING)
        for f in files:
            ctl.load(f)
        ctl.ground([("base", [])])
        ctl.solve()
 
clingo.clingo_main(SudokuApp(), sys.argv[1:])