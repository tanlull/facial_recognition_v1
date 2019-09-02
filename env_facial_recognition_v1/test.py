import PIL.Image
import dlib
import numpy as np
from PIL import ImageFile
import face_recognition_models
import cv2
import face_recognition
import sqlite3
import os
import os.path
import random
import sys
import pickle


# conn = sqlite3.connect("./data/dbFacerecognition.db")

# email = str(input('Enter your Emial-Address: '))


# def selectUserID(conn, email):
    
#     cursor = conn.cursor()
#     cursor.execute("SELECT id FROM tbProfile WHERE email=?", (email, ))
#     u_id = cursor.fetchone()
#     return u_id[0]

# print(selectUserID(conn,email))



def encode_SavetoDB(u_id):
    conn = sqlite3.connect("./data/dbFacerecognition.db")
    cursor = conn.cursor()
    cursor.execute("SELECT img_path FROM tbImage WHERE u_id=?", (u_id, ))

    rows = cursor.fetchall()

    for row in rows:
        
        _image = face_recognition.load_image_file(str(row[0]))

        _encoding = face_recognition.face_encodings(_image)

        #print(type(_encoding[0]))  

        print(_encoding)

        with open('dataset_faces.dat', 'wb') as f:
                pickle.dump(all_face_encodings, f)
        

        
      

   

encode_SavetoDB(19)

# img = cv2.imread("./data/images_color/amornpan@gmail.com/0.507205920034092.jpg")

 
# cv2.imshow('sample image',img)
 
# cv2.waitKey(0) # waits until a key is pressed
# cv2.destroyAllWindows() # destroys the window showing image



