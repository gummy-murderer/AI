from fastapi import APIRouter, HTTPException, Request

from app.schemas import game_schema 
from app.services.game_service import GameService


router = APIRouter(
    prefix="/api/v2/in-game",
    tags=["IN_GAME"]
)

# NPC에게 할 질문을 생성하는 라우터
@router.post("/generate-question", 
            description="NPC에게 할 질문을 생성하는 API 입니다.")
async def generate_question(request: Request, question_data: game_schema.QuestionRequest):
    game_service: GameService = request.app.state.game_service
    try:
        question = game_service.generate_npc_questions(
            question_data.gameNo, 
            question_data.npcName, 
            question_data.keyWord, 
            question_data.keyWordType
        )
        return {"question": question}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# NPC에게 한 질문에 대한 답을 생성하는 라우터
@router.post("/generate-answer", 
            description="NPC에게 한 질문에 대한 답을 생성하는 API 입니다.")
async def talk_to_npc(request: Request, answer_data: game_schema.AnswerRequest):
    game_service: GameService = request.app.state.game_service
    try:
        response = game_service.talk_to_npc(
            answer_data.gameNo, 
            answer_data.npcName, 
            answer_data.keyWord, 
            answer_data.keyWordType
        )
        return {"response": response}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))