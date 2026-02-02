import streamlit as st
import cv2
import pickle
import numpy as np
from scipy.spatial.distance import cosine

from src.face_utils import get_face_embedding
from src.spoof import is_blinking
from src.attendance import init_db, mark_attendance

DATA_FILE = "data/embeddings.pkl"
THRESHOLD = 0.4

init_db()

st.set_page_config(page_title="Face Attendance System", layout="centered")
st.title("🧑‍💻 Face Authentication Attendance System")

menu = st.sidebar.selectbox("Select Action", ["Register", "Mark Attendance"])

# Load embeddings
try:
    with open(DATA_FILE, "rb") as f:
        known_faces = pickle.load(f)
except:
    known_faces = {}

cap = cv2.VideoCapture(0)

if menu == "Register":
    st.subheader("Register New User")
    name = st.text_input("Enter User Name")

    if st.button("Start Registration"):
        embeddings = []
        st.info("Capturing face samples... Blink naturally.")

        while len(embeddings) < 20:
            ret, frame = cap.read()
            result = get_face_embedding(frame)

            if result:
                emb, _ = result
                embeddings.append(emb)

            st.image(frame, channels="BGR")

        avg_emb = np.mean(embeddings, axis=0)
        known_faces[name] = avg_emb

        with open(DATA_FILE, "wb") as f:
            pickle.dump(known_faces, f)

        st.success(f"{name} registered successfully!")

elif menu == "Mark Attendance":
    st.subheader("Face Authentication")
    blinked = False

    frame_window = st.image([])

    while True:
        ret, frame = cap.read()
        result = get_face_embedding(frame)

        if result:
            emb, shape = result

            if is_blinking(shape):
                blinked = True

            for name, stored_emb in known_faces.items():
                dist = cosine(emb, stored_emb)

                if dist < THRESHOLD and blinked:
                    action = mark_attendance(name)
                    st.success(f"{name}: {action}")
                    cap.release()
                    cv2.destroyAllWindows()
                    st.stop()

        frame_window.image(frame, channels="BGR")
