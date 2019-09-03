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
from PIL import Image


# conn = sqlite3.connect("./data/dbFacerecognition.db")

# email = str(input('Enter your Emial-Address: '))


# def selectUserID(conn, email):

#     cursor = conn.cursor()
#     cursor.execute("SELECT id FROM tbProfile WHERE email=?", (email, ))
#     u_id = cursor.fetchone()
#     return u_id[0]

# print(selectUserID(conn,email))


def compareAllFaceFromEncoding(known_face_encodings,face_encoding):
    for face_encoding in encodeFromDB:
            
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"
            
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            
            if matches[best_match_index]:
                name = known_face_names[best_match_index]

            face_names.append(name)


def showAllFaceFromEncoding():
    conn = sqlite3.connect("./data/dbFacerecognition.db")
    cursor = conn.cursor()
    cursor.execute("SELECT img_encoding,img_path FROM tbImage")

    rows = cursor.fetchall()

    for row in rows:

        # read encoding
        _encoding = pickle.loads(eval(str(row[0])))

        # convert to image
        # _image = face_recognition.load_image_file(str(row[1]))
        # return _image
        
        img = cv2.imread(str(row[1]))


        cv2.imshow('sample image', img)
        print(str(row[1]))

        cv2.waitKey(0)  # waits until a key is pressed
        cv2.destroyAllWindows()  # destroys the window showing image

    #return str(row[1])


#showAllFaceFromEncoding()

def read_Encode_Image_fromDB(u_id):
    encoding = []
    conn = sqlite3.connect("./data/dbFacerecognition.db")
    cursor = conn.cursor()
    cursor.execute("SELECT img_encoding FROM tbImage WHERE u_id=?", (u_id, ))

    rows = cursor.fetchall()

    for row in rows:

        # read encoding
        encoding = pickle.loads(eval(str(row[0])))

        # print(encoding)
    return encoding

#list1 = read_Encode_Image_fromDB(19)
# print(list1[0])


def selectJoinTable(face_encoding):
    result_compare = [[]]
    conn = sqlite3.connect("./data/dbFacerecognition.db")
    cursor = conn.cursor()
    cursor.execute(''' SELECT 
                   tbProfile.first_name , 
                   tbProfile.email ,
                   tbImage.u_id,
                   tbImage.img_encoding
                   FROM
                   tbProfile LEFT JOIN tbImage
                   ON
                   tbProfile.id = tbImage.u_id;
                   ''')

    rows = cursor.fetchall()

    for row in rows:
      # read encoding
      known_face_encodings.append(pickle.loads(eval(str(row[3]))))
    
      known_face_names.append(str(row[0]))
      
      face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
      result_compare.append(face_distances,)
      print('firstname = {}'.format(encoding))
    #return result

selectJoinTable()

def encode_SavetoDB(u_id):
    conn = sqlite3.connect("./data/dbFacerecognition.db")
    cursor = conn.cursor()
    cursor.execute("SELECT img_path FROM tbImage WHERE u_id=?", (u_id, ))

    rows = cursor.fetchall()

    for row in rows:

        _image = face_recognition.load_image_file(str(row[0]))

        _encoding = face_recognition.face_encodings(_image)

        # before write encoding to database
        encoding = pickle.dumps(_encoding)

        sql = ''' UPDATE tbImage
              SET img_encoding = ?
              WHERE u_id = ?'''

        cur = conn.cursor()
        cur.execute(sql, [encoding, u_id])
        conn.commit()

# encode_SavetoDB(19)


# img = cv2.imread(showAllFaceFromEncoding())


# cv2.imshow('sample image', img)

# cv2.waitKey(0)  # waits until a key is pressed
# cv2.destroyAllWindows()  # destroys the window showing image
