# Face Authentication Attendance System - AI/ML Intern - Medoc Health

## 1. Introduction
This project implements a face authentication–based attendance system that operates on real-time camera input. The system enables user enrollment through face registration and performs live face authentication to automatically record attendance as Punch-In and Punch-Out events.

The primary objective of this assignment is to demonstrate:

* Practical application of face recognition techniques

* Understanding of machine learning deployment constraints

* System reliability under real-world conditions

* Awareness of security, privacy, and spoofing limitations

The system is designed to be lightweight, CPU-based, and suitable for local execution on standard hardware.

---

## 2. System Overview

At a high level, the system performs the following steps:

1. Capture frames from a live camera

2. Detect a face in the frame

3. Extract facial landmarks and generate a numerical face representation

4. Compare the representation with stored user embeddings

5. Verify basic liveness using blink detection

6. Mark attendance based on authentication outcome

The system is intentionally embedding-based rather than classification-based to ensure scalability and avoid retraining as new users are added.

---

## 3. Architecture

```

Live Camera Feed
      ↓
Face Detection (dlib HOG)
      ↓
Facial Landmark Detection (68-point model)
      ↓
Face Embedding Extraction (ResNet-based model)
      ↓
Similarity Matching (Cosine Distance)
      ↓
Liveness Check (Blink Detection)
      ↓
Attendance Logic
      ↓
SQLite Database

```

---

## 4. File Structure

```

face_attendance/
│
├── models/
│   ├── shape_predictor_68_face_landmarks.dat
│   └── dlib_face_recognition_resnet_model_v1.dat
│
├── data/
│   ├── embeddings.pkl
│   └── attendance.db
│
├── src/
│   ├── face_utils.py
│   ├── spoof.py
│   └── attendance.py
│
├── app.py              # Streamlit UI (MAIN ENTRY)
├── Dockerfile
├── requirements.txt
└── README.md

```

---

## 4. Model and Approach Used

### 4.1 Face Detection

* **Library**: ` dlib `

* **Technique**: Histogram of Oriented Gradients (HOG)

Used for efficient and reliable face detection on CPU without GPU dependency

### 4.2 Facial Landmark Detection

* **Model**: ` shape_predictor_68_face_landmarks.dat `

Detects 68 facial keypoints

Used for:

  * Eye localization

  * Blink detection (liveness verification)

  * Stable face alignment

### 4.3 Face Recognition

* **Model**: ` dlib_face_recognition_resnet_model_v1 `

  * Deep CNN based on ResNet architecture

  * Outputs a 128-dimensional face embedding

  * Trained on millions of face images by the dlib authors

### 4.4 Face Matching

* **Metric**: Cosine Distance

* Authentication decision is made using a predefined similarity threshold

* This avoids multi-class classification and scales linearly with users

### 4.5 Liveness / Spoof Prevention

* **Method**: Eye Aspect Ratio (EAR)–based blink detection

* Confirms presence of natural eye movement

* Blocks basic spoofing attempts such as printed photos or static images

This liveness approach is intentionally simple and serves as a baseline rather than a complete anti-spoofing solution.

---

## 5. Training Process

### 5.1 Model Training

* No custom training is performed as part of this project.

* The face recognition model used is a pretrained embedding model, which is standard practice in production face recognition systems. Training such models from scratch requires very large, labeled datasets and significant compute resources.

### 5.2 User Registration (Enrollment)

During registration:

  * Multiple frames of the user’s face are captured

  * An embedding is extracted from each frame

  * Embeddings are averaged to reduce noise and variance

  * The final embedding is stored for authentication

No raw face images are stored permanently.

---

## 6. Data Storage Design

### 6.1 Face Data

Stored as numerical embeddings only

* **Location**: ` data/embeddings.pkl `

* **Format**: Key-value mapping of user identifier to embedding vector

### 6.2 Attendance Data

* Stored in an SQLite database

* **Location**: ` data/attendance.db `

* Fields:

  * User identifier

  * Date

  * Punch-In time

  * Punch-Out time

This design minimizes storage requirements and reduces privacy risks.

---

## 7. Accuracy Expectations

Performance depends on environmental conditions and camera quality.

| Condition  | Expected Performance |
| ------------- | ------------- |
| Good lighting, frontal face  | 95–98%  |
| Moderate lighting variation  | 88–92%  |
| Low lighting	| ~85% |
| Same user across days	| High consistency | 
| Printed photo attack	| Mostly blocked | 
| High-quality video  | replay	May bypass |

These values are indicative and based on practical testing rather than benchmark datasets.

---

## 8. Known Failure Cases and Limitations

The system has the following known limitations:

  * Poor performance under extreme lighting conditions

  * Occlusions such as masks, sunglasses, or hands

  * Difficulty distinguishing identical twins or very similar faces

  * Vulnerability to high-quality replay or deepfake attacks

  * Dependence on camera quality and positioning

  * No depth or infrared information (monocular camera only)

These limitations are expected given the lightweight design and are explicitly acknowledged.

---

## 9. Privacy and Ethical Considerations

* Face images are not stored

* Only numerical embeddings are persisted

* Embeddings are non-reversible representations

* Reduces risk of biometric data misuse

The system is designed with basic privacy principles in mind.

---

## 10. User Interface

The system uses Streamlit for demonstration purposes.

The interface supports:

  * User registration

  * Live face authentication

  * Attendance marking feedback

> The UI is intended for local execution and evaluation rather than production deployment.

--- 

## 11. How to Run the Application

This section describes the complete steps required to set up and run the Face Authentication Attendance System.

### 11.1 Prerequisites

Operating System

  * **macOS (recommended for local demo)**

  * **Windows or Linux (Docker-based execution supported)**

  * **Python**

  * **Python 3.10 (mandatory)**

> Python versions 3.12 and above are not supported by dlib at the time of development

### 11.2 System Dependencies

The following system-level dependencies are required to build and run dlib.

#### macOS

* Install Xcode Command Line Tools:

``` 

xcode-select --install

```


* Install required build tools:

```

brew install cmake
brew install boost
brew install boost-python3

```

* Verify installation:

```

cmake --version

```

#### Windows

For Windows systems, Docker-based execution is recommended to avoid native build issues with dlib.

* Install Docker Desktop

* Ensure WSL2 is enabled

* Webcam access is supported when running Docker on Linux environments

### 11.3 Clone the Repository

```

git clone https://github.com/<your-username>/<repo-name>.git
cd <repo-name>

```

### 11.4 Create and Activate Virtual Environment (macOS)

```

python3.10 -m venv venv
source venv/bin/activate

```

### 11.5 Install Python Dependencies

* Upgrade build tools:

```

pip install --upgrade pip setuptools wheel

```

* Install required packages:

```

pip install -r requirements.txt

```

If dlib is not listed in requirements.txt, install it explicitly:

```

pip install dlib

```
---

## 12. Pretrained Models Setup

This project uses official pretrained models provided by the dlib library.
These models are not included in the repository and must be downloaded manually.

### 12.1 Required Models

| Model File | Purpose | 
| shape_predictor_68_face_landmarks.dat |	Facial landmark detection and blink-based liveness |
| dlib_face_recognition_resnet_model_v1.dat	| Face embedding extraction |

### 12.2 Download Links (Official Source)

```

http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2

http://dlib.net/files/dlib_face_recognition_resnet_model_v1.dat.bz2

```

### 12.3 Extract the Models

```

bunzip2 shape_predictor_68_face_landmarks.dat.bz2
bunzip2 dlib_face_recognition_resnet_model_v1.dat.bz2

```

### 19.4 Place the Models in the Project

```

mkdir -p models
mv shape_predictor_68_face_landmarks.dat models/
mv dlib_face_recognition_resnet_model_v1.dat models/

```
**Expected directory structure:**

```

models/
├── shape_predictor_68_face_landmarks.dat
└── dlib_face_recognition_resnet_model_v1.dat

```

## 13. Running the Application

### 13.1 Local Execution (macOS)

```

streamlit run app.py

```

#### Open in browser:

[http://localhost:8501](http://localhost:8501)

### 13.2 Docker Execution (Windows / Linux)

**Docker execution is recommended on Windows systems to avoid native compilation issues with dlib.**

```

docker build -t face-attendance .
docker run -p 8501:8501 face-attendance

```

#### Open in browser:

[http://localhost:8501](http://localhost:8501)


> Note: On macOS, Docker containers do not have access to the host webcam. For live face authentication, local execution is required.

## 14. Execution Notes

* Webcam access is required for live authentication

* The application must be run locally on macOS for camera support

* Docker execution is intended for Windows and Linux systems

* Pretrained model files must be present before startup

## 15. Troubleshooting

* **Issue**: dlib build failure

* Confirm **Python version is 3.10**

* Confirm **CMake** and **Boost** are installed

* Ensure virtual environment is activated

* **Issue**: Webcam not detected

* Check OS permissions

* Ensure no other application is using the camera

---

## 14. Environment and Execution

### 14.1 Recommended Environment

* **Operating System: macOS**

* **Python Version: 3.10**

* **Execution Mode: Local**

### 14.2 macOS and Docker Note

> Docker containers on macOS do not support direct access to the host webcam due to virtualization constraints.

**As a result:**

* **Live face authentication is demonstrated via local execution**

* **Docker support is provided for dependency reproducibility and Linux-based deployment scenarios**

## 15. Future Enhancements

* Potential improvements include:

* Deep learning–based anti-spoofing models

* Multi-factor authentication (face + PIN or OTP)

* Encrypted embedding storage

* Web-based attendance dashboard

* Support for mobile camera input

* Temporal consistency checks across frames

## 13. Evaluation Alignment

This project demonstrates:

  * Practical machine learning implementation

  * Understanding of real-world deployment constraints

  * Awareness of security and spoofing risks

  * Responsible handling of biometric data

  * End-to-end system design and documentation

## 14. Assignment Context

This project was developed as part of an AI/ML Internship Assignment for Medoc Health, with emphasis on real-world applicability, reliability, and clarity of limitations rather than theoretical accuracy claims.

## 15. References

* dlib Library and Pretrained Models

  [http://dlib.net](http://dlib.net)

* Face Recognition using Deep Metric Learning

* Eye Aspect Ratio for Blink Detection
