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
logger.init("db.py",logger.INFO)

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
            sql = "INSERT INTO image(id,img_path) Values( '"+str(
                ba)+"','"+path+ba.replace('\'', '')+"/"+img_path+"')"
            logger.debug(sql)
            cur.execute(sql)
        conn.commit()
    except pg.Error as e:
        logger.error(e.pgerror)


# Update Encoding to Database
def encode_SavetoDB(ba):
    try:
        cursor = conn.cursor()
        sql="""SELECT img_path FROM image WHERE id=%s"""
        cursor.execute(sql,(ba,))

        rows = cursor.fetchall()

        for row in rows:

            _image = face_recognition.load_image_file(str(row[0]))

            small_frame = cv2.resize(_image, (0, 0), fx=0.25, fy=0.25)

            rgb_small_frame = small_frame[:, :, ::-1]
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            _encoding = face_recognition.face_encodings(rgb_small_frame, face_locations)

            logger.debug(type(_encoding))
            logger.debug(_encoding)

            # before write encoding to database
            encoding = cPickle.dumps(_encoding)
            logger.debug(type(encoding))
            logger.debug(encoding)

            ### Convert back to list
            #decoding2 = pickle.loads(encoding)
            #logger.debug(type(decoding2))
            #logger.debug(decoding2)

            sql = """UPDATE image SET img_encoding = %s  WHERE id = %s and img_path = %s"""
            cur = conn.cursor()
            cur.execute(sql,(encoding, ba,str(row[0])))
        conn.commit()

    except pg.Error as e:
        logger.error(e.pgerror)


def decode_DB(ba):
    try:
        cursor = conn.cursor()
        sql = """SELECT i.* from image i where i.id = %s"""
        cursor.execute(sql,(ba,))
        id = cursor.fetchone()
        return cPickle.loads(id[2])
    except pg.Error as e:
        logger.error(e.pgerror)



def selectUserID(ba):
    try:
        cursor = conn.cursor()
        sql = """SELECT id FROM profile WHERE ba=%s"""
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
    sql = '''select p.first_name,p.ba,i.img_encoding from image i,profile p where i.id = p.ba'''
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
