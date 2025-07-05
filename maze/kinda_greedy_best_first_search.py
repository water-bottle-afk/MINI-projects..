# main 
from PIL import Image
maze = Image.open("maze.png")
links = {}
directions = (0, 1), (0, -1), (1, 0), (-1, 0)
path_color = (255,) *4
border = (0,0,0,255)
red = (255,0,0,255)
width, height = maze.size
start = (width - 2, 0)
end = (1, height - 1)

def manhatten(tpl):
    """
    :param x:
    :param y:
    :return:
    returns manhatted distance from end.
    """
    return abs(end[0]-tpl[0])+abs(end[1]-tpl[1])

class Frontier:
    def __init__(self):
        self.forntier = []
        self.seen = []

    def add(self, pixel):
        if pixel in self.seen:
            return False
        # if pixel not in self.seen and not self.is_empty():
        #     if manhatten(pixel) <= manhatten(self.forntier[-1]):
        #         self.seen.append(pixel)
        #         self.forntier.append(pixel)
        #         return True
        # if self.is_empty():
        if (not self.is_empty() and manhatten(self.forntier[0]) > manhatten(pixel)) or self.is_empty():
            self.forntier.append(pixel)
            self.seen.append(pixel)
            return True
        # return False

    def remove(self):
        if self.is_empty():
            x = self.seen.pop(-1)
            self.seen = [x] + self.seen
            return x
        pixel = self.forntier[-1]
        self.forntier = self.forntier[:-1]
        return pixel

    def is_empty(self):
        return len(self.forntier) == 0


    def append_from_enviroment(self, pixel):
        lst_of_valid_pixels = [(pixel[0]+direction[0],pixel[1]+direction[1]) for direction in directions]
        for pix in lst_of_valid_pixels:
            try:
                if maze.getpixel(pix) != border:
                    self.add(pix)
            except Exception as e:
                pass

    def print(self):
        print(self.forntier)
