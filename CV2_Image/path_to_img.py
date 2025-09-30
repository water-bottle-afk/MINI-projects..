from PIL import Image

pic_url = r"Donut-icon.png"
img = Image.open(pic_url)

img = img.convert("RGBA")

width, height = img.size  # <-- FIXED
color = ' .;-:!>7?CO$QHNM'

pixel = img.load()
with open("res.txt", "w") as file:
    for h in range(height):
        for w in range(width):
            r, g, b, a = pixel[w, h]
            brightness = (r + g + b) // 3
            idx = brightness * (len(color) - 1) // 255
            file.write(color[idx] + " ")
        file.write('\n')
