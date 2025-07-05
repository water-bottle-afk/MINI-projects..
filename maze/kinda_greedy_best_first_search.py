def manhatten(tpl):
    #returns manhatted distance from end.
    return abs(end[0]-tpl[0])+abs(end[1]-tpl[1])

class Frontier:
    def __init__(self):
        self.forntier = []
        self.seen = []

    def add(self, pixel):
        if pixel in self.seen:
        if (not self.is_empty() and manhatten(self.forntier[0]) > manhatten(pixel)) or self.is_empty():
            self.forntier.append(pixel)
            self.seen.append(pixel)

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

from PIL import Image
#using kinda version on greedy best search
maze = Image.open("maze.png")

directions = (0, 1), (0, -1), (1, 0), (-1, 0)
path_color = (255,) *4
border = (0,0,0,255)
red = (255,0,0,255)
width, height = maze.size
start = (width - 2, 0)
end = (1, height - 1)

maze.putpixel(end, red)
maze.putpixel(start, red)

for i,j in zip(range(height), range(width)):
    maze.putpixel((0, i), red)
    maze.putpixel((j, 0), red)

frontier = Frontier()
frontier.add(end)
i = 1
try:

    while True:
        rmv = frontier.remove()
        frontier.append_from_enviroment(rmv)
        maze.putpixel(rmv,red)
        print("add pixel:" , rmv) # logs
        if rmv == start:
            print("found")
            break
        i+=1
        if i % 10000 == 0: # logs
            maze.save(f"try{i//10000}.png")
            print("got to",i)

    frontier.print()
except KeyboardInterrupt: # stop while working
    pass
finally:
    maze.save("solution.png")
    frontier.print()
