DROP TABLE IF EXISTS 'tbProfile';
CREATE TABLE 'tbProfile' (
  'id' INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  'first_name' NVARCHAR(50) ,
  'last_name' NVARCHAR(50)  ,
  'email' NVARCHAR(50)  NOT NULL,
  'mobile' NVARCHAR(20)  NOT NULL,
  'create_date' TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)

DROP TABLE IF EXISTS 'tbImage';
CREATE TABLE 'tbImage' (
    'id' INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    'u_id' INTEGER NOT NULL,
    'img_path' TEXT  NOT NULL,
    'img_encoding' TEXT  ,
    CONSTRAINT `fk_tbProfile_id`
        FOREIGN KEY ('u_id') REFERENCES 'tbProfile' ('id')
        ON DELETE CASCADE
        ON UPDATE CASCADE
) 