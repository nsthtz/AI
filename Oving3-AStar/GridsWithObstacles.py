__author__ = 'nsthtz'
import math
import os
import image


class Node():
    """
    Preparing the node class for use in the graph.
    """

    def __init__(self, pos, type):
        """
        :param pos: The node position as a tuple
        :param type: Its type (terrain)
        """
        self.pos = pos
        self.type = type
        self.parent = ''
        self.children = []
        self.tag = ''  # For imaging purposes (path, open, closed)

    def __repr__(self):  # For easy reprinting of the matrix
        return self.type


class buildWorld():
    """
    This class imports the text-file, represents it as a matrix and converts each element to a node-object.
    """

    def __init__(self, path):
        f = open(path, 'r')
        self.w = [list(line.rstrip()) for line in f]
        self.convert()

    def convert(self):  # Basic conversion to Nodes, with only their type and position-values set
        for y in range(len(self.w)):
            for x, val in enumerate(self.w[y]):
                self.w[y][x] = Node((x, y), val)
                if val == 'A':
                    self.start = self.w[y][x]
                if val == 'B':
                    self.goal = self.w[y][x]

    def getWorld(self):  # Allows easy access to the matrix (w), start and goal nodes.
        return self.w, self.start, self.goal


class Algorithm():
    """
    The Astar Algorithm is implemented in the initialization, as it is supposed to just run all the way through immediately.
    There probably exists a way of doing it with less redundancy.
    """

    def __init__(self, world, start, goal, flag):
        """
        :param world: The matrix.
        :param start: Points to the start node object.
        :param goal: Points to the end node object.
        :return: None, is implemented with its own printing-method for this exercise.
        """
        self.world = world
        self.start = start
        self.goal = goal
        self.open = []
        self.closed = []
        self.flag = flag # For selecting algorithm ("A" for A*, "B" for BFS and "D" for Dijkstra)

        start.g = 0  # Sets g(start)
        start.h = self.h(start)  # Sets distance to end
        start.f = start.g + start.h  # Heuristic
        self.open = [start]

        if self.run():  # Actually runs the algorithm, and is used for generating the visual representation of the shortest path if applicable.
            node = self.goal.parent
            while node != self.start:
                node.tag = 'path'
                node = node.parent
        else:
            print("No solution")

    def run(self):
        """
        Runs the desired algorithm, adopted more or less line by line from the pseudocode in the supplement.
        """
        while True:  # Runs until it returns either success or failure. Using an actual clause would probably be better,
            # i.e. stopping when the node position equals the goal node.
            if len(self.open) == 0:  # Exits if there is no more elements in the OPEN list, meaning failure.
                # self.mark()  # Marks open or closed nodes - ONLY USED FOR PROBLEM A.3.2
                return False
            node = self.open.pop(0)  # pop first element in list
            self.closed.append(node)
            if node.pos == self.goal.pos:  # If node is the goal node -> Solution!
                # self.mark() # ONLY USED FOR PROBLEM A.3.2
                return True
            self.getChildren(node)  # Generates children and appends them to the node.children list.
            for child in node.children:
                if not child in self.open and not child in self.closed:  # If the child is new
                    self.evaluate(child, node)  # attach-and-eval
                    self.open.append(child)
                    if self.flag == 'A':  # Astar sorts by node.f
                        self.open.sort(key=lambda node: node.f)
                    if self.flag == 'D':  # Dijkstra sorts by node.g, no sort for BFS
                        self.open.sort(key=lambda node: node.g)
                elif node.g < child.g:  # Shorter path discovered
                    self.evaluate(child, node)  # recalculates heuristics values and reassigns parent
                    if child in self.closed:  # if child has already been processed, relax and propagate the changes
                        self.propagate(child)

    def evaluate(self, child, node):  # attach and evaluate
        child.parent = node
        child.g = node.g
        child.f = child.g + self.h(child)  # uses distance to goal as estimated cost

    def propagate(self, node):  # Propagates changes to parent
        for child in node.children:
            if node.g < child.g:
                child.parent = node
                child.g = node.g
                child.f = child.g + self.h(child)

    def h(self, node):  # Estimate using straight line to goal
        h = math.sqrt((node.pos[0] - self.goal.pos[0]) ** 2 + (node.pos[1] - self.goal.pos[1]) ** 2)
        return h

    def getChildren(self, node):
        """
        Generates and appends children if valid position. Uses the boundaries of the matrix as limit.
        Alternatively this could all be done during world building, but would then "initialize" nodes that are never touched.
        """
        posX = node.pos[0]
        posY = node.pos[1]
        if (posY - 1) >= 0:
            upNode = self.world[posY - 1][posX]
            if self.validPath(upNode):
                node.children.append(upNode)
        if (posY + 1) < len(self.world):
            downNode = self.world[posY + 1][posX]
            if self.validPath(downNode):
                node.children.append(downNode)
        if (posX - 1) >= 0:
            leftNode = self.world[posY][posX - 1]
            if self.validPath(leftNode):
                node.children.append(leftNode)
        if (posX + 1) < len(self.world[posY]):
            rightNode = self.world[posY][posX + 1]
            if self.validPath(rightNode):
                node.children.append(rightNode)

    def validPath(self, node):  # Walls are ignored
        if node.type == '#':
            return False
        return True

    def mark(self):  # Added for Assignment A3 to mark open or closed nodes.
        for node in self.open:  # Marks opened nodes with * in case of failure
            node.tag = "open"
        for node in self.closed:  # Marks closed nodes with x in case of failure
            node.tag = "closed"

    def getParams(self):  # returns matrix
        return self.world


world, start, goal = buildWorld(os.path.dirname(os.path.abspath(__file__)) + r'\boards\board-1-1.txt').getWorld()
gui = image.gui(Algorithm(world, start, goal, "D").getParams(), len(world[0]), len(world))
map = gui.send_it()
map.show()
