from typing import Optional, List
from pydantic import BaseModel


class PreviousChatContent(BaseModel):
    sender: str
    receiver: str
    chatContent: str
    chatDay: int

class ConversationUserSchema(BaseModel):
    sender: str
    receiver: str
    chatContent: str
    chatDay: int
    previousStory: Optional[str] = None
    previousChatContents: List[PreviousChatContent]

class ConversationNPCSchema(BaseModel):
    sender: str
    npcName1: str
    npcName2: str
    chatDay: int
    previousStory: Optional[str]