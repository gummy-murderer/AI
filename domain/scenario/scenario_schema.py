from typing import Optional, List
from pydantic import BaseModel


class GeneratorSchema(BaseModel):
    content: str

class GenerateVictimSchema(BaseModel):
    day: int
    murderer: str
    livingCharacters: List
    previousStory: Optional[str]