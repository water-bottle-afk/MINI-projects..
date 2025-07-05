import heapq # for priority queue

def manhatten(pix=None, x=None,y=None,steps=None):
    #returns manhatted distance from end.
    if pix is not None:
        return abs(end.x-pix.x)+abs(end.y-pix.y)+pix.steps
    return abs(end.x-x)+abs(end.y-y)+steps

class Pixel:
    def __init__(self, x, y, steps=0):
        self.x = x
        self.y = y
        self.steps = steps  # g(n)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))  # allows using in sets

    # def is_closer(self, other):
    #     if manhatten(self.x, self.y, self.steps) < manhatten(other):
    #         return True
    #     return False

    def __lt__(self, other):
        return manhatten(x = self.x, y = self.y, steps= self.steps) < manhatten(other)

class Frontier:
    def __init__(self):
        self.heap = []
        self.seen = set()

    def add(self, pixel):
        if (pixel.x, pixel.y) in self.seen:
            return
        heapq.heappush(self.heap, pixel)
        self.seen.add((pixel.x, pixel.y))

    def remove(self):
        if self.is_empty():
            raise Exception("empty")
        return heapq.heappop(self.heap) # uses operater <

    def is_empty(self):
        return len(self.heap) == 0


    def append_from_enviroment(self, pix):
        lst_of_valid_pixels = [Pixel(pix.x+direction[0],pix.y+direction[1], pix.steps+1) for direction in directions]
        for px in lst_of_valid_pixels:
            try:
                if maze.getpixel((px.x,px.y)) != border:
                    self.add(px)
            except Exception as e:
                pass

    def print(self):
        print(self.heap)

from PIL import Image
#using kinda version on greedy best search
maze = Image.open("maze.png")

directions = (0, 1), (0, -1), (1, 0), (-1, 0)
path_color = (255,) *4
border = (0,0,0,255)
red = (255,0,0,255)
yellow = (255,255,0,255)

width, height = maze.size
start = Pixel(width - 2, 0,0)
end = Pixel(1, height - 1,0)

maze.putpixel((end.x, end.y), yellow)
maze.putpixel((start.x, start.y), yellow)

# for i,j in zip(range(height), range(width)):
#     maze.putpixel((0, i), red)
#     maze.putpixel((j, 0), red)

frontier = Frontier()
frontier.add(end)
i = 1
try:

    while True:
        rmv = frontier.remove()
        frontier.append_from_enviroment(rmv)
        maze.putpixel((rmv.x, rmv.y),yellow)
        print(f"add pixel: ({rmv.x}, {rmv.y})") # logs
        if rmv == start:
            print("found")
            break
        i+=1
        if i % 10000 == 0: # logs
            maze.save(f"try_Y{i//10000}.png")
            print("got to",i)

    frontier.print()
except KeyboardInterrupt: # stop while working
    pass
finally:
    maze.save("solutionY.png")
    frontier.print()

