from pydantic import BaseModel
from typing import List, Dict

class NPC(BaseModel):
    name: str
    personality: str
    is_alive: bool = True
    alibi: str = None
    preferredTimes: List[str] = []

class Location(BaseModel):
    name: str
    description: str
    clues: List[str] = []

class Item(BaseModel):
    name: str
    description: str
    related_to: str = None

class GameState(BaseModel):
    npcs: List[NPC]
    locations: List[Location]
    items: List[Item]
    murderer: NPC
    days_passed: int
    conversations_left: int
    game_over: bool
    current_questions: List[str] = []
    user_language: str = "en"
    murder_times: List[str] = []

class NPCInfo(BaseModel):
    npcName: str  # NPC ID (영어, 예: "KimKoongYa", "Theo", "Sophia")
    npcJob: str

class GameStartRequest(BaseModel):
    gameNo: int = 0
    language: str = "ko"
    characters: List[NPCInfo] = [
    {
        "npcName": "KimKoongYa",
        "npcJob": "Resident"
    },
    {
        "npcName": "ParkDongSik",
        "npcJob": "Resident"
    },
    {
        "npcName": "ZzanZzanYoung",
        "npcJob": "Murderer"
    },
    {
        "npcName": "TaeGeunTV",
        "npcJob": "Resident"
    },
    {
        "npcName": "ParkYoonJu",
        "npcJob": "Resident"
    },
    {
        "npcName": "Theo",
        "npcJob": "Resident"
    },
    {
        "npcName": "Sophia",
        "npcJob": "Resident"
    },
    {
        "npcName": "Marco",
        "npcJob": "Resident"
    },
    {
        "npcName": "Alex",
        "npcJob": "Resident"
    }
]

class GameRequest(BaseModel):
    gameNo: int
    language: str = "ko"

class QuestionRequest(BaseModel):
    gameNo: int
    language: str = "ko"
    npcName: str  # NPC ID (영어, 예: "KimKoongYa", "Theo", "Sophia")
    keyWord: str
    keyWordType: str = "weapon"

class AnswerRequest(BaseModel):
    gameNo: int
    language: str = "ko"
    npcName: str  # NPC ID (영어, 예: "KimKoongYa", "Theo", "Sophia")
    keyWord: str
    keyWordType: str = "weapon"

class LivingNPCInfo(BaseModel):
    name: str  # NPC ID (영어, 예: "KimKoongYa", "Theo", "Sophia")
    job: str
    status: str

class NextDayRequest(BaseModel):
    gameNo: int = 0
    language: str = "ko"
    livingCharacters: List[LivingNPCInfo] = [
        {
            "name": "KimKoongYa",
            "job": "Resident",
            "status": "Alive"
        },
        {
            "name": "ParkDongSik",
            "job": "Resident",
            "status": "Alive"
        },
        {
            "name": "ZzanZzanYoung",
            "job": "Murderer",
            "status": "Alive"
        },
        {
            "name": "TaeGeunTV",
            "job": "Resident",
            "status": "Dead"
        },
        {
            "name": "ParkYoonJu",
            "job": "Resident",
            "status": "Alive"
        },
        {
            "name": "Theo",
            "job": "Resident",
            "status": "Dead"
        },
        {
            "name": "Sophia",
            "job": "Resident",
            "status": "Alive"
        },
        {
            "name": "Marco",
            "job": "Resident",
            "status": "Alive"
        },
        {
            "name": "Alex",
            "job": "Resident",
            "status": "Alive"
        }
    ]

class GameEndRequest(BaseModel):
    gameNo: int
    language: str = "ko"
    gameResult: str = "WIN"