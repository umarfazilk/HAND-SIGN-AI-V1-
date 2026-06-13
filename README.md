# HAND SIGN AI V1

**Hand Sign AI V1** is an AI-based computer vision project that detects hand signs through a webcam and converts them into readable text or voice output. The main goal of this project is to support communication for people with speech or hearing difficulties by recognizing hand gestures in real time.

---

## Project Overview

This project uses a webcam to capture hand gestures, processes the hand landmarks using computer vision, and predicts the corresponding sign using a machine learning model. The recognized sign can be displayed as text and can also be converted into speech output.

---

## Problem Statement

Many people with speech or hearing disabilities use hand signs to communicate. However, not everyone understands sign language. This creates a communication gap between sign language users and the general public.

This project aims to reduce that gap by building an AI system that can recognize hand signs and convert them into understandable text or speech.

---

## Features

* Real-time hand sign detection using webcam
* Hand landmark tracking
* AI-based gesture recognition
* Text output for detected signs
* Voice output support
* Simple and beginner-friendly project structure
* Useful for accessibility and assistive technology applications

---

## Technologies Used

* Python
* OpenCV
* MediaPipe
* Machine Learning
* NumPy
* Text-to-Speech
* Webcam-based Computer Vision

---

## Project Workflow

1. Capture live video from webcam
2. Detect hand using computer vision
3. Extract hand landmarks
4. Process landmark data
5. Predict the hand sign using trained model
6. Display the predicted sign as text
7. Convert the detected text into speech output

---

## Folder Structure

```text
HAND-SIGN-AI-V1/
│
├── README.md
├── requirements.txt
├── main.py
│
├── src/
│   ├── hand_detector.py
│   ├── gesture_recognition.py
│   └── text_to_speech.py
│
├── model/
│   └── model_info.txt
│
├── assets/
│   ├── demo_image.png
│   └── output_screenshot.png
│
└── docs/
    └── project_report.pdf
```

---

## How to Run the Project

### 1. Clone the Repository

```bash
git clone https://github.com/umarfazilk/HAND-SIGN-AI-V1-.git
```

### 2. Go to the Project Folder

```bash
cd HAND-SIGN-AI-V1-
```

### 3. Install Required Libraries

```bash
pip install -r requirements.txt
```

### 4. Run the Project

```bash
python main.py
```

---

## Requirements

Create a `requirements.txt` file and add:

```text
opencv-python
mediapipe
numpy
pyttsx3
scikit-learn
```

---

## Applications

* Assistive communication system
* Sign language learning support
* Human-computer interaction
* AI-based accessibility tool
* Smart classroom support system
* Healthcare and rehabilitation assistance

---

## Future Improvements

* Add support for more hand signs
* Improve model accuracy
* Add sentence formation from multiple signs
* Build a web dashboard
* Add mobile app support
* Support regional sign language datasets
* Improve real-time performance
* Add multilingual voice output

---

## Project Status

This is Version 1 of the project. The current focus is on basic real-time hand sign detection and output conversion.

---

## Author

**Umar Fazil K**
Electronics and Communication Engineering
Madras Institute of Technology, Anna University

GitHub: [umarfazilk](https://github.com/umarfazilk)
LinkedIn: [linkedin.com/in/umarfazilk](https://linkedin.com/in/umarfazilk)

---

## License

This project is created for learning, research, and educational purposes.
