import dlib
import cv2
import numpy as np

detector = dlib.get_frontal_face_detector()
sp = dlib.shape_predictor("models/shape_predictor_68_face_landmarks.dat")
facerec = dlib.face_recognition_model_v1(
    "models/dlib_face_recognition_resnet_model_v1.dat"
)

def get_face_embedding(frame):
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    faces = detector(rgb, 1)

    if len(faces) != 1:
        return None

    shape = sp(rgb, faces[0])
    embedding = np.array(facerec.compute_face_descriptor(rgb, shape))
    return embedding, shape
