#
# import logging
# from  .worker import  app
# from celery import Task
# from deepface.basemodels import Facenet
# from deepface.commons import functions
# from elasticsearch import Elasticsearch
# import gc
# from db.database import get_db
# gc.enable()
# # from ..main import client
# target_size = (160, 160)
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
#
# try:
#     client = get_db()
# except Exception as e:
#     print("Error while connecting to elasticsearch: ")
# @app.task(bind=True, base=PredictTask, name="add_image_to_index_task", ignore_result=False, max_retries=5, default_retry_delay=100)
# def add_image_to_index_task(self, alias: str, url: str, lat: float , lon: float):
#     try:
#         img = functions.preprocess_face(url, target_size=target_size, detector_backend='mtcnn')
#     except Exception as e:
#         raise self.retry(exc=e, countdown=1800)
#     embedding = self.model.predict(img)[0]
#     doc = {"embedding": embedding.tolist(), "kid_name": url,
#            "coordinate": {"lat": lat, "lon": lon}}
#     try:
#         result = client.index(index="face_recognition",
#                               id=alias, document=doc)
#     except Exception as e:
#         raise self.retry(exc=e, countdown=3600, max_retries=24)
#
#     #clear memory
#     del img
#     del embedding
#     del doc
#
#     gc.collect()
#
#
#     if result['result'] == 'updated':
#         return {"message": "updated", "alias": alias, "url": url}
#     if result['result'] == 'created':
#         return {"message": "created", "alias": alias, "url": url}
#     return {"message": "Image added to database", "alias": alias, "url": url}