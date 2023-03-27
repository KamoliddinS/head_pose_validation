from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel
from deepface import DeepFace
from fastapi import File, UploadFile
import numpy as np
from PIL import Image, ImageDraw
from io import BytesIO
from service.mark_detector import MarkDetector
from service.pose_estimator import PoseEstimator
from fastapi.responses import Response

import cv2

app = FastAPI()

# model = DeepFace.build_model("DeepFace")


def read_imagefile(data) -> Image.Image:
    image = Image.open(BytesIO(data))
    return image


# free gpu memory
import tensorflow as tf

tf.keras.backend.clear_session()

app.get("/")


def read_root():
    return {"Hello": "World"}


# @app.post("/predict")
# async def estimate_emotion(image: UploadFile = File(...)):
#     try:
#         image = read_imagefile(await image.read())
#     except:
#         return {"error": "image not found"}
#     image = np.array(image)[:, :, ::-1].copy()
#     return DeepFace.analyze(image, actions=['emotion'])
#
def get_image_buffer(image: Image.Image, format: str = "PNG") -> bytes:
    buffered = BytesIO()
    image.save(buffered, format=format)
    img_bytes = buffered.getvalue()
    return img_bytes


@app.post("/predict2")
async def draw_bonding_box(file: UploadFile = File(...)):
    # get image high and width
    image = Image.open(BytesIO(await file.read()))
    image_array = np.array(image)
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
    face_img= image_array[y1:y2, x1:x2]

    marks = mark_detector.detect_marks(face_img)

    marks *= (x2 - x1)
    marks[:, 0] += x1
    marks[:, 1] += y1




    pose =pose_estimator.solve_pose_by_68_points(marks)

    pose_estimator.draw_annotation_box(image_array, pose[0], pose[1], color=(255, 128, 128))

    def test_face_if_it_is_straight(pose):
        return pose[0][0] > 0.1 or pose[0][0] < -0.1
    # print(test_face_is_between_acceptable_range(pose))

    #pose_estimator.draw_axes(image_array, pose[0], pose[1])
    image = Image.fromarray(image_array)
    image_bytes = get_image_buffer(image)
    return Response(content=image_bytes, media_type="image/png")
