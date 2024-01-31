from fastapi import APIRouter, HTTPException

from domain.user import user_crud
from domain.user.schema import user_router_schema
from LLMs.langchain import chatbot

from lib.chat_management import previous_chat_contents

router = APIRouter(
    prefix="/api/user",
)


@router.post("/conversation_with_user", 
             description="npc와 user간의 대화를 위한 API입니다.", 
            #  response_model=user_router_schema.ConversationUserOutput, 
             tags=["user"])
async def conversation_with_user(conversation_user_schema: user_router_schema.ConversationUserInput):
    # print(conversation_user_schema.model_dump_json(indent=2))

    if not user_crud.get_character_info(conversation_user_schema.receiver.name):
        raise HTTPException(status_code=404, detail="Receiver not found in the character list.")
    
    input_data_json, input_data_pydantic = user_crud.conversation_with_user_input(conversation_user_schema)

    print(input_data_pydantic)
                
    answer, tokens, execution_time = chatbot.conversation_with_user(input_data_pydantic)

    final_response = {
        "answer": answer, 
        "tokens": tokens
    }

    print(f"chatContent : {answer}\ntokens : {tokens}\nexecution_time : {execution_time}")
    return final_response


# @router.post("/conversation_between_npcs", 
#              description="npc와 npc간의 대화를 생성해 주는 API입니다.", 
#              tags=["user"])
# async def conversation_between_npc(conversation_npc_schema: ConversationNPCSchema):
#     print(f"input")
#     print(f"npc_name_1 : {conversation_npc_schema.npcName1}")
#     print(f"npc_name_2 : {conversation_npc_schema.npcName2}")
#     # chatDay, previousStory 이용 안함

#     npc_1, npc_name_1 = get_npc_information(conversation_npc_schema.npcName1, random_=False)
#     npc_2, npc_name_2 = get_npc_information(conversation_npc_schema.npcName2, random_=False)
#     if not npc_1:
#         raise HTTPException(status_code=400, detail=f"{conversation_npc_schema.npcName1} is not in npc list!")
#     if not npc_2:
#         raise HTTPException(status_code=400, detail=f"{conversation_npc_schema.npcName2} is not in npc list!")

#     prompt = f" target_npc_1: ({npc_1})\n" \
#                 + f" target_npc_2: ({npc_2})\n" \
#                 + f"{npc_name_1}: " \
    
#     answer, tokens, execution_time = chatbot.conversation_between_npc(prompt, conversation_npc_schema.npcName1, conversation_npc_schema.npcName2)

#     final_response = {
#         "chatContent": answer, 
#         "tokens": tokens
#     }

#     print(f"chatContent : {answer}\ntokens : {tokens}\nexecution_time : {execution_time}")
#     return final_response


# @router.post("/conversation_between_npcs_stepwise", 
#              description="npc와 npc간의 대화를 하나씩 생성해 주는 API입니다.", 
#              tags=["user"])
# async def conversation_between_npc(conversation_npc_schema: ConversationNPCSchema2):
#     print(f"input")
#     print(f"npc_name_1 : {conversation_npc_schema.npcName1}")
#     print(f"npc_name_2 : {conversation_npc_schema.npcName2}")
#     # chatDay, previousStory 이용 안함

#     npc_1, npc_name_1 = get_npc_information(conversation_npc_schema.npcName1, random_=False)
#     npc_2, npc_name_2 = get_npc_information(conversation_npc_schema.npcName2, random_=False)
#     if not npc_1:
#         raise HTTPException(status_code=400, detail=f"{conversation_npc_schema.npcName1} is not in npc list!")
#     if not npc_2:
#         raise HTTPException(status_code=400, detail=f"{conversation_npc_schema.npcName2} is not in npc list!")

#     prompt = f" target_npc_1: ({npc_1})\n" \
#                 + f" target_npc_2: ({npc_2})\n" \
#                 + f"\n대화 내용: \n" \
#                 + f"{npc_name_1}: " \
                
#     print(prompt)
    
#     answer, tokens, execution_time = chatbot.conversation_between_npcs_stepwise(prompt)
#     print(answer)
#     print(tokens)

    # final_response = {
    #     "chatContent": answer, 
    #     "tokens": tokens
    # }

    # print(f"chatContent : {answer}\ntokens : {tokens}\nexecution_time : {execution_time}")
    # return final_response