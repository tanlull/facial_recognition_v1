import psycopg2 as pg
import sys
import numpy as np
import db
import pickle
import face_recognition
import os
import base64
import cv2
import _pickle as cPickle

import log as logger
logger.init("db.py",logger.DEBUG)

from six.moves import configparser
config = configparser.ConfigParser()
config.read("parameters.ini")

conn = {};



def connect(db):
    global conn
    try:
        if(db=="test"):
            thost=config.get("TestDB", "host")
            tdatabase=config.get("TestDB", "database")
            tuser=config.get("TestDB", "user")
            tpassword=config.get("TestDB", "password")
        else:
            thost=config.get("PrdDB", "host")
            tdatabase=config.get("PrdDB", "database")
            tuser=config.get("PrdDB", "user")
            tpassword=config.get("PrdDB", "password")
       #logger.info("{0},{1},{2},{3}".format(thost,tdatabase,tuser,tpassword))
        conn = pg.connect(host=thost,database=tdatabase, user=tuser, password=tpassword)
        logger.debug("Database connect successfully")
        return True
        
    except:
        logger.error("Cannot connect to the database.")
        return False


def insertImagePath(id,ba,path):
    try:
        cur = conn.cursor()

        for img_path in listImagePath(ba.replace('\'', ''),path):
            sql = "INSERT INTO image(id,img_path,img_encoding) Values('"+str(id)+"','"+path+ba.replace('\'', '')+"/"+img_path+"','0')"
            logger.debug(sql)
            cur.execute(sql)
        conn.commit()
    except pg.Error as e:
        logger.error(e.pgerror)


# Update Encoding to Database
def encode_SavetoDB(id):
    try:
        cursor = conn.cursor()
        sql="""SELECT img_path,ctid FROM image WHERE id=%s and octet_length(img_encoding) < 10"""
        cursor.execute(sql,(str(id),))
        logger.info("Select {} Rows".format(cursor.rowcount))
        rows = cursor.fetchall()
        logger.debug(type(rows))
        logger.debug(rows)

        for row in rows:
            ctid = str(row[1])
            img_path = str(row[0])
            logger.info("ctid = {0}, image_path = {1}".format(ctid,img_path))

            _encoding = encode_face_image(str(row[0]))

            # logger.debug(type(_encoding))
            # logger.debug(_encoding)

            # before write encoding to database
            encoding = cPickle.dumps(_encoding)
            logger.debug(type(encoding))
            logger.debug(encoding)

            try:
                sql = """UPDATE image SET img_encoding = %s  WHERE ctid = %s"""
                cur = conn.cursor()
                cur.execute(sql,(pg.Binary(encoding),ctid))
                conn.commit()
                logger.info("Update {} Row Successfully".format(cur.rowcount))
            except pg.Error as e:
                logger.error(e.pgerror)
                pass
            
        logger.info("Finished Update Image Encoding DB!!! ")
    except pg.Error as e:
        logger.error(e.pgerror)
        pass


def decode_DB(id):
    try:
        cursor = conn.cursor()
        sql = """SELECT i.* from image i where i.id = %s"""
        cursor.execute(sql,(str(id),))
        first_id = cursor.fetchone()
        return cPickle.loads(first_id[2])
    except pg.Error as e:
        logger.error(e.pgerror)



def selectUserID(ba):
    try:
        cursor = conn.cursor()
        sql = """SELECT id FROM profile WHERE ba=%s order by id desc"""
        cursor.execute(sql,(ba,))
        id = cursor.fetchone()

        return id[0]
    except pg.Error as e:
        logger.error(e.pgerror)


def insertUserProfile(ba, firstname):
    try:
        isRowExist = 0
        cur = conn.cursor()
        sql = "SELECT * FROM profile WHERE ba='{0}'".format(ba)
        logger.debug(sql)
        cur.execute(sql)
        rows = cur.fetchall()
        logger.debug("Fetch Success")
        for row in rows:
            isRowExist = 1

        if(isRowExist==1):
            logger.debug("Existing {} ba addresss !! ".format(ba.replace('\'', '')))
            return False
        else:
            sql = "INSERT INTO profile(ba,first_name) Values( '"+ba+"','"+firstname+"')"
            logger.debug("Insert {0} Successfully".format(ba))
            cur.execute(sql)
            conn.commit()
            return True
    except pg.Error as e:
        logger.error(e.pgerror)



def listImagePath(ba,path):
    foldername = ba
    path = path+foldername
    dirs = os.listdir(path)
    list_files = []
    for filename in dirs:
        (shortname, extension) = os.path.splitext(filename)
        if extension == '.jpg':
            list_files.append(filename)
    return list_files


def getAllFaceData():
    # Create arrays of known face encodings and their names
    known_face_encodings = []
    known_face_names =[]
    known_face_ba =[]
    # global conn
    cursor = conn.cursor()
    sql = '''select p.first_name,p.ba,i.img_encoding from image i,profile p where i.id = p.id'''
    cursor.execute(sql)

    rows = cursor.fetchall()

    for row in rows:
        # read encoding
        if(len(row[2])>10):
            encode = cPickle.loads(row[2])
            known_face_encodings.append(encode)
            known_face_names.append(str(row[0]))
            known_face_ba.append(str(row[1]))
    
    return known_face_names,known_face_encodings,known_face_ba



### FOR load_images.py #####

def encode_face_image(image):
    image_to_encode = face_recognition.load_image_file(image)
    face_locations = face_recognition.face_locations(image_to_encode)
    image_to_encode_encoding = face_recognition.face_encodings(image_to_encode,face_locations)[0]
    return image_to_encode_encoding


def save2DB(face):
    image_encode = encode_face_image(face[0])
    encoding = cPickle.dumps(image_encode)
    db.SaveImage2DB(face[0],face[1],face[2],encoding)
    
## Store face to Postgres DB
def SaveImage2DB(image_name,person_name,ba,encoding):
    try:
        insertUserProfile(ba,person_name)
        id = db.selectUserID(ba)
        cur = conn.cursor()
        logger.debug("Insert {} , ba = {}".format(image_name,ba))
        sql = """INSERT into image(id,img_path,img_encoding) Values(%s , %s , %s)"""
        cur.execute(sql,(id,image_name,pg.Binary(encoding)))
        conn.commit()
        logger.debug("Successfully inserted")
    except pg.Error as e:
        logger.error(e.pgerror)