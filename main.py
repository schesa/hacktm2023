import face_recognition

PERSON_NAME = "Timo Bejan"

unknown_picture = face_recognition.load_image_file(f'test_data/{PERSON_NAME}.jpg')
unknown_face_encoding = face_recognition.face_encodings(unknown_picture)[0]

# Now we can see the two face encodings are of the same person with `compare_faces`!

picture_of_me = face_recognition.load_image_file(f'train_data/{PERSON_NAME}.jpg')
my_face_encoding = face_recognition.face_encodings(picture_of_me)[0]

# my_face_encoding now contains a universal 'encoding' of my facial features that can be compared to any other picture of a face!

results = face_recognition.compare_faces([my_face_encoding], unknown_face_encoding)

if results[0] == True:
    print("Face matching!")
else:
    print("Face not matching!")

# import face_recognition
# import numpy as np
# from PIL import Image, ImageDraw
# from IPython.display import display

# # This is an example of running face recognition on a single image
# # and drawing a box around each person that was identified.

# # Load a sample picture and learn how to recognize it.
# obama_image = face_recognition.load_image_file("obama.jpg")
# obama_face_encoding = face_recognition.face_encodings(obama_image)[0]

# # Load a second sample picture and learn how to recognize it.
# biden_image = face_recognition.load_image_file("biden.jpg")
# biden_face_encoding = face_recognition.face_encodings(biden_image)[0]

# # Create arrays of known face encodings and their names
# known_face_encodings = [
#     obama_face_encoding,
#     biden_face_encoding
# ]
# known_face_names = [
#     "Barack Obama",
#     "Joe Biden"
# ]
# print('Learned encoding for', len(known_face_encodings), 'images.')