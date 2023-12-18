from typing import Optional
from datetime import datetime

from pydantic import BaseModel

class ChatbotSchema(BaseModel):
    island_id: str
    user_id: str
    content: str
    datetime: Optional[str] = str(datetime.now())