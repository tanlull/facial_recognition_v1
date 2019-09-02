with open('dataset_faces.dat', 'wb') as f:
    pickle.dump(all_face_encodings, f)