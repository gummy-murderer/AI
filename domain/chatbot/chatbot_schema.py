from typing import Optional
from datetime import datetime

from pydantic import BaseModel

class ChatbotSchema(BaseModel):
    content: str