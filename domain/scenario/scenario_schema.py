from typing import List, Optional
from pydantic import BaseModel

# router schema
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


class GenerateIntroInput(BaseModel):
    characters: List

class GenerateVictimInput(GenerateInput):
    day: int
    murderer: str
    livingCharacters: List
    previousStory: Optional[str]

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

class GenerateIntroOutput(GenerateOutput):
    answer: IntroAnswer

class GenerateVictimOutput(GenerateOutput):
    answer: VictimAnswer


# characters information schema
class CriminalScenarioSchema(BaseModel):
    motivation: str
    procedure: str

class CharacterSchema(BaseModel):
    name: str
    age: int
    gender: str
    wealth: str
    personality: str
    personalityDescription: str
    feature: str
    featureDescription: str
    criminalScenario: CriminalScenarioSchema

class CharactersSchema(BaseModel):
    npcs: List[CharacterSchema]


# places schema
class PlaceName(BaseModel):
    placeNameEn: str
    placeNameKo: str

class PlacesSchema(BaseModel):
    places: List[PlaceName]


# generate_victim input schema
class BaseGameSchema(BaseModel):
    gameNo: Optional[int]
    secretKey: Optional[str]

class VictimGenerationSchema(BaseGameSchema):
    day: int
    murderer: str
    livingCharacters: List
    previousStory: Optional[str]


# prompt input schema
class MurdererInfo(BaseModel):
    name: str
    motivation: str
    procedure: str

class CharacterInfo(BaseModel):
    name: str
    # personality: str
    personalityDescription: str
    # feature: str
    featureDescription: str

class GameScenario(BaseModel):
    day: int
    murderer: MurdererInfo
    crimeScene: str
    method: str
    victim: str
    witness: str
    livingCharacters: List[CharacterInfo]
    previousStory: str

class GameScenarioContainer(BaseModel):
    information: GameScenario