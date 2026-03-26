from typing import Tuple
import clingo


class Sudoku:
    def __init__(self, sudoku: dict[Tuple[int, int], int]):
        self.sudoku = sudoku

    def __str__(self) -> str:
        s = ""
        for row in range(1, 10):
            cells = []
            for col in range(1, 10):
                val = self.sudoku.get((row, col), None)
                cells.append(str(val) if val is not None else "-")
            s += " ".join(cells[0:3]) + "  " + " ".join(cells[3:6]) + "  " + " ".join(cells[6:9]) + "\n"
            if row % 3 == 0:
                s += "\n"
        return s

    @classmethod
    def from_str(cls, s: str) -> "Sudoku":
        sudoku = {}
        # YOUR CODE HERE
        return cls(sudoku)

    @classmethod
    def from_model(cls, model: clingo.solving.Model) -> "Sudoku":
        sudoku = {}
        for atom in model.symbols(shown=True):
            if atom.name == "sudoku" and len(atom.arguments) == 3:
                row = atom.arguments[0].number
                col = atom.arguments[1].number
                val = atom.arguments[2].number
                sudoku[(row, col)] = val
        return cls(sudoku)
