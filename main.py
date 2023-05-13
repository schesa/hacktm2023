
# import required module
import os

import face_recognition
# import numpy as np
from PIL import Image, ImageDraw
# from IPython.display import display
import pickle
from pathlib import Path

 
PERSON_NAME = "Hacktm Jury"
ENCODINGS_PICKLE = "encodings.pkl"

cache_encodings = {}

unknown_picture = face_recognition.load_image_file(f'test_data/{PERSON_NAME}.jpeg')
unknown_face_encodings = face_recognition.face_encodings(unknown_picture)
unknown_face_locations = face_recognition.face_locations(unknown_picture)

def load_train():
    
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
            cache_encodings[f] = train_face_encoding

    with open(ENCODINGS_PICKLE, 'wb') as f:
        pickle.dump(cache_encodings, f)

# Check the file exist or not
if os.path.isfile(ENCODINGS_PICKLE):
   # print the message if file exists
    with open(ENCODINGS_PICKLE, 'rb') as f:
        cache_encodings = pickle.load(f)
else:
    load_train()

pil_image = Image.fromarray(unknown_picture)
draw = ImageDraw.Draw(pil_image)
matching_name = "Unkown"

for unknown_face_encoding in unknown_face_encodings:
    for file, encoding in cache_encodings.items():
        results = face_recognition.compare_faces([encoding], unknown_face_encoding)
        if results[0] == True:
            print(f'Face matching with {file}')
            matching_name = Path(file).stem
            break
        else:
            print(f'Face not matching for {file}')
    # Convert the image to a PIL-format image so that we can draw on top of it with the Pillow library
    # See http://pillow.readthedocs.io/ for more about PIL/Pillow
    # Create a Pillow ImageDraw Draw instance to draw with

    # Loop through each face found in the unknown image
    for (top, right, bottom, left), face_encoding in zip(unknown_face_locations, unknown_face_encodings):
        # See if the face is a match for the known face(s)
        # matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

        # If a match was found in known_face_encodings, just use the first one.
        # if True in matches:
        #     first_match_index = matches.index(True)
        #     name = known_face_names[first_match_index]

        # Or instead, use the known face with the smallest distance to the new face
        # face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        # best_match_index = np.argmin(face_distances)
        # if matches[best_match_index]:
        #     name = known_face_names[best_match_index]

        # Draw a box around the face using the Pillow module
        draw.rectangle(((left, top), (right, bottom)), outline=(0, 0, 255))

        # Draw a label with a name below the face
        print(f'matching name: {matching_name}')
        text_width, text_height = draw.textsize(matching_name)
        draw.rectangle(((left, bottom - text_height - 10), (right, bottom)), fill=(0, 0, 255), outline=(0, 0, 255))
        draw.text((left + 6, bottom - text_height - 5), matching_name, fill=(255, 255, 255, 255))


# Remove the drawing library from memory as per the Pillow docs
del draw

# Display the resulting image
# pil_image.show()
pil_image.save('./result.jpeg', 'JPEG')

# You can also save a copy of the new image to disk if you want by uncommenting this line
# pil_image.save("image_with_boxes.jpg")