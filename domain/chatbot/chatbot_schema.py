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
    sender: str
    npcName1: str
    npcName2: str
    previousStory: Optional[str]

class GenerateVictimSchema(BaseModel):
    day: int
    murderer: str
    previousStory: Optional[str]