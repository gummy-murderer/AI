from fastapi import APIRouter, HTTPException

from domain.scenario.scenario_schema import GenerateIntroSchema, GenerateVictimSchema, GenerateFinalWordsSchema
from domain.scenario.scenario_crud import get_criminal_scenario, get_specific_npc_information
from LLMs.langchain import chatbot

router = APIRouter(
    prefix="/api/scenario",
)


@router.post("/generate_intro", 
             description="게임의 intro를 생성해 주는 API입니다.", 
             tags=["scenario"])
async def generate_intro(generator_intro_schema: GenerateIntroSchema):
    print(f"Characters : {generator_intro_schema.Characters}")
    
    prompt = f"\n" \
    
    answer, tokens, execution_time = chatbot.generate_intro(prompt)

    final_response = {
        "answer": answer, 
        "tokens": tokens
    }
    print(f"answer : {answer}\ntokens : {tokens}\nexecution_time : {execution_time}")
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
    if not criminal_scenario:
        raise HTTPException(status_code=400, detail=f"{generate_victim_schema.murderer} is not in npc list!")

    prompt = f"{characters}\n" \
                + f"Input\n" \
                + f"day: {generate_victim_schema.day}\n" \
                + f"murderer: {criminal_scenario['npcName']}\n" \
                + f"motivation: {criminal_scenario['Motivation']}\n" \
                + f"procedure: {criminal_scenario['Procedure']}\n" \
                + f"previousStory: {generate_victim_schema.previousStory}\n" \

    answer, tokens, execution_time = chatbot.generate_victim(prompt)

    final_response = {
        "answer": answer, 
        "tokens": tokens
    }
    print(f"answer : {answer}\ntokens : {tokens}\nexecution_time : {execution_time}")
    return final_response


@router.post("/generate_victim_backup_plan", 
             description="밤마다 진행되는 피해자 선택과 흰트를 2개 생성해 주는 API입니다.", 
             tags=["scenario"])
async def generate_victim_backup_plan(generate_victim_schema: GenerateVictimSchema):
    print(f"day : {generate_victim_schema.day}")
    print(f"murderer : {generate_victim_schema.murderer}")
    print(f"livingCharacters : {generate_victim_schema.livingCharacters}")
    print(f"previousStory : {generate_victim_schema.previousStory}")
    # previousStory 이용 안함
    criminal_scenario = get_criminal_scenario(generate_victim_schema.murderer)

    # plan A
    characters = get_specific_npc_information(generate_victim_schema.livingCharacters)
    if not criminal_scenario:
        raise HTTPException(status_code=400, detail=f"{generate_victim_schema.murderer} is not in npc list!")

    prompt = f"{characters}\n" \
                + f"Input\n" \
                + f"day: {generate_victim_schema.day}\n" \
                + f"murderer: {criminal_scenario['npcName']}\n" \
                + f"motivation: {criminal_scenario['Motivation']}\n" \
                + f"procedure: {criminal_scenario['Procedure']}\n" \
                + f"previousStory: {generate_victim_schema.previousStory}\n" \

    answer_a, tokens_a, execution_time_a = chatbot.generate_victim(prompt)

    # plan B
    generate_victim_schema.livingCharacters.remove(answer_a['victim'])
    
    characters = get_specific_npc_information(generate_victim_schema.livingCharacters)
    if not criminal_scenario:
        raise HTTPException(status_code=400, detail=f"{generate_victim_schema.murderer} is not in npc list!")

    prompt = f"{characters}\n" \
                + f"Input\n" \
                + f"day: {generate_victim_schema.day}\n" \
                + f"murderer: {criminal_scenario['npcName']}\n" \
                + f"motivation: {criminal_scenario['Motivation']}\n" \
                + f"procedure: {criminal_scenario['Procedure']}\n" \
                + f"previousStory: {generate_victim_schema.previousStory}\n" \

    answer_b, tokens_b, execution_time_b = chatbot.generate_victim(prompt)

    tokens = {key: tokens_a.get(key, 0) + tokens_b.get(key, 0) for key in set(tokens_a) | set(tokens_b)}

    final_response = {
        "answer": {
            "planA": answer_a,
            "planB": answer_b
        }, 
        "tokens": tokens
    }
    # print(f"answer : {answer_a + answer_b}\ntokens : {tokens}\nexecution_time : {execution_time_a + execution_time_b}")
    return final_response


@router.post("/generate_final_words", 
             description="범인의 마지막 한마디를 생성해 주는 API입니다.", 
             tags=["scenario"])
async def generate_intro(generator_final_words_schema: GenerateFinalWordsSchema):
    print(f"result : {generator_final_words_schema.result}")
    print(f"murderer : {generator_final_words_schema.murderer}")
    # previousStory 이용 안함
    
    criminal_scenario = get_criminal_scenario(generator_final_words_schema.murderer)
    if not criminal_scenario:
        raise HTTPException(status_code=400, detail=f"{generator_final_words_schema.murderer} is not in npc list!")

    print(criminal_scenario)
    prompt = f"game result: {generator_final_words_schema.result}\n" \
                + f"murderer information\n" \
                + f"murderer: {criminal_scenario['npcName']}\n" \
                + f"motivation: {criminal_scenario['Motivation']}\n" \
                + f"procedure: {criminal_scenario['Procedure']}\n" \
                + f"{criminal_scenario['npcName']}: \n" \
    
    print(prompt)
    answer, tokens, execution_time = chatbot.generate_final_words(prompt)
    print(answer)

    final_response = {
        "answer": answer, 
        "tokens": tokens
    }
    print(f"answer : {answer}\ntokens : {tokens}\nexecution_time : {execution_time}")
    return final_response