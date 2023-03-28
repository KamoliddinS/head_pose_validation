import logging
from  .worker import  app
from celery import Task
from deepface import DeepFace
from service.schemas import Face_url

import cv2
import gc
gc.enable()

# class PredictTask(Task):
#
#     abstract = True
#     def __init__(self):
#         self.model = None
#
#     def __call__(self, *args, **kwargs):
#
#         if not self.model:
#             self.model  = Facenet.loadModel()
#         return self.run(*args, **kwargs)

@app.task(bind=True, name="analyze_face_emotions_and_straightness", ignore_result=False, max_retries=5, default_retry_delay=100)
def analyze_face_emotions_and_straightness(self, face_url: Face_url):
    try:
        logging.info("analyze_face_emotions_and_straightness: kid_id: %s, image_url: %s, call_back_url: %s, call_back_image_url: %s", kid_id, image_url, call_back_url, call_back_image_url)
        image = cv2.imread(image_url)
        bgr_image_array = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    except Exception as e:
        logging.exception("analyze_face_emotions_and_straightness.couldn't get image from url:image_url: %s.", image_url)
        raise self.retry(exc=e, countdown=10)
