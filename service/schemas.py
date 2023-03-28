from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class Face_url(BaseModel):
    kid_id: int
    image_url: str
    call_back_url: str
    call_back_image_url: str