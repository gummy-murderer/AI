from fastapi import APIRouter, HTTPException

from domain.chatbot.chatbot_schema import GeneratorSchema, ConversationUserSchema, ConversationNPCSchema, GenerateVictimSchema
from domain.chatbot.chatbot_crud import get_npc_information, get_all_npc_information, get_criminal_scenario, get_specific_npc_information
from LLMs.langchain import chatbot

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
        "totalTokens": tokens["Total_Tokens"]
    }

    print(f"chatContent : {answer}\ntokens : {tokens}\nexecution_time : {execution_time}")
    return final_response


@router.post("/conversation_between_npcs", 
             description="npc와 npc간의 대화를 생성해 주는 API입니다.", 
             tags=["generator"])
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
        "totalTokens": tokens["Total_Tokens"]
    }

    print(f"chatContent : {answer}\ntokens : {tokens}\nexecution_time : {execution_time}")
    return final_response


@router.post("/generate_victim", 
             description="밤마다 진행되는 피해자 선택과 흰트를 생성해 주는 API입니다.", 
             tags=["generator"])
async def generate_victim(generate_victim_schema: GenerateVictimSchema):
    print(f"day : {generate_victim_schema.day}")
    print(f"murderer : {generate_victim_schema.murderer}")
    print(f"livingCharacters : {generate_victim_schema.livingCharacters}")
    print(f"previousStory : {generate_victim_schema.previousStory}")
    # previousStory 이용 안함
    
    characters = get_all_npc_information(info_type='str')
    characters = get_specific_npc_information(info_type='str')
    criminal_scenario = get_criminal_scenario(generate_victim_schema.murderer)

    while True:
        try:
            answer, tokens, execution_time = chatbot.generate_victim(
                f"{characters}\n" \
                f"Input\n" \
                + f"day: {generate_victim_schema.day}\n" \
                + f"murderer: {criminal_scenario['npcName']}\n" \
                + f"motivation: {criminal_scenario['Motivation']}\n" \
                + f"procedure: {criminal_scenario['Procedure']}\n" \
                + f"previousStory: {generate_victim_schema.previousStory}\n" \
            )
            answer_dic = {i.split(':')[0]: i.split(':')[1] for i in answer.split('\n')}
            break
        except IndexError as e:
            print("#"*10 + "I got IndexError...Try again!" + "#"*10)

    print(f"answer : {answer}")
    final_response = {
        "chatContent": answer_dic, 
        "totalTokens": tokens["Total_Tokens"]
    }
    return final_response
