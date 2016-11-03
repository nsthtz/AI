__author__ = 'nsthtz'
from PIL import Image, ImageDraw

class gui:
    """
    This class creates an image-object by reading node types and tags.
    """
    def __init__(self, matrix, x, y):
        self.matrix = matrix
        self.len_x = x  # lengde til brettet
        self.len_y = y  # hoyde til brettet

        self.colors = {
            ".": "#bfbfbf",
            "#": "#4c4c4c",
            "A": "#79d279",
            "B": "#b20000",
            "w": "#6666ff",
            "m": "#666666",
            "f": "#006600",
            "g": "#329932",
            "r": "#ff9933"
        }
        self.sq_size = 30

        self.img = Image.new("RGB", size=(self.sq_size * self.len_x, self.sq_size * self.len_y))
        self.draw = ImageDraw.Draw(self.img)

        for x in range(0, self.len_x):
            for y in range(0, self.len_y):
                node = matrix[y][x]
                self.draw.rectangle(
                    [(x * self.sq_size, y * self.sq_size), ((x + 1) * self.sq_size, (y + 1) * self.sq_size)],
                    self.colors[node.type], "#000000")
                if node.type == "A":
                    self.draw.text(((2 * x + 1) / 2 * self.sq_size, (2 * y + 1) / 2 * self.sq_size), "A", "#000000")
                elif node.type == "B":
                    self.draw.text(((2 * x + 1) / 2 * self.sq_size, (2 * y + 1) / 2 * self.sq_size), "B", "#000000")
                elif node.tag == "path":
                    self.draw.text(((2 * x + 1) / 2 * self.sq_size, (2 * y + 1) / 2 * self.sq_size), "O", "#000000")
                elif node.tag == "open":
                    self.draw.text(((2 * x + 1) / 2 * self.sq_size, (2 * y + 1) / 2 * self.sq_size), "*", "#000000")
                elif node.tag == "closed":
                    self.draw.text(((2 * x + 1) / 2 * self.sq_size, (2 * y + 1) / 2 * self.sq_size), "X", "#000000")

    def send_it(self):
        return self.img
