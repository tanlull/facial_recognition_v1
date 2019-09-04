import os
import os.path
import sqlite3

def listImagePath(email):
    foldername = email
    path = './data/images_color/'+foldername
    dirs = os.listdir(path)
    list_files = []
    for filename in dirs:
        (shortname, extension) = os.path.splitext(filename)
        if extension == '.jpg':
            list_files.append(filename)
    return list_files

def 

## Insert photo path to database
def insertImagePath(u_id):

    conn = sqlite3.connect("./data/dbFacerecognition.db")

    for img_path in listImagePath(email):
        sql = "INSERT INTO tbImage(u_id,img_path) Values( "+u_id+","+img_path+")"
        conn.execute(sql)
        conn.commit()

    conn.close()