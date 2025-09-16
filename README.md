# 🧩 Sudoku Solver in Python

Academic project from an **Introduction to Computer Science** course.  
The program implements a **Sudoku solver**, including board validation, automatic solving steps, and user interaction when multiple options are available.

---

## 📚 Features

- **Board Validation**: checks if a Sudoku board is legal (no duplicates in rows, columns, or 3x3 boxes).
- **Options Calculation**: for each empty cell, calculates all possible digits that can be placed there.
- **Automatic Solving**: fills cells with a single possible digit.
- **User Interaction**: if multiple digits are possible, the program asks the user to choose.
- **Random Board Generation**: creates a Sudoku board with 10–20 random numbers placed legally.
- **Board Printing**: displays the board in a clear format on the console or writes it into a text file.

---

## 🛠️ Implementation Details

- The board is represented as a 9×9 list of lists.  
  - Filled cells contain digits `1–9`.  
  - Empty cells are represented by `-1`.  
- Constants are defined for solver states:  
  - `FINISH_SUCCESS` – board solved successfully.  
  - `FINISH_FAILURE` – board not solvable or contains contradictions.  
  - `NOT_FINISH` – board not yet complete.  
- The solver works in stages:  
  1. Fills cells with only one possible option.  
  2. If needed, asks the user to select a digit for the cell with the fewest options.  
  3. Repeats until success or failure.

---

## 📖 Example Boards

The project demonstrates solving of:
- A fully valid board
- A partially filled board
- An impossible board
- An invalid board (with duplicates)
- A rendomaly geenerated board

---

## 💻 Example Outputs

1. The board is not finished yet  
In the location: (0, 2) The current possibilities are: [1, 2, 4, 8]  
Please choose one number:  

2. "FINISH_SUCCESS" (Board solved successfully!)   

---------------------------
|5 |3 |4 |6 |7 |8 |9 |1 |2 |
---------------------------
|6 |7 |2 |1 |9 |5 |3 |4 |8 |
---------------------------
|1 |9 |8 |3 |4 |2 |5 |6 |7 |
---------------------------
|8 |5 |9 |7 |6 |1 |4 |2 |3 |
---------------------------
|4 |2 |6 |8 |5 |3 |7 |9 |1 |
---------------------------
|7 |1 |3 |9 |2 |4 |8 |5 |6 |
---------------------------
|9 |6 |1 |5 |3 |7 |2 |8 |4 |
---------------------------
|2 |8 |7 |4 |1 |9 |6 |3 |5 |
---------------------------
|3 |4 |5 |2 |8 |6 |1 |7 |9 |
---------------------------

---

## 📂 Files

- `main.py` – contains all the code (solver functions, board generation, printing, and execution).  
- `solved_sudoku.txt` – output file containing the solving results of the boards.  

---

## 🧑‍💻 Skills Demonstrated

*Python programming: functions, lists, loops, conditionals.  
*Problem solving using backtracking and constraint satisfaction.  
*File I/O and formatted printing.  
*User interaction in algorithmic processes.  
*Algorithmic thinking in Sudoku solving and board generation.  

