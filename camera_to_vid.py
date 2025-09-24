import cv2
import numpy as np
from PIL import Image

cap = cv2.VideoCapture(0)
if (cap.isOpened() == False):
    print("Error opening video stream or file")

# Define the codec and create VideoWriter object.The output is stored in 'outpy.avi' file.

# We need to set resolutions.
# so, convert them from float to integer.
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))

size = (frame_width, frame_height)

# Below VideoWriter object will create
# a frame of above defined The output
# is stored in 'filename.avi' file.
result = cv2.VideoWriter('fileam.avi',
                         cv2.VideoWriter_fourcc(*'MJPG'),
                         10, size)

# Read until video is completed
while (cap.isOpened()):
    # Capture frame-by-frame
    try:
        ret, frame = cap.read()
        if ret == True:

            img = Image.fromarray(frame)
            img = img.convert("RGBA")
            img = img.resize((50, 50))

            result.write(frame)

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
                cap.release()
                result.release()
                break

        # Break the loop
        else:
            cap.release()
            result.release()
            break
    except:
        cap.release()
        result.release()
        exit()
        pass

# When everything done, release the video capture object
cap.release()
result.release()


# Closes all the frames
cv2.destroyAllWindows()



"""note: its half working, i see the ascii chars in the console but:
1. i cant stop the program by prerssing Q or S
2. the vid (output) is in .avi form but just from the camera and not from the ascii chars"""