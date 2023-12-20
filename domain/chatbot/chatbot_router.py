from fastapi import APIRouter
from datetime import datetime

from domain.chatbot.chatbot_schema import ChatbotSchema
from lang_agency import chatbot
# from lang_agency import chatbot, memory


router = APIRouter(
    prefix="/api/chatbot",
)

@router.get("/hello", tags=["hello"])
async def hello():
    return {"content": "Hello World!"}


@router.post("/conversation", tags=["conversation_with_user"])
async def chat(chatbot_schema: ChatbotSchema):
    print(f"input : {chatbot_schema.content}")
    
    while True:
        try:
            answer = chatbot.chatbot(
                chatbot_schema.content
            )
            break
        except IndexError as e:
            print("#"*10 + "I got IndexError...Try again!" + "#"*10)

    final_response = {
        "island_id": chatbot_schema.island_id,
        "answer": answer, 
        "task": "", 
    }
    print(f"answer : {answer}")
    if answer == "":
        final_response["task"] = "대기"
    return final_response


@router.post("/intro", tags=["conversation_with_user"])
async def chat(chatbot_schema: ChatbotSchema):
    print(f"input : {chatbot_schema.content}")
    
    while True:
        try:
            answer = chatbot.intro(
                chatbot_schema.content
            )
            break
        except IndexError as e:
            print("#"*10 + "I got IndexError...Try again!" + "#"*10)

    final_response = {
        "answer": answer, 
    }
    print(f"answer : {answer}")
    return final_response


@router.post("/scenario", tags=["conversation_with_user"])
async def chat(chatbot_schema: ChatbotSchema):
    print(f"input : {chatbot_schema.content}")
    
    while True:
        try:
            answer = chatbot.scenario(
                chatbot_schema.content
            )
            break
        except IndexError as e:
            print("#"*10 + "I got IndexError...Try again!" + "#"*10)

    final_response = {
        "answer": answer, 
    }
    print(f"answer : {answer}")
    return final_response
