from fastapi import APIRouter
from datetime import datetime

from domain.chatbot.chatbot_schema import GeneratorSchema, ConversationUserSchema, ConversationNPCSchema
from lang_agency import chatbot
# from lang_agency import chatbot, memory


router = APIRouter(
    prefix="/api/chatbot",
)

@router.get("/hello", tags=["hello"])
async def hello():
    return {"content": "Hello World!"}


@router.post("/intro_generator", tags=["conversation_with_user"])
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


@router.post("/scenario_generator", tags=["conversation_with_user"])
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


@router.post("/conversation_with_user", tags=["conversation_with_user"])
async def conversation_with_user(conversation_user_schema: ConversationUserSchema):
    print(f"input")
    print(f"content : {conversation_user_schema.content}")
    print(f"npc_name : {conversation_user_schema.npc_name}")
    
    while True:
        try:
            answer = chatbot.conversation_with_user(
                f" content: {conversation_user_schema.content}" \
                + f" target_npc: {conversation_user_schema.npc_name}" \
            )
            break
        except IndexError as e:
            print("#"*10 + "I got IndexError...Try again!" + "#"*10)

    final_response = {
        "answer": answer, 
    }
    print(f"answer : {answer}")
    return final_response


@router.post("/conversation_between_npc", tags=["conversation_with_user"])
async def conversation_between_npc(conversation_npc_schema: ConversationNPCSchema):
    print(f"input")
    print(f"npc_name_1 : {conversation_npc_schema.npc_name_1}")
    print(f"npc_name_2 : {conversation_npc_schema.npc_name_2}")
    
    while True:
        try:
            answer = chatbot.conversation_between_npc(
                f" npc_name_1: {conversation_npc_schema.npc_name_1}" \
                + f" npc_name_2: {conversation_npc_schema.npc_name_2}" \
            )
            break
        except IndexError as e:
            print("#"*10 + "I got IndexError...Try again!" + "#"*10)

    final_response = {
        "answer": answer, 
    }
    print(f"answer : {answer}")
    return final_response
