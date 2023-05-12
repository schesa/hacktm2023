
# import required module
import os

import face_recognition
import numpy as np
from PIL import Image, ImageDraw
from IPython.display import display

 
PERSON_NAME = "Timo Bejan"

unknown_picture = face_recognition.load_image_file(f'test_data/{PERSON_NAME}.jpg')
unknown_face_encoding = face_recognition.face_encodings(unknown_picture)[0]

# assign directory
directory = 'train_data'

# iterate over files in
# that directory
for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    # checking if it is a file
    if os.path.isfile(f):
        print(f)
        # Now we can see the two face encodings are of the same person with `compare_faces`!
        train_face_picture = face_recognition.load_image_file(f)
        train_face_encoding = face_recognition.face_encodings(train_face_picture)[0]

        # my_face_encoding now contains a universal 'encoding' of my facial features that can be compared to any other picture of a face!
        results = face_recognition.compare_faces([train_face_encoding], unknown_face_encoding)
        if results[0] == True:
            print("Face matching!")
        else:
            print("Face not matching!")
