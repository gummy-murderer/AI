from fastapi import APIRouter, HTTPException

from domain.scenario.scenario_schema import GenerateVictimSchema
from domain.scenario.scenario_crud import get_character_info, generate_victim_input
from LLMs.langchain import chatbot

router = APIRouter(
    prefix="/api/scenario",
)



@router.post("/generate_victim", 
             description="밤마다 진행되는 피해자 선택과 흰트를 생성해 주는 API입니다.", 
             tags=["scenario"])
async def generate_victim(generate_victim_schema: GenerateVictimSchema):
    print(f"day : {generate_victim_schema.day}")
    print(f"murderer : {generate_victim_schema.murderer}")
    print(f"livingCharacters : {generate_victim_schema.livingCharacters}")
    print(f"previousStory : {generate_victim_schema.previousStory}")
    # previousStory 이용 안함

    input_data_json, input_data_pydantic = generate_victim_input(generate_victim_schema)
    if not input_data_json or not input_data_pydantic:
        if not get_character_info(generate_victim_schema.murderer):
            raise HTTPException(status_code=404, detail="Murderer not found in the character list.")
        else:
            raise HTTPException(status_code=404, detail="Invalid livingCharacters in the list.")
        
    # print(input_data_json)
    # characters = get_specific_npc_information(generate_victim_schema.livingCharacters)
    # criminal_scenario = get_criminal_scenario(generate_victim_schema.murderer)
    # if not criminal_scenario:
    #     raise HTTPException(status_code=400, detail=f"{generate_victim_schema.murderer} is not in npc list!")

    # prompt = f"{characters}\n" \
    #             + f"Input\n" \
    #             + f"day: {generate_victim_schema.day}\n" \
    #             + f"murderer: {criminal_scenario['npcName']}\n" \
    #             + f"motivation: {criminal_scenario['Motivation']}\n" \
    #             + f"procedure: {criminal_scenario['Procedure']}\n" \
    #             + f"previousStory: {generate_victim_schema.previousStory}\n" \

    # answer, tokens, execution_time = chatbot.generate_victim(input_data_json)
    # print(answer, tokens, execution_time)
    # final_response = {
    #     "answer": answer, 
    #     "tokens": tokens
    # }
    # print(f"answer : {answer}\ntokens : {tokens}\nexecution_time : {execution_time}")
    # return final_response