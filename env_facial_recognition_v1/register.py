import PIL.Image
import dlib
import numpy as np
from PIL import ImageFile
import face_recognition_models
import cv2
import face_recognition
import sqlite3
import os, os.path

sampleN = 0
N = 100

detector = dlib.get_frontal_face_detector()


video_capture = cv2.VideoCapture(0)
video_capture.set(cv2.CAP_PROP_AUTOFOCUS, 1)

# get the size of the screen
# screen = screeninfo.get_monitors()[0]
# width, height = screen.width, screen.height


uname = str(input('Enter Your Name: '))

directory = "./data/images_color/"+uname+"/"
if not os.path.exists(directory):
    os.makedirs(directory)


def variance_of_laplacian(image):
    # compute the Laplacian of the image and then return the focus
    # measure, which is simply the variance of the Laplacian
    return cv2.Laplacian(image, cv2.CV_64F).var()


while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()

    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]

    dets = detector(rgb_small_frame, 1)

    #print("Number of faces detected: {}".format(len(dets)))

    for i, d in enumerate(dets):

        sampleN = sampleN+1

        left = d.left()*4  # x
        top = d.top()*4  # y
        right = d.right()*4  # w
        bottom = d.bottom()*4  # h

        # print("Detection {}: Left: {} Top: {} Right: {} Bottom: {}".format(
        #     len(dets), d.left(), d.top(), d.right(), d.bottom()))

        font = cv2.FONT_HERSHEY_DUPLEX

        # # Draw Result on Screen
        # cv2.putText(frame,"Detection Face: Left: {} Top: {} Right: {} Bottom: {}".format(
        # d.left(), d.top(), d.right(), d.bottom()),(20, 30), font, 1.0, (51, 102, 0), 1)

        roi = frame[top+3:bottom-3, left+3:right-3]
        gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        blur_check = variance_of_laplacian(gray_roi)

        print('Bulurry value = {}'.format(blur_check))
        if blur_check < 320:
            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 99), 3)
            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35),
                          (right, bottom), (0, 0, 99), cv2.FILLED)
            cv2.putText(frame, 'Bulurry..{}'.format(blur_check), (left + 6, bottom - 6),
                        font, 1.0, (255, 255, 255), 1)
        else:

            

            cv2.imwrite("./data/images_color/"+uname+"/" +uname+
                        "."+str(sampleN) + ".jpg", roi)


            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (51, 102, 0), 3)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35),
                          (right, bottom), (51, 102, 0), cv2.FILLED)

            cv2.putText(frame, 'Capture..', (left + 6, bottom - 6),
                        font, 1.0, (255, 255, 255), 1)

    # Display the video output
    window_name = 'projector'
    cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN,
                          cv2.WINDOW_FULLSCREEN)
    cv2.imshow(window_name, frame)

    # Quit video by typing Q
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    intNumberofFiles = len([name for name in os.listdir(directory) if os.path.isfile(os.path.join(directory, name))])
    if intNumberofFiles >= N:
        break

video_capture.release()
cv2.destroyAllWindows()
