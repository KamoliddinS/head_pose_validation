from fastapi import FastAPI
from fastapi import File, UploadFile
from PIL import Image, ImageDraw
from io import BytesIO
import numpy as np
from fastapi.responses import Response
from service.head_pose_analysis import analyze_nose_angle_draw_bounding_box
from fastapi.openapi.utils import get_openapi
from starlette.responses import RedirectResponse, JSONResponse
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security.api_key import APIKeyQuery, APIKeyCookie, APIKeyHeader, APIKey
from service.utils import get_api_key, get_admin_api_key
from celery import Celery, Task
from service.celery_task_app.tasks import  analyze_face_emotions_and_straightness
from service.schemas import Face_url
from typing import Optional, List
import datetime
import tensorflow as tf
print("Num GPUs Available: ", len(tf.config.list_physical_devices('GPU')))

app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)
origins = ["*"]
methods = ["*"]
headers = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=methods,
    allow_headers=headers
)


@app.get("/")
async def homepage():
    return "Welcome to the DeepFace API."


@app.get("/openapi.json", tags=["documentation"])
async def get_open_api_endpoint():
    response = JSONResponse(
        get_openapi(title="Face authentication and search API for kindergarten kids in Uzbekistan",
                    description="This Application is optimized for searching faces, and For precise searches Please Search faces with raidus option enabled",
                    version=1, routes=app.routes)
    )
    return response


@app.get("/docs", tags=["documentation"])
async def get_documentation():
    response = get_swagger_ui_html(openapi_url="/openapi.json", title="docs")
    return response


def get_image_buffer(image: Image.Image, format: str = "PNG") -> bytes:
    buffered = BytesIO()
    image.save(buffered, format=format)
    img_bytes = buffered.getvalue()
    return img_bytes


@app.post("/analyze_face_emotions_and_straightness_test", tags=["face_emotions_and_straightness"])
async def draw_bonding_box(file: UploadFile = File(...)):
    # get image high and width
    image_array = np.array(Image.open(BytesIO(await file.read())))
    image_array, emotion = analyze_nose_angle_draw_bounding_box(image_array)
    image = Image.fromarray(image_array)
    image_bytes = get_image_buffer(image)
    return Response(content=image_bytes, media_type="image/png")


@app.post("/analyze_face_emotions_and_straightness", tags=["face_emotions_and_straightness"])
async def draw_bonding_box(face_url: Face_url):
    # get image high and width
    task = analyze_face_emotions_and_straightness.delay(face_url.face_url)
    return {"task_id": task.id}

@app.get("/analyze_face_emotions_and_straightness/{task_id}", tags=["face_emotions_and_straightness"])
async def get_task_result(task_id: str):
    task = analyze_face_emotions_and_straightness.AsyncResult(task_id)
    if task.state == 'SUCCESS':
        return task.result
    else:
        return {'state': task.state}