from fastapi import APIRouter, Request

from app.services.game_service import GameService

router = APIRouter(
    prefix="/api/v2/interrogation",
    tags=["INTERROGATION"]
)
from pydantic import BaseModel

class NewInterRequest(BaseModel):
    gameNo: int
    language: str = "ko"
    npcName: str = "ParkDongSik"  # NPC ID (영어, 예: "KimKoongYa", "ParkDongSik")
    # murderWeapon: str
    # murderLocation: str
    murderWeapon: str = "Baby_Hammer"
    murderLocation: str = "UnderPig"
    murderTime: str = "Five"

class ConversationRequest(BaseModel):
    gameNo: int
    language: str = "ko"
    npcName: str = "ParkDongSik"  # NPC ID (영어, 예: "KimKoongYa", "ParkDongSik")
    content: str = "너가 범인이지! 난 다 알고 있어어"

class InterrogationResponse(BaseModel):
    npcName: str
    status: str
    isMurderer: bool
    heartRate: int
    response: str

@router.post("/new", 
             description="새로운 취조를 시작하는 API 입니다.",
             response_model=InterrogationResponse
            )
async def new_interrogation(request: Request, input: NewInterRequest):
    from fastapi import HTTPException
    if input.language not in ["en", "ko"]:
        raise HTTPException(status_code=400, detail="Invalid language. Choose 'en' or 'ko'.")
    print(input)
    game_service: GameService = request.app.state.game_service
    data = {
        "murder_weapon": input.murderWeapon ,
        "murder_location": input.murderLocation, 
        "murder_time": input.murderTime
    }
    return game_service.new_interrogation(input.gameNo, input.npcName, data, input.language)

@router.post("/conversation", 
             description="취조에서 자유 대화하는 API 입니다.",
             response_model=InterrogationResponse
            )
async def interrogation(request: Request, input: ConversationRequest):
    from fastapi import HTTPException
    if input.language not in ["en", "ko"]:
        raise HTTPException(status_code=400, detail="Invalid language. Choose 'en' or 'ko'.")
    game_service: GameService = request.app.state.game_service
    return game_service.generation_interrogation_response(input.gameNo, input.npcName, input.content, input.language)