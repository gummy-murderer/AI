from fastapi import APIRouter, HTTPException

# from domain.scenario.scenario_schema import GenerateVictimInput
from domain.scenario import scenario_crud, scenario_schema
from LLMs.langchain import chatbot

router = APIRouter(
    prefix="/api/scenario",
)


@router.post("/generate_intro", 
             description="게임의 intro를 생성해 주는 API입니다.", 
             response_model=scenario_schema.GenerateIntroOutput, 
             tags=["scenario"])
async def generate_intro(generator_intro_schema: scenario_schema.GenerateIntroInput):
    print(f"Characters : {generator_intro_schema.characters}")
    
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
             response_model=scenario_schema.GenerateVictimOutput, 
             tags=["scenario"])
async def generate_victim(generate_victim_schema: scenario_schema.GenerateVictimInput):
    print(f"day : {generate_victim_schema.day}")
    print(f"murderer : {generate_victim_schema.murderer}")
    print(f"livingCharacters : {generate_victim_schema.livingCharacters}")
    print(f"previousStory : {generate_victim_schema.previousStory}")
    # previousStory 이용 안함

    input_data_json, input_data_pydantic = scenario_crud.generate_victim_input(generate_victim_schema)
    if not input_data_json or not input_data_pydantic:
        if not scenario_crud.get_character_info(generate_victim_schema.murderer):
            raise HTTPException(status_code=404, detail="Murderer not found in the character list.")
        else:
            raise HTTPException(status_code=404, detail="Invalid livingCharacters in the list.")

    answer, tokens, execution_time = chatbot.generate_victim(input_data_pydantic)

    result = scenario_crud.generate_victim_output(answer, input_data_pydantic)
    final_response = {
        "answer": result, 
        "tokens": tokens
    }
    print(f"answer : {answer}\ntokens : {tokens}\nexecution_time : {execution_time}")
    return final_response

