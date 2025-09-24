import cv2
from PIL import Image

cap = cv2.VideoCapture(0)
if (cap.isOpened() == False):
    print("Error opening video stream or file")



# Read until video is completed
while (cap.isOpened()):
    # Capture frame-by-frame
        ret, frame = cap.read()
        if ret == True:

            img = Image.fromarray(frame)
            img = img.convert("RGBA")
            img = img.resize((50, 50))

            height, width = img.size
            color = ' .;-:!>7?CO$QHNM'

            pixel = img.load()

            for h in range(height):
                for w in range(width):
                    rgb = pixel[w, h]

                    sum_of_rgb = 0

                    for i in range(len(rgb) - 1):  # i dont want the A in RGBA but the pychram has warned me
                        sum_of_rgb += rgb[i]

                    x = sum_of_rgb // 3
                    x = x // len(color)

                    print(color[x], end="")

                print()

            # Press Q on keyboard to  exit
            if cv2.waitKey(20) & 0xFF == ord('q'):
                break

        # Break the loop
        else:
            break

# When everything done, release the video capture object
cap.release()

# Closes all the frames
cv2.destroyAllWindows()
