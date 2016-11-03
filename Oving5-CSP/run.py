__author__ = 'nsthtz'
import time
import assignment5 as code

def color():
    start_time = time.time()
    csp = code.create_map_coloring_csp()
    assignment = csp.backtracking_search()
    print("\nTimes iterated: " + str(csp.iterationCounter) + " and times failed: " + str(csp.failureCounter))
    print("Code ran in %s seconds" % (time.time() - start_time))
    print assignment

def sudoku(filename):
    start_time = time.time()
    csp = code.create_sudoku_csp(filename)
    print "Sudoku Board " + filename + "\n"
    code.print_sudoku_solution(csp.backtracking_search())
    print("\nTimes iterated: " + str(csp.iterationCounter) + " and times failed: " + str(csp.failureCounter))
    print("Code ran in %s seconds" % (time.time() - start_time))

sudoku("easy.txt")
sudoku("medium.txt")
sudoku("hard.txt")
sudoku("veryhard.txt")

