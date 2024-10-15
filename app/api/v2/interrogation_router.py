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

@router.post("/new", 
             description="새로운 취조를 시작하는 API 입니다.",
             response_model=NewInterResponse
            )
async def new_interrogation(request: Request, input: NewInterRequest):
    try:
        game_service: GameService = request.app.state.game_service
        game_service.new_interrogation(input.game_no, input.npc_name)
        return {"message": "New interrogation started"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/submit",
             description="취조 증거품을 제출하는 API 입니다.\n type: weapon, time_of_death, location",
            #  response_model=SubmitEvidenceResponse
             )
async def submit_evidence(request: Request, input: SubmitEvidenceRequest):
    game_service: GameService = request.app.state.game_service
    return None


@router.post("/conversation", 
             description="취조에서 자유대화하는 API 입니다.",
             response_model=ConversationResponse
            )
async def interrogation(request: Request, input: ConversationRequest):
    game_service: GameService = request.app.state.game_service
    try:
        response = game_service.generation_interrogation_response(input.game_no, input.npc_name, input.content)
    except TypeError as e:
        raise HTTPException(status_code=404, detail=f"interrogation not found: {e}")
    return response