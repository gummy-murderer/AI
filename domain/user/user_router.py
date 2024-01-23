from fastapi import APIRouter, HTTPException

from domain.user.user_schema import ConversationUserSchema, ConversationNPCSchema
from domain.user.user_crud import get_npc_information
from LLMs.langchain import chatbot

from lib.chat_management import previous_chat_contents

router = APIRouter(
    prefix="/api/user",
)


@router.post("/conversation_with_user", 
             description="npc와 user간의 대화를 위한 API입니다.", 
             tags=["user"])
async def conversation_with_user(conversation_user_schema: ConversationUserSchema):
    print(f"input")
    print(f"sender : {conversation_user_schema.sender}")
    print(f"receiver : {conversation_user_schema.receiver}")
    print(f"chatContent : {conversation_user_schema.chatContent}")
    print(f"chatDay : {conversation_user_schema.chatDay}")
    # previousChatContents.chatDay 이용 안함

    previous_contents = previous_chat_contents(conversation_user_schema.previousChatContents)
    print(f"previous_contents")
    print(f"{previous_contents}")
    
    info, name = get_npc_information(conversation_user_schema.receiver, random_=False)
    if not info:
        raise HTTPException(status_code=400, detail=f"{conversation_user_schema.receiver} is not in npc list!")

    prompt = f" target_npc_info: ({info})\n" \
                + f"대화내용: \n" \
                + f"{previous_contents}\n" \
                + f"{conversation_user_schema.sender}: {conversation_user_schema.chatContent}\n" \
                + f"{name}: " \
                
    answer, tokens, execution_time = chatbot.conversation_with_user(prompt)

    final_response = {
        "chatContent": answer, 
        "tokens": tokens
    }

    print(f"chatContent : {answer}\ntokens : {tokens}\nexecution_time : {execution_time}")
    return final_response


@router.post("/conversation_between_npcs", 
             description="npc와 npc간의 대화를 생성해 주는 API입니다.", 
             tags=["user"])
async def conversation_between_npc(conversation_npc_schema: ConversationNPCSchema):
    print(f"input")
    print(f"npc_name_1 : {conversation_npc_schema.npcName1}")
    print(f"npc_name_2 : {conversation_npc_schema.npcName2}")
    # chatDay, previousStory 이용 안함

    npc_1, npc_name_1 = get_npc_information(conversation_npc_schema.npcName1, random_=False)
    npc_2, npc_name_2 = get_npc_information(conversation_npc_schema.npcName2, random_=False)
    if not npc_1:
        raise HTTPException(status_code=400, detail=f"{conversation_npc_schema.npcName1} is not in npc list!")
    if not npc_2:
        raise HTTPException(status_code=400, detail=f"{conversation_npc_schema.npcName2} is not in npc list!")

    prompt = f" target_npc_1: ({npc_1})\n" \
                + f" target_npc_2: ({npc_2})\n" \
                + f"{npc_name_1}: " \
    
    answer, tokens, execution_time = chatbot.conversation_between_npc(prompt, conversation_npc_schema.npcName1, conversation_npc_schema.npcName2)

    final_response = {
        "chatContent": answer, 
        "tokens": tokens
    }

    print(f"chatContent : {answer}\ntokens : {tokens}\nexecution_time : {execution_time}")
    return final_response