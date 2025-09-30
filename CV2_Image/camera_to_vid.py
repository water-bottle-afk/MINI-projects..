import cv2
from PIL import Image
#also creating a video from the cavera and saves it in a .avi file
cap = cv2.VideoCapture(0)
if (cap.isOpened() == False):
    print("Error opening video stream or file")


frame_width = int(cap.get(3))
frame_height = int(cap.get(4))

size = (frame_width, frame_height)


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

                    for i in range(len(rgb) - 1):
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



cv2.destroyAllWindows()



"""note: its half working, i see the ascii chars in the console but:
1. i cant stop the program by prerssing Q or S

2. the vid (output) is in .avi form but just from the camera and not from the ascii chars"""
