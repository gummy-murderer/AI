from fastapi import APIRouter, HTTPException

from domain.chatbot.chatbot_schema import GeneratorSchema, ConversationUserSchema, ConversationNPCSchema
from LLMs.langchain import chatbot, prompts

from lib.npc_management import get_npc_information
from lib.chat_management import previous_chat_contents


router = APIRouter(
    prefix="/api/chatbot",
)


@router.post("/intro_generator", 
             description="사용자 입력에 기반하여 소개 또는 시작 대화를 생성해 주는 API입니다.", 
             tags=["generator"])
async def intro_generator(generator_schema: GeneratorSchema):
    print(f"input : {generator_schema.content}")
    
    while True:
        try:
            answer = chatbot.intro(
                generator_schema.content
            )
            break
        except IndexError as e:
            print("#"*10 + "I got IndexError...Try again!" + "#"*10)

    final_response = {
        "answer": answer, 
    }
    print(f"answer : {answer}")
    return final_response


@router.post("/scenario_generator", 
             description="사용자 입력을 바탕으로 상세한 대화 시나리오를 생성해 주는 API입니다.", 
             tags=["generator"])
async def scenario_generator(generator_schema: GeneratorSchema):
    print(f"input : {generator_schema.content}")
    
    while True:
        try:
            answer = chatbot.scenario(
                generator_schema.content
            )
            break
        except IndexError as e:
            print("#"*10 + "I got IndexError...Try again!" + "#"*10)

    final_response = {
        "answer": answer, 
    }
    print(f"answer : {answer}")
    return final_response


@router.post("/conversation_with_user", 
             description="npc와 user간의 대화를 위한 API입니다.", 
             tags=["generator"])
async def conversation_with_user(conversation_user_schema: ConversationUserSchema):
    print(f"input")
    print(f"sender : {conversation_user_schema.sender}")
    print(f"receiver : {conversation_user_schema.receiver}")
    print(f"chatContent : {conversation_user_schema.chatContent}")
    print(f"chatDay : {conversation_user_schema.chatDay}")

    previous_contents = previous_chat_contents(conversation_user_schema.previousChatContents)
    print(f"previous_contents")
    print(f"{previous_contents}")
    
    info, name = get_npc_information(conversation_user_schema.receiver, random_=False)
    if not info:
        raise HTTPException(status_code=400, detail=f"{conversation_user_schema.receiver} is not in npc list!")
    print(info)

    while True:
        try:
            answer, tokens, execution_time = chatbot.conversation_with_user(
                f" target_npc_info: ({info})\n" \
                + f"대화내용: \n" \
                + f"{previous_contents}\n" \
                + f"{conversation_user_schema.sender}: {conversation_user_schema.chatContent}\n" \
                + f"{name}: " \
            )
            break
        except IndexError as e:
            print("#"*10 + "I got IndexError...Try again!" + "#"*10)

    final_response = {
        "chatContent": answer, 
        "totalTokens": tokens["Total_Tokens"]
    }
    print(f"chatContent : {answer}")
    print(f"tokens : {tokens}")
    print(f"execution_time : {execution_time}")
    return final_response


@router.post("/conversation_between_npcs", 
             description="npc와 npc간의 대화를 생성해 주는 API입니다.", 
             tags=["generator"])
async def conversation_between_npc(conversation_npc_schema: ConversationNPCSchema):
    print(f"input")
    print(f"npc_name_1 : {conversation_npc_schema.npc_name_1}")
    print(f"npc_name_2 : {conversation_npc_schema.npc_name_2}")

    npc_1, npc_name_1 = get_npc_information(conversation_npc_schema.npc_name_1, random_=False)
    npc_2, npc_name_2 = get_npc_information(conversation_npc_schema.npc_name_2, random_=False)
    if not npc_1:
        raise HTTPException(status_code=400, detail=f"{conversation_npc_schema.npc_name_1} is not in npc list!")
    if not npc_2:
        raise HTTPException(status_code=400, detail=f"{conversation_npc_schema.npc_name_2} is not in npc list!")
    
    while True:
        try:
            answer, tokens, execution_time = chatbot.conversation_between_npc(
                f" target_npc_1: ({npc_1})\n" \
                + f" target_npc_2: ({npc_2})\n" \
                + f"{npc_name_1}: " \
            )
            answer_list = [i for i in answer.split("\n") if i]
            validity_check = []
            for answer_ in answer_list:
                if npc_name_1 not in answer_.split(':') and npc_name_2 not in answer_.split(':'):
                    validity_check.append(answer_)
            if not validity_check:
                break
            else:
                print("Invalid format, please try again")
        except IndexError as e:
            print("#"*10 + "I got IndexError...Try again!" + "#"*10)

    final_response = {
        "chatContent": answer_list, 
        "totalTokens": tokens["Total_Tokens"]
    }
    print(f"chatContent : {answer}")
    print(f"tokens : {tokens}")
    print(f"execution_time : {execution_time}")
    return final_response

@router.post("/generate_victim", tags=["generate_victim"])
async def generate_victim(generator_schema: GeneratorSchema):
    print(f"input : {generator_schema.content}")
    
    while True:
        try:
            answer = chatbot.generate_victim(
                generator_schema.content
            )
            break
        except IndexError as e:
            print("#"*10 + "I got IndexError...Try again!" + "#"*10)

    final_response = {
        "answer": answer, 
    }
    print(f"answer : {answer}")
    return final_response
