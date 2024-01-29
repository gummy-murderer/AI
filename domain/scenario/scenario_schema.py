from typing import List, Optional
from pydantic import BaseModel

# router schema
class GenerateSchema(BaseModel):
    gameNo: Optional[int]
    secretKey: Optional[str]

class GenerateVictimSchema(GenerateSchema):
    day: int
    murderer: str
    livingCharacters: List
    previousStory: Optional[str]


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
    victim: str
    witness: str
    livingCharacters: List[CharacterInfo]

class GameScenarioContainer(BaseModel):
    information: GameScenario