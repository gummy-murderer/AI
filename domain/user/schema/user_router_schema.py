from typing import List, Optional
from pydantic import BaseModel


class Tokens(BaseModel):
    totalTokens: int
    promptTokens: int
    completionTokens: int

class GenerateInput(BaseModel):
    gameNo: Optional[int]
    secretKey: Optional[str]

class GenerateOutput(BaseModel):
    tokens: Tokens

    class Config:
        arbitrary_types_allowed = True


# router input
class CharacterInfo(BaseModel):
    name: str
    alibi: str

class PreviousChatContent(BaseModel):
    sender: str
    receiver: str
    chatContent: str
    chatDay: int

class ConversationUserInput(GenerateInput):
    sender: str
    receiver: CharacterInfo
    chatContent: str
    chatDay: int
    previousStory: Optional[str] = None
    previousChatContents: List[PreviousChatContent]


# router output
class ConversationUserAnswer(BaseModel):
    chatContent: str

class ConversationUserOutput(GenerateOutput):
    answer: ConversationUserAnswer
