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

# class ChatSaveRequestSchema(BaseModel):
#     chatSaveRequest: ConversationUserSchema

class ConversationNPCSchema(BaseModel):
    npc_name_1: str
    npc_name_2: str

class MakingNPCSchema(BaseModel):
    npc_number: int