
import db
import log as logger
import config 

logger.init("load_images.py")

DB = 'test'
db.connect(DB)


faces = [
    ["obama.jpg","Barack Obama","022798129"],
    ["biden.jpg","Joe Biden","039436788"],
    ["tanya.jpg","Tanya S.","0962536559"],
    ["bingo.jpg","Bingo","0962536366"],
    ["lulliya.jpg","Lulliya","025051147"]
    ]

#Save DB
for face in faces:
    db.save2DB(face)