from typing import Optional
from datetime import datetime

from pydantic import BaseModel


class GeneratorSchema(BaseModel):
    content: str


class ConversationUserSchema(BaseModel):
    content: str
    npc_name : str


class ConversationNPCSchema(BaseModel):
    npc_name_1 : str
    npc_name_2 : str