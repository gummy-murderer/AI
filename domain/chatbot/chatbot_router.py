from fastapi import APIRouter

from domain.chatbot.chatbot_schema import GeneratorSchema, ConversationUserSchema, ConversationNPCSchema
from LLMs.langchain import chatbot, prompts
# from lang_agency import chatbot, memory
from lib.npc_management import get_npc_information


router = APIRouter(
    prefix="/api/chatbot",
)


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
    print(f"sender : {conversation_user_schema.sender}")
    print(f"receiver : {conversation_user_schema.receiver}")
    print(f"chatContent : {conversation_user_schema.chatContent}")
    print(f"chatDay : {conversation_user_schema.chatDay}")
    print(f"이전 대화 내용 넣어야 함")
    
    info = get_npc_information(conversation_user_schema.receiver, random_=True)
    print(info)

    while True:
        try:
            answer = chatbot.conversation_with_user(
                f" user: {conversation_user_schema.chatContent}\n" \
                + f" target_npc_info: ({info})" \
            )
            break
        except IndexError as e:
            print("#"*10 + "I got IndexError...Try again!" + "#"*10)

    final_response = {
        "answer": answer, 
    }
    print(f"answer : {answer}")
    return final_response


@router.post("/conversation_between_npcs", tags=["conversation_between_npcs"])
async def conversation_between_npc(conversation_npc_schema: ConversationNPCSchema):
    print(f"input")
    print(f"npc_name_1 : {conversation_npc_schema.npc_name_1}")
    print(f"npc_name_2 : {conversation_npc_schema.npc_name_2}")
    
    while True:
        try:
            answer = chatbot.conversation_between_npc(
                prompts.conversation_between_npc_prompt,
                conversation_npc_schema.npc_name_1,
                conversation_npc_schema.npc_name_2
            )
            break
        except IndexError as e:
            print("#"*10 + "I got IndexError...Try again!" + "#"*10)

    final_response = {
        "answer": answer, 
    }
    print(f"answer : {answer}")
    return final_response