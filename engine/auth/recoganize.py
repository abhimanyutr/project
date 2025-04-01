import os
import cv2
import face_recognition
import pickle
import numpy as np

def AuthenticateFace(image_path=None):
    """
    Authenticate a face either from a live webcam feed or from a provided image file.
    If image_path is None, the function uses a webcam for real-time authentication.
    """
    # Paths
    base_dir = os.path.dirname(os.path.abspath(__file__))
    dlib_models_dir = os.path.join(base_dir, "dlib_models")
    
    # Get list of stored encoding files
    encoding_files = [f for f in os.listdir(dlib_models_dir) if f.endswith(".pickle")]
    
    if not encoding_files:
        print("❌ No stored encodings found!")
        return False
    
    flag = False  # Authentication status
    
    if image_path:
        # Load the provided image
        image = cv2.imread(image_path)
        if image is None:
            print("❌ Failed to load image!")
            return False
        
        rgb_frame = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    else:
        # Open webcam
        video = cv2.VideoCapture(0)
        while True:
            ret, frame = video.read()
            if not ret:
                print("❌ Failed to capture image from webcam!")
                return False
            
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Detect faces
            face_locations = face_recognition.face_locations(rgb_frame)
            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
            
            # Check for a match
            if check_face_match(face_encodings, encoding_files, dlib_models_dir):
                flag = True
                break
            
            cv2.imshow("Authentication", frame)
            if cv2.waitKey(1) & 0xFF == 27:  # Press 'Esc' to exit
                break
        
        video.release()
        cv2.destroyAllWindows()
        return flag
    
    # Process image-based authentication
    face_locations = face_recognition.face_locations(rgb_frame)
    if not face_locations:
        print("❌ No face detected in the image.")
        return False
    
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
    return check_face_match(face_encodings, encoding_files, dlib_models_dir)

def check_face_match(face_encodings, encoding_files, dlib_models_dir):
    """Compares detected face encodings with stored encodings."""
    for encoding_file in encoding_files:
        id_name = os.path.splitext(encoding_file)[0]  # Extract ID from filename
        encoding_path = os.path.join(dlib_models_dir, encoding_file)
        
        # Load stored encodings
        with open(encoding_path, "rb") as f:
            stored_data = pickle.load(f)
        
        stored_encodings = stored_data.get("encodings", [])
        
        for encoding in face_encodings:
            matches = face_recognition.compare_faces(stored_encodings, encoding, tolerance=0.5)
            distances = face_recognition.face_distance(stored_encodings, encoding)
            
            if len(distances) > 0:
                best_match_index = np.argmin(distances)
                best_distance = distances[best_match_index]
                
                if matches[best_match_index] and best_distance < 0.45:
                    print(f"✅ Face matches with ID: {id_name} (Distance: {best_distance:.2f})")
                    return True
    
    print("❌ No match found in stored encodings.")
    return False