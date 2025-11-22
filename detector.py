import cv2
import os
import numpy as np
from PIL import Image
import json
from db import mark_attendance

# Paths
dataset_path = os.path.join(os.getcwd(), "dataset")
trainer_path = os.path.join(os.getcwd(), "trainer.yml")
os.makedirs(dataset_path, exist_ok=True)

# Use Haarcascade from OpenCV data path
cascade_path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"

def register_face(uid:int, name:str, samples:int=20):
    cam = cv2.VideoCapture(0)
    detector = cv2.CascadeClassifier(cascade_path)
    count = 0
    while True:
        ret, img = cam.read()
        if not ret:
            print("Failed to grab frame from webcam.")
            break
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = detector.detectMultiScale(gray, 1.3, 5)
        for (x,y,w,h) in faces:
            count += 1
            face_img = gray[y:y+h, x:x+w]
            file_path = os.path.join(dataset_path, f"User.{uid}.{count}.jpg")
            cv2.imwrite(file_path, face_img)
            cv2.rectangle(img, (x,y), (x+w, y+h), (255,0,0), 2)
            cv2.putText(img, f"Sample {count}/{samples}", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)
        cv2.imshow('Register - Press q to quit', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        if count >= samples:
            break
    cam.release()
    cv2.destroyAllWindows()
    # save name mapping
    save_name_mapping(uid, name)

def save_name_mapping(uid, name):
    p = os.path.join(os.getcwd(), "names.json")
    d = {}
    if os.path.exists(p):
        with open(p, 'r') as f:
            try:
                d = json.load(f)
            except:
                d = {}
    d[str(uid)] = name
    with open(p, 'w') as f:
        json.dump(d, f)

def get_images_and_labels(path):
    image_paths = [os.path.join(path, f) for f in os.listdir(path) if f.endswith(".jpg") or f.endswith(".png")]
    face_samples = []
    ids = []
    for imagePath in image_paths:
        pil_img = Image.open(imagePath).convert('L') # grayscale
        img_numpy = np.array(pil_img, 'uint8')
        # filename format: User.<id>.<count>.jpg
        filename = os.path.split(imagePath)[-1]
        try:
            id = int(filename.split(".")[1])
        except:
            continue
        faces = cv2.CascadeClassifier(cascade_path).detectMultiScale(img_numpy)
        for (x,y,w,h) in faces:
            face_samples.append(img_numpy[y:y+h, x:x+w])
            ids.append(id)
    return face_samples, ids

def start_recognition(confidence_threshold=60):
    # Load names
    names = {}
    names_path = os.path.join(os.getcwd(), "names.json")
    if os.path.exists(names_path):
        with open(names_path, 'r') as f:
            names = json.load(f)

    # Check recognizer
    if not os.path.exists(trainer_path):
        print("No trained model found. Please train first.")
        return

    recognizer = None
    try:
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        recognizer.read(trainer_path)
    except Exception as e:
        print("Error creating recognizer. Ensure opencv-contrib-python is installed.")
        print("Exception:", e)
        return

    cam = cv2.VideoCapture(0)
    detector = cv2.CascadeClassifier(cascade_path)
    while True:
        ret, img = cam.read()
        if not ret:
            print("Failed to read from webcam.")
            break
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = detector.detectMultiScale(gray, 1.2, 5)
        for(x,y,w,h) in faces:
            id, confidence = recognizer.predict(gray[y:y+h, x:x+w])
            if confidence < confidence_threshold:
                name = names.get(str(id), f"User-{id}")
                mark_attendance(id, name)
                label = f"{name} ({int(confidence)})"
            else:
                label = "Unknown"
            cv2.rectangle(img, (x,y), (x+w, y+h), (0,255,0), 2)
            cv2.putText(img, label, (x, y-10), cv2.FONT_HERSHEY_PLAIN, 1.2, (255,255,255), 2)
        cv2.imshow('Attendance - Press q to exit', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cam.release()
    cv2.destroyAllWindows()