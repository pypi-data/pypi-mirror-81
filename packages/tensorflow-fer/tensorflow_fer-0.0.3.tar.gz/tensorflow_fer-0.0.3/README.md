### Project Description

    Facial Emotion Recognition using Tensorflow.

    It creates a bounding box around the face of the person present in the picture and put a text
    at the top of the bounding box representing the recognised emotion.

#



### Install

    pip install tensorflow-fer
    
#

### Requirements

    tensorflow-gpu>=2.0.0

    opencv-python

    numpy>=1.18.1
#

### Usage:

    from tensorflow_fer.emotion_recognition import EmotionRecognition
    
    import cv2 as cv
    
    er = EmotionRecognition()
    
    cam = cv.VideoCapture(0)
    
    success, frame = cam.read()
    
    frame = er.recognise(frame, return_type='BGR')
    
    cv.imshow('frame', frame)
    
    cv.waitkey(0)
    
#

### Arguments
    
    frame = er.recognise_emotion(frame, return_type='BGR')
    
    return_type='BGR' or 'RGB'
#

### References

1. "Challenges in Representation Learning: A report on three machine learning
contests." I Goodfellow, D Erhan, PL Carrier, A Courville, M Mirza, B
Hamner, W Cukierski, Y Tang, DH Lee, Y Zhou, C Ramaiah, F Feng, R Li,
X Wang, D Athanasakis, J Shawe-Taylor, M Milakov, J Park, R Ionescu,
M Popescu, C Grozea, J Bergstra, J Xie, L Romaszko, B Xu, Z Chuang, and
Y. Bengio. arXiv 2013.

#
