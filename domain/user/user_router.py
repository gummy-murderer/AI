from fastapi import APIRouter, HTTPException

from domain.user import user_crud
from domain.user.schema import user_router_schema
from LLMs.langchain import chatbot


router = APIRouter(
    prefix="/api/user",
)


@router.post("/conversation_with_user", 
             description="npc와 user간의 대화를 위한 API입니다.", 
             response_model=user_router_schema.ConversationUserOutput, 
             tags=["user"])
async def conversation_with_user(conversation_user_schema: user_router_schema.ConversationUserInput):
    print(conversation_user_schema.model_dump_json(indent=2))

    if not user_crud.get_character_info(conversation_user_schema.receiver.name):
        raise HTTPException(status_code=404, detail="Receiver not found in the character list.")
    
    input_data_json, input_data_pydantic = user_crud.conversation_with_user_input(conversation_user_schema)
                
    answer, tokens, execution_time = chatbot.conversation_with_user(input_data_pydantic)

    final_response = {
        "answer": answer, 
        "tokens": tokens
    }
    print(f"chatContent : {answer}\ntokens : {tokens}\nexecution_time : {execution_time}")
    return final_response


@router.post("/conversation_between_npcs", 
             description="npc와 npc간의 대화를 생성해 주는 API입니다.", 
             response_model=user_router_schema.ConversationNPCOutput, 
             tags=["user"])
async def conversation_between_npc(conversation_npc_schema: user_router_schema.ConversationNPCInput):
    print(conversation_npc_schema.model_dump_json(indent=2))
    # chatDay, previousStory 이용 안함

    if not user_crud.get_character_info(conversation_npc_schema.npcName1.name):
        raise HTTPException(status_code=404, detail="npcName1 not found in the character list.")
    if not user_crud.get_character_info(conversation_npc_schema.npcName2.name):
        raise HTTPException(status_code=404, detail="npcName2 not found in the character list.")
    
    input_data_json, input_data_pydantic = user_crud.conversation_between_npc_input(conversation_npc_schema)
    
    answer, tokens, execution_time = chatbot.conversation_between_npc(input_data_pydantic)

    final_response = {
        "answer": answer, 
        "tokens": tokens
    }
    print(f"chatContent : {answer}\ntokens : {tokens}\nexecution_time : {execution_time}")
    return final_response