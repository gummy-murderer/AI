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


# @router.post("/conversation", tags=["conversation"])
# async def chat(chatbot_schema: ChatbotSchema):
#     day_of_the_week = {0: "Monday", 1: "Tuesday", 2: "Wednesday", 3: "Thursday", 4: "Friday", 5: "Saturday", 6: "Sunday"}
#     current_time = f" current_time: {datetime.now()} {day_of_the_week[datetime.now().weekday()]}"
#     chatbot_name = "까망"
    
#     answer = ""
#     if chatbot_name in chatbot_schema.content:
        
#         while True:
#             try:
#                 answer = chatbot.chatbot(
#                     chatbot_schema.content \
#                     + current_time \
#                     + f" current_user: {chatbot_schema.user_id}" \
#                     + f" chatbot_name: {chatbot_name}"
#                 )
#                 break
#             except IndexError as e:
#                 print("#"*10 + "I got IndexError...Try again!" + "#"*10)
#     else:
#         memory.memory.chat_memory.add_user_message(chatbot_schema.content)

#     print(memory.memory)
#     print("#"*10 + answer + "#"*10)
#     final_response = {
#         "island_id": chatbot_schema.island_id,
#         "answer": answer, 
#         "task": "", 
#         "data": {
#             "year": None, 
#             "month": None, 
#             "date": None, 
#             "hour": None, 
#             "minute": None, 
#             "content": None,
#         }
#     }
#     if answer == "":
#         final_response["task"] = "대기"
#     return final_response