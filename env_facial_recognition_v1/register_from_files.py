
import db


import log as logger

logger.init("Register_from_file.py",logger.INFO)

IMAGE_PATH = "./data/images_color/"
DB = 'test'

db.connect(DB)


ba = input('Enter your Service Number: ')
firstname = input('Enter Your Name: ')

try:
    db.insertUserProfile(ba, firstname)
    logger.info("Insert Profile Successfully")
    id = db.selectUserID(ba)
    logger.info("id = "+str(id))
    db.insertImagePath(id,ba,IMAGE_PATH)
    logger.info("Insert Image Successfully")
    db.encode_SavetoDB(id)
    logger.info("Update Encoding Successfully")

except Exception as err:
    logger.error('\nError: %s' % (str(err)))




