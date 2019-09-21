import PIL.Image
import dlib
import numpy as np
from PIL import ImageFile
import face_recognition_models
import cv2
import face_recognition
import log as logger
import db
import _pickle as cPickle

logger.init("webcam.py",logger.INFO)
DB = 'test'
db.connect(DB)

# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture(0)


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


# known_face_encodings = []
# known_face_names =[]
# known_face_ba = [] 

# for face in faces:
#     encode=encode_face_image(face[0])
#     known_face_encodings.append(encode)
#     known_face_names.append(face[1])

# Get data from database
known_face_names,known_face_encodings,known_face_ba = db.getAllFaceData()


# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Only process every other frame of video to save time
    if process_this_frame:
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        face_info = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = ""
            info = ""

            # # If a match was found in known_face_encodings, just use the first one.
            # if True in matches:
            #     first_match_index = matches.index(True)
            #     name = known_face_names[first_match_index]

            # Or instead, use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            logger.debug(" Match Index = {}".format(best_match_index))
            if matches[best_match_index]:
                name = known_face_names[best_match_index]
                info = known_face_ba[best_match_index]

            face_names.append(name)
            face_info.append(info)

    process_this_frame = not process_this_frame


    # Display the results
    for (top, right, bottom, left), name, info in zip(face_locations, face_names,face_info):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom + 100), (right, bottom), (0, 0, 255), cv2.FILLED)
        cv2.rectangle(frame, (left, top - 30), (right, top), (0, 255, 0), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, top-5 ), font, 1.0, (0, 0, 0), 1)
        cv2.putText(frame, info, (left + 6, bottom + 30), font, 1.0, (255, 255, 255), 1)

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()


