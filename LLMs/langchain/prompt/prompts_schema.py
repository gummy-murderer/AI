from langchain_core.pydantic_v1 import BaseModel, Field
from typing import List, Optional


class IntroSchema(BaseModel):
    greeting: str
    content: str
    closing: str

class AlibisSchema(BaseModel):
    name: str
    alibi: str

class GenerateVictimSchema(BaseModel):
    eyewitnessInformation: str
    dailySummary: str
    alibis: List[AlibisSchema]

class FinalWordsSchema(BaseModel):
    finalWords: str