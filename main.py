
# import required module
import os
import shutil
import time
import re
import face_recognition
# import numpy as np
from PIL import Image, ImageDraw
# from IPython.display import display
import pickle
from pathlib import Path


PERSON_NAME = "Hacktm Jury"
ENCODINGS_PICKLE = "encodings.pkl"

cache_encodings = {}

def list_files(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            print(file_path)

def get_file_extension(filename):
    pattern = r'\.(\w+)$'
    match = re.search(pattern, filename)
    if match:
        return match.group(1)
    else:
        return None


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


def process_image(unknown_picture,  unknown_face_locations, unknown_face_encodings, result_file, extension, result_names_file):
    pil_image = Image.fromarray(unknown_picture)
    draw = ImageDraw.Draw(pil_image)

    matching_name_arr = []
    for i, unknown_face_encoding in enumerate(unknown_face_encodings):
        for file, encoding in cache_encodings.items():
            results = face_recognition.compare_faces([encoding], unknown_face_encoding)
            if results[0] == True:
                print(f'Face matching with {file}')
                matching_name = Path(file).stem
                matching_name_arr.append(matching_name)
                break
            else:
                print(f'Face not matching for {file}')
        # Convert the image to a PIL-format image so that we can draw on top of it with the Pillow library
        # See http://pillow.readthedocs.io/ for more about PIL/Pillow
        # Create a Pillow ImageDraw Draw instance to draw with

        # Loop through each face found in the unknown image
        print(type(unknown_face_locations))
        print(unknown_face_locations)
        print(i)

        if matching_name_arr:
            try:
              with open(result_names_file, 'w') as f:
                for item in matching_name_arr:
                  f.write("%s\n" % item)
            except IOError as e:
              print(f"An error occurred while writing to the file: {e}")

        (top, right, bottom, left) = unknown_face_locations[i]
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
        # pil_image.save(f'./result{matching_name}.jpeg', 'JPEG')

    # Remove the drawing library from memory as per the Pillow docs
    del draw

    # Display the resulting image
    # pil_image.show()
    pil_image.save(result_file, extension)


def scan_directory(directory):
    # Keep track of the last processed directory number
    last_processed_number = None
    last_file_name = None

    while True:
        # Get the list of directories in the given directory
        directories = [d for d in os.listdir(directory) if os.path.isdir(os.path.join(directory, d))]

        # Filter the directories based on the specified conditions
        filtered_directories = []
        for d in directories:
            if d.startswith("work_"):
                work_number = d.split("_")[-1]
                work_dir = os.path.join(directory, d)
                upload_files = [f for f in os.listdir(work_dir) if f.startswith(f"upload_{work_number}")]
                processed_dir = os.path.join(directory, f"{d}/processed_{work_number}")

                if upload_files and not os.path.isdir(processed_dir):
                    filtered_directories.append((d, upload_files[0]))

        # Process the filtered directory
        if filtered_directories:
            d, file_name = filtered_directories[0]
            if d != last_processed_number and file_name != last_file_name:
                print(f"Processing directory: {d}")
                print(f"Matching file: {d}/{file_name}")

                # Create the processed directory
                work_number = d.split("_")[-1]
                processed_dir = os.path.join(directory, f"{d}", f"processed_{work_number}")
                os.makedirs(processed_dir)
                file_extension = get_file_extension(file_name)
                result_file_name = f"{processed_dir}/result.{file_extension}"
                restult_names_file_name = f"{processed_dir}/names.txt"

                unknown_picture = face_recognition.load_image_file(f"/uploads/{d}/{file_name}")
                unknown_face_encodings = face_recognition.face_encodings(unknown_picture)
                unknown_face_locations = face_recognition.face_locations(unknown_picture)

                process_image(unknown_picture, unknown_face_locations, unknown_face_encodings, result_file_name, file_extension, restult_names_file_name)

                # Update the last processed directory number and file name
                last_processed_number = d
                last_file_name = file_name

        # Sleep for 5 seconds before scanning again
        time.sleep(5)


# Call the function to start scanning the directory
scan_directory('/uploads')

# You can also save a copy of the new image to disk if you want by uncommenting this line
# pil_image.save("image_with_boxes.jpg")