import cv2
import os
import numpy as np
from detector import get_images_and_labels, trainer_path

def train_model():
    faces, ids = get_images_and_labels(os.path.join(os.getcwd(), "dataset"))
    if len(faces) == 0:
        print("No face samples found in dataset/. Add samples by registering users.")
        return
    recognizer = None
    try:
        recognizer = cv2.face.LBPHFaceRecognizer_create()
    except Exception as e:
        print("Error: cv2.face not available. Install opencv-contrib-python.")
        return
    recognizer.train(faces, np.array(ids))
    recognizer.write(trainer_path)
    print(f"Model trained and saved at {trainer_path}")

if __name__ == "__main__":
    import numpy as np
    train_model()