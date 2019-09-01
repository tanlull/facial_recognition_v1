import os
import sqlite3
import sys
import time

conn = sqlite3.connect("./data/dbFacerecognition.db")

email = str(input('Enter your Emial-Address: '))


def selectUserID(conn, email):
    #print(email)
    #print(type(email))
    cur = conn.cursor()
    cur.execute("SELECT id FROM tbProfile WHERE email=?", (email,))

    cursor = conn.cursor()
    cursor.execute("SELECT id FROM tbProfile WHERE email=?", (email, ))
    u_id = cursor.fetchone()
    return u_id[0]

print(selectUserID(conn,email))
#print('uid = {}'.format(selectUserID(conn,email)))