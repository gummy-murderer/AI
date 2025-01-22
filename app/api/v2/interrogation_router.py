from fastapi import APIRouter, Request, HTTPException

from app.services.game_service import GameService
from app.schemas.interrogation import (
    NewInterRequest, 
    NewInterResponse, 
    SubmitEvidenceRequest, 
    SubmitEvidenceResponse, 
    ConversationRequest, 
    ConversationResponse
    )

router = APIRouter(
    prefix="/api/v2/interrogation",
    tags=["INTERROGATION"]
)
from pydantic import BaseModel

class NewInterRequest(BaseModel):
    gameNo: int
    npcName: str = "박동식"
    murderWeapon: str = "뿅망치"
    murderLocation: str = "잡화샵"
    murderTime: str = "아침 6시"

class NewInterResponse(BaseModel):
    message: str

class ConversationRequest(BaseModel):
    gameNo: int
    npcName: str = "박동식"
    content: str

class ConversationResponse(BaseModel):
    response: str
    heartRate: int

@router.post("/new", 
             description="새로운 취조를 시작하는 API 입니다.",
            #  response_model=NewInterResponse
            )
async def new_interrogation(request: Request, input: NewInterRequest):
    game_service: GameService = request.app.state.game_service
    data = {
        "murder_weapon": input.murderWeapon ,
        "murder_location": input.murderLocation, 
        "murder_time": input.murderTime
    }
    response = game_service.new_interrogation(input.gameNo, input.npcName, data)

    # return {"message": "New interrogation started"}
    return response

@router.post("/conversation", 
             description="취조에서 자유대화하는 API 입니다.",
             response_model=ConversationResponse
            )
async def interrogation(request: Request, input: ConversationRequest):
    game_service: GameService = request.app.state.game_service
    response = game_service.generation_interrogation_response(input.gameNo, input.npcName, input.content)
    # try:
    # except TypeError as e:
    #     raise HTTPException(status_code=404, detail=f"interrogation not found: {e}")
    return response