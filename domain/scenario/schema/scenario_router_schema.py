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
class GenerateIntroInput(GenerateInput):
    characters: List

class GenerateVictimInput(GenerateInput):
    day: int
    murderer: str
    livingCharacters: List
    previousStory: Optional[str]

class GenerateFinalWordsInput(GenerateInput):
    gameResult: str = "victory"
    murderer: str
    livingCharacters: List
    previousStory: Optional[str]


# router output
class Alibis(BaseModel):
    name: str
    alibi: str

class VictimAnswer(BaseModel):
    victim: str
    crimeScene: str
    method: str
    witness: str
    eyewitnessInformation: str
    dailySummary: str
    alibis: List[Alibis]

class IntroAnswer(BaseModel):
    greeting: str
    content: str
    closing: str

class FinalWordsAnswer(BaseModel):
    finalWords: str

class GenerateIntroOutput(GenerateOutput):
    answer: IntroAnswer

class GenerateVictimOutput(GenerateOutput):
    answer: VictimAnswer

class GenerateFinalWordsOutput(GenerateOutput):
    answer: FinalWordsAnswer