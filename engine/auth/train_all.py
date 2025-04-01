import os
import cv2
import face_recognition
import pickle

# Get the directory for storing encodings
base_dir = os.path.dirname(os.path.abspath(__file__))
dlib_models_dir = os.path.join(base_dir, "dlib_models")
samples_dir = os.path.join(base_dir, "samples")

# Ensure the samples directory exists
if not os.path.exists(samples_dir):
    print("❌ Samples directory not found!")
    exit()

# Loop through all image files in the 'samples' directory
for filename in os.listdir(samples_dir):
    image_path = os.path.join(samples_dir, filename)

    # Ensure the file is an image and follows the format face.<id>.<version>.jpg
    if filename.startswith("face.") and filename.endswith(('.jpg', '.jpeg', '.png')):
        parts = filename.split('.')
        if len(parts) < 3:
            print(f"❌ Invalid filename format: {filename}")
            continue
        
        id = parts[1]  # Extract the ID from the filename
        encodings_file = os.path.join(dlib_models_dir, f"{id}.pickle")

        # Prepare the data structure for encodings
        data = {"encodings": [], "names": []}

        # Check if encodings file exists and load it
        if os.path.exists(encodings_file) and os.path.getsize(encodings_file) > 0:
            with open(encodings_file, "rb") as f:
                data = pickle.load(f)

        if not os.path.exists(image_path):
            print(f"❌ Image not found: {image_path}")
            continue

        # Load the image using OpenCV
        image = cv2.imread(image_path)
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Detect face locations and compute encodings
        face_locations = face_recognition.face_locations(rgb_image)
        if face_locations:
            face_encodings = face_recognition.face_encodings(rgb_image, face_locations)

            # Add the new encodings and names
            for encoding in face_encodings:
                data["encodings"].append(encoding)
                data["names"].append(id)

            print(f"✅ Processed {filename} with {len(face_encodings)} encoding(s).")
        else:
            print(f"❌ No face detected in {filename}")

        # Save the updated encodings to the pickle file
        with open(encodings_file, "wb") as f:
            pickle.dump(data, f)

        print(f"✅ Successfully saved encodings to {encodings_file}")