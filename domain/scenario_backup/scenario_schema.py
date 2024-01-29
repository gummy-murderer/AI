from typing import Optional, List
from pydantic import BaseModel


class GenerateSchema(BaseModel):
    gameNo: Optional[int]
    secretKey: Optional[str]

class GenerateIntroSchema(GenerateSchema):
    Characters: List

class GenerateVictimSchema(GenerateSchema):
    day: int
    murderer: str
    livingCharacters: List
    previousStory: Optional[str]

class GenerateFinalWordsSchema(GenerateSchema):
    result: str = "victory"
    murderer: str
    livingCharacters: List
    previousStory: Optional[str]