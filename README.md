# Face Recognition System

This project is a real-time face recognition and attendance tracking system using OpenCV, Streamlit, and Python. It captures face data, stores it, and uses a K-Nearest Neighbors (KNN) classifier for recognition.

## Prerequisites
Ensure you have Python installed. You can check your Python version with:
```sh
python --version
```
If not installed, download it from [python.org](https://www.python.org/).

## Installation
1. **Clone the Repository**
```sh
git clone https://github.com/GURUJANARDHANREDDY/face-recognition.git
cd face-recognition
```

2. **Install Dependencies**
```sh
pip install -r requirements.txt
```

3. **Download Haarcascade File**
Ensure the `haarcascade_frontalface_default.xml` file is present in the project directory. If missing, download it from [OpenCV GitHub](https://github.com/opencv/opencv/tree/master/data/haarcascades) and place it in the project folder.

## Usage
### 1. **Add Faces**
To register a new face:
```sh
python add_faces.py
```
Follow the on-screen instructions to capture your face data.

### 2. **Recognize Faces and Track Attendance**
Run the recognition script:
```sh
python recognize_faces.py
```
This will match detected faces against the stored dataset and mark attendance.

## Troubleshooting
### **1. OpenCV Error: Can't open haarcascade_frontalface_default.xml**
- Ensure the file exists in the directory.
- Try running with an absolute path:
  ```sh
  python add_faces.py --cascade "C:\Users\reddy\Downloads\IDBMS PROJECT\face_recognition\haarcascade_frontalface_default.xml"
  ```

### **2. ModuleNotFoundError: No module named 'cv2'**
- Install OpenCV:
  ```sh
  pip install opencv-python
  ```

### **3. Permission Denied or File Not Found**
- Run the script as administrator.
- Verify correct directory paths.


