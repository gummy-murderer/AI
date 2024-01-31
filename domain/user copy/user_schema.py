from typing import Optional, List
from pydantic import BaseModel


class GenerateSchema(BaseModel):
    gameNo: Optional[int]
    secretKey: Optional[str]
    
class PreviousChatContent(BaseModel):
    sender: str
    receiver: str
    chatContent: str
    chatDay: int

class ConversationUserSchema(GenerateSchema):
    sender: str
    receiver: str
    chatContent: str
    chatDay: int
    previousStory: Optional[str] = None
    previousChatContents: List[PreviousChatContent]

class ConversationNPCSchema(GenerateSchema):
    sender: str
    npcName1: str
    npcName2: str
    chatDay: int
    previousStory: Optional[str]

class ConversationNPCSchema2(ConversationNPCSchema):
    previousChatContents: List[PreviousChatContent]