from typing import Optional, List, Dict
from datetime import datetime

from pydantic import BaseModel


class GeneratorSchema(BaseModel):
    content: str

class ConversationUserSchema(BaseModel):
    sender: str
    receiver: str
    chatContent: str
    chatDay: int
    previousChatContents: List[dict] 

class ConversationNPCSchema(BaseModel):
    npc_name_1: str
    npc_name_2: str

class GenerateVictimSchema(BaseModel):
    day: int
    murderer: str
    previousStory: Optional[str]