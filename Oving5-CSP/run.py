__author__ = 'nsthtz'
import time
import assignment5 as code

def color():
    csp = code.create_map_coloring_csp()
    assignment = csp.backtracking_search()
    print assignment

def sudoku(filename):
    csp = code.create_sudoku_csp(filename)
    code.print_sudoku_solution(csp.backtracking_search())

# color()
start_time = time.time()
sudoku("easy.txt")
print "\n"
sudoku("medium.txt")
print "\n"
sudoku("hard.txt")
print "\n"
sudoku("veryhard.txt")
print("--- %s seconds ---" % (time.time() - start_time))