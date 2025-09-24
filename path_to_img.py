from PIL import Image

pic_url = r"AAAA.jpeg"
img = Image.open(pic_url)

img = img.convert("RGB")

height, width = img.size
color = ' .;-:!>7?CO$QHNM'

pixel = img.load()
with open("resres.txt","w") as file:
    file.write("")
with open("resres.txt","a") as file:
    for h in range(height):
        for w in range(width):
            try:
                rgb = pixel[w, h]

                sum_of_rgb = 0

                for i in range(len(rgb)-1):  # i dont want the A in RGBA but the pychram has warned me
                    sum_of_rgb += rgb[i]

                x = sum_of_rgb // 3
                x = x // len(color)

                file.write(color[x]+" ")
                # print(color[x], end=" ")
            except:
                pass
        file.write('\n')
    print()


