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
        self.tag = '' # For imaging purposes (path)

    def __repr__(self): # For easy reprinting of the matrix
        return self.type


class buildWorld():
    """
    This class imports the text-file, represents it as a matrix and converts each element to a node-object.
    """

    def __init__(self, path):
        f = open(path, 'r')
        self.w = [list(line.rstrip()) for line in f]
        self.convert()

    def convert(self): # Basic conversion to Nodes, with only their type and position-values set
        for y in range(len(self.w)):
            for x, val in enumerate(self.w[y]):
                self.w[y][x] = Node((x,y), val)
                if val == 'A':
                    self.start = self.w[y][x]
                if val == 'B':
                    self.goal = self.w[y][x]

    def getWorld(self): # Allows easy access to the matrix (w), start and goal nodes.
        return self.w, self.start, self.goal

class Algorithm():
    """
    The Astar Algorithm is implemented in the initialization, as it is supposed to just run all the way through immediately.
    There probably exists a way of doing it with less redundancy.
    """

    def __init__(self, world, start, goal): # Mostly same as previous assignment, will comment alterations
        """
        :param world: The matrix.
        :param start: Points to the start node object.
        :param goal: Points to the end node object.
        :return: None, is implemented with its own printing-method for this exercise.
        """
        self.costs = {'w': 100, 'm': 50, 'f': 10, 'g': 5, 'r': 1, 'A': 0, 'B': 0}
        self.world = world
        self.start = start
        self.goal = goal
        self.open = []
        self.closed = []
        self.tag = ''

        start.g = 0
        start.h = self.h(start)
        start.f = start.g+start.h
        self.open = [start]

        self.run()
        node = self.goal.parent
        while node != self.start:
            node.tag = 'path'
            node = node.parent


    def run(self):
        """
        Runs the A* algorithm, adopted more or less line by line from the pseudocode in the supplement.
        Only changes from previous version are commented.
        """
        while True:
            if len(self.open) == 0:
                return False
            node = self.open.pop()
            self.closed.append(node)
            if node.pos == self.goal.pos:
                return 1
            self.getChildren(node)
            for child in node.children:
                if not child in self.open and not child in self.closed:
                    self.evaluate(child, node)
                    self.open.append(child)
                    self.open.sort(key=lambda node: node.f, reverse=True)
                elif node.g + self.costs[child.type] < child.g: # Needs to take the cost (h(node)) of the node into consideration
                    self.evaluate(child, node)
                    if child in self.closed:
                        self.propagate(child)


    def evaluate(self, child, node): # attach and evaluate
        child.parent = node
        child.g = node.g + self.costs[child.type] # Looks up the cost of the type in a dictionary
        child.f = child.g + self.h(child)

    def propagate(self, node): # Propagates changes to parent
        for child in node.children:
            if node.g < child.g:
                child.parent = node
                child.g = node.g + self.costs[child.type] # Looks up the cost of the type in a dictionary
                child.f = child.g + self.h(child)

    def h(self, node): # Estimate using straight line to goal
        h = math.sqrt((node.pos[0] - self.goal.pos[0])**2 + (node.pos[1] - self.goal.pos[1])**2)
        return h

    def getChildren(self, node):
        """
        Generates and appends children if valid position. Uses the boundaries of the matrix as limit.
        Alternatively this could all be done during world building, but would then "initialize" nodes that are never touched.
        """
        posX = node.pos[0]
        posY = node.pos[1]
        if (posY - 1) >= 0:
            upNode = self.world[posY -1][posX]
            node.children.append(upNode)
        if (posY + 1) < len(self.world):
            downNode = self.world[posY + 1][posX]
            node.children.append(downNode)
        if (posX - 1) >= 0:
            leftNode = self.world[posY][posX - 1]
            node.children.append(leftNode)
        if (posX + 1) < len(self.world[posY]):
            rightNode = self.world[posY][posX + 1]
            node.children.append(rightNode)

    def getParams(self): # Returns matrix
        return self.world

world, start, goal = buildWorld(os.path.dirname(os.path.abspath(__file__))+r'\boards\board-2-4.txt').getWorld()
gui = image.gui(Algorithm(world, start, goal).getParams(), len(world[0]), len(world))
map = gui.send_it()
map.show()