from fastapi import APIRouter, HTTPException

from domain.scenario.scenario_schema import GeneratorSchema, GenerateVictimSchema
from domain.scenario.scenario_crud import get_all_npc_information, get_criminal_scenario, get_specific_npc_information
from LLMs.langchain import chatbot

router = APIRouter(
    prefix="/api/scenario",
)


@router.post("/intro_generator", 
             description="사용자 입력에 기반하여 소개 또는 시작 대화를 생성해 주는 API입니다.", 
             tags=["scenario"])
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
             tags=["scenario"])
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


@router.post("/generate_victim", 
             description="밤마다 진행되는 피해자 선택과 흰트를 생성해 주는 API입니다.", 
             tags=["scenario"])
async def generate_victim(generate_victim_schema: GenerateVictimSchema):
    print(f"day : {generate_victim_schema.day}")
    print(f"murderer : {generate_victim_schema.murderer}")
    print(f"livingCharacters : {generate_victim_schema.livingCharacters}")
    print(f"previousStory : {generate_victim_schema.previousStory}")
    # previousStory 이용 안함
    
    characters = get_specific_npc_information(generate_victim_schema.livingCharacters)
    criminal_scenario = get_criminal_scenario(generate_victim_schema.murderer)

    prompt = f"{characters}\n" \
                f"Input\n" \
                + f"day: {generate_victim_schema.day}\n" \
                + f"murderer: {criminal_scenario['npcName']}\n" \
                + f"motivation: {criminal_scenario['Motivation']}\n" \
                + f"procedure: {criminal_scenario['Procedure']}\n" \
                + f"previousStory: {generate_victim_schema.previousStory}\n" \

    answer, tokens, execution_time = chatbot.generate_victim(prompt)

    final_response = {
        "chatContent": answer, 
        "totalTokens": tokens["Total_Tokens"]
    }
    print(f"chatContent : {answer}\ntokens : {tokens}\nexecution_time : {execution_time}")
    return final_response