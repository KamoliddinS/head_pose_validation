from pydantic import BaseModel
from typing import Union
from deepface import DeepFace
import numpy as np
from service.mark_detector import MarkDetector
from service.pose_estimator import PoseEstimator
import math
from PIL import Image, ImageDraw
from io import BytesIO

import cv2
def calcAngle(p1, p2):
    ang = None
    try:
        m = (p1[1] - p2[1])/(p1[0] - p2[0])
        ang = int(math.degrees(math.atan(-1/m)))
    except:
        ang = 90
    return ang

def read_imagefile(data) -> Image.Image:
    image = Image.open(BytesIO(data))
    return image

def analyze_nose_angle_draw_bounding_box(image_array):

    image_array = cv2.cvtColor(image_array, cv2.COLOR_BGR2RGB)
    height = image_array.shape[0]
    width = image_array.shape[1]
    pose_estimator = PoseEstimator(img_size=(height, width))
    mark_detector = MarkDetector()
    face_box = mark_detector.extract_cnn_facebox(image_array)
    x1, y1, x2, y2 = face_box
    # draw = ImageDraw.Draw(image)
    # draw = draw.rectangle(face_box, outline="red")
    #
    #
    # image_bytes = get_image_buffer(image)
    face_img = image_array[y1:y2, x1:x2]

    marks = mark_detector.detect_marks(face_img)

    marks *= (x2 - x1)
    marks[:, 0] += x1
    marks[:, 1] += y1
    shape = marks.astype(np.uint)

    # Draw Markers on face
    # mark_detector.draw_marks(img, marks, color=(0, 255, 0))
    image_points = np.array([
        shape[30],  # Nose tip
        shape[8],  # Chin
        shape[36],  # Left eye left corner
        shape[45],  # Right eye right corne
        shape[48],  # Left Mouth corner
        shape[54]  # Right mouth corner
    ], dtype="double")

    nose_points = np.array([
        shape[27],
        shape[28],
        shape[29],
        shape[30]
    ])
    p1 = (int(nose_points[0][0]), int(nose_points[0][1]))
    p2 = (int(nose_points[3][0]), int(nose_points[3][1]))

    cv2.line(image_array, p1, p2, (255, 255, 0), 2)
    ang = calcAngle(p1, p2)
    if ((ang <= 10 and ang >= -10) or ang == 90):
        cv2.putText(image_array, "face is straight", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
    else:
        cv2.putText(image_array, "face is not straight", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)
    pose = pose_estimator.solve_pose_by_68_points(marks)

    pose_estimator.draw_annotation_box(image_array, pose[0], pose[1], color=(255, 128, 128))
    emotion = DeepFace.analyze(image_array, actions=['emotion'], detector_backend='mtcnn')

    #put text emotion
    cv2.putText(image_array, emotion[0]['dominant_emotion'], (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

    #back to rgb
    image_array = cv2.cvtColor(image_array, cv2.COLOR_BGR2RGB)
    return image_array, emotion