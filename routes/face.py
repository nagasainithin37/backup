from fastapi import APIRouter
from fastapi.responses import JSONResponse
from config.database import otpCollection,usersCollection,imageCollection
import sys, numpy, os
import urllib
import numpy as np
import time
from subprocess import call
import glob
import base64
import random
import cv2
import face_recognition
import base64
from PIL import Image
from io import BytesIO
# from twilio.rest import Client
face = APIRouter()

@face.post('/face-verify')
async def verify_face(acc_id : str):
    try:
        user=usersCollection.find_one({"accountno":acc_id})
        print(user)
        if user==None:
            return JSONResponse(content={
                "message":"No user found",
                "status":"success",
                "isError":False
            })
        imgObj=imageCollection.find_one({"accountno":acc_id})
        image_bytes = base64.b64decode(imgObj['image'])
        image = Image.open(BytesIO(image_bytes))
        image.save("routes/images/"+acc_id+".jpg")
        video_capture = cv2.VideoCapture(0)
        imgPath="routes/images/"+acc_id+".JPG"
        input1 = face_recognition.load_image_file(imgPath)
        if os.path.exists(imgPath):
            os.remove(imgPath)
        nithin_face_encoding = face_recognition.face_encodings(input1)[0]
        known_face_encodings = [
            nithin_face_encoding,
        ]
        known_face_names = [
            user['name'],
        ]
        face_locations = []
        face_encodings = []
        face_names = []
        process_this_frame = True
        isRecognised=False
        while True:
            # Grab a single frame of video
            ret, frame = video_capture.read()
            cv2.imshow("resized output",frame)
            # Resize frame of video to 1/4 size for faster face recognition processing
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            rgb_small_frame = numpy.ascontiguousarray(small_frame[:, :, ::-1])
            # Only process every other frame of video to save time
            if process_this_frame:
                # Find all the faces and face encodings in the current frame of video
                face_locations = face_recognition.face_locations(rgb_small_frame)
                face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
                face_names = []
                for face_encoding in face_encodings:
                    # See if the face is a match for the known face(s)
                    matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                    name = "Unknown"
                    face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]:
                        name = known_face_names[best_match_index]
                    face_names.append(name)
            process_this_frame = not process_this_frame
            if face_names==known_face_names:
                print("you are allowed")
                # face_names[0]=user['name']
                isRecognised=True
            else:
                print('unknown')
                isRecognised=False
                # face_names[0]="Not "+user['name']
                print("you are not allowed")
            # Display the results
            for (top, right, bottom, left), name in zip(face_locations, face_names):
                # Scale back up face locations since the frame we detected in was scaled to 1/4 size
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4
                # Draw a box around the face
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                # Draw a label with a name below the face
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
            # Display the resulting image
            cv2.imshow('output videoVideo', frame)
            # Hit 'q' on the keyboard to quit!
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        # Release handle to the webcam
        video_capture.release()
        cv2.destroyAllWindows()
        return JSONResponse(content={
                "message":isRecognised,
                "status":"success",
                "isError":False
            })
    except Exception as e:
            return JSONResponse(content={
                "message":str(e),
                "status":"failure",
                "isError":True
            })

