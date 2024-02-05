from fastapi import APIRouter, HTTPException

from domain.scenario import scenario_crud
from domain.scenario.schema import scenario_router_schema
from LLMs.langchain import chatbot

router = APIRouter(
    prefix="/api/scenario",
)


@router.post("/generate_intro", 
             description="게임의 intro를 생성해 주는 API입니다.", 
             response_model=scenario_router_schema.GenerateIntroOutput, 
             tags=["scenario"])
async def generate_intro(generator_intro_schema: scenario_router_schema.GenerateIntroInput):
    print(generator_intro_schema.model_dump_json(indent=2))
    
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
             response_model=scenario_router_schema.GenerateVictimOutput, 
             tags=["scenario"])
async def generate_victim(generate_victim_schema: scenario_router_schema.GenerateVictimInput):
    print(generate_victim_schema.model_dump_json(indent=2))
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


@router.post("/generate_victim_backup_plan", 
             description="밤마다 진행되는 피해자 선택과 흰트를 2개 생성해 주는 API입니다.", 
             response_model=scenario_router_schema.GenerateVictimBackupPlanOutput, 
             tags=["scenario"])
async def generate_victim_backup_plan(generate_victim_schema: scenario_router_schema.GenerateVictimInput):
    print(generate_victim_schema.model_dump_json(indent=2))
    # previousStory 이용 안함

    # plan A
    input_data_json, input_data_pydantic = scenario_crud.generate_victim_input(generate_victim_schema)

    answer_a, tokens_a, execution_time_a = chatbot.generate_victim(input_data_pydantic)

    result_a = scenario_crud.generate_victim_output(answer_a, input_data_pydantic)

    # plan B
    generate_victim_schema.livingCharacters.remove(input_data_pydantic.information.victim)

    input_data_json, input_data_pydantic = scenario_crud.generate_victim_input(generate_victim_schema)

    answer_b, tokens_b, execution_time_b = chatbot.generate_victim(input_data_pydantic)
    result_b = scenario_crud.generate_victim_output(answer_b, input_data_pydantic)

    # result
    tokens = {key: tokens_a.get(key, 0) + tokens_b.get(key, 0) for key in set(tokens_a) | set(tokens_b)}

    final_response = {
        "answer": {
            "planA": result_a,
            "planB": result_b
        }, 
        "tokens": tokens
    }
    print(f"answer : {answer_a, answer_b}\ntokens : {tokens}\nexecution_time : {execution_time_a + execution_time_b}")
    return final_response


@router.post("/generate_final_words", 
             description="범인의 마지막 한마디를 생성해 주는 API입니다.", 
             response_model=scenario_router_schema.GenerateFinalWordsOutput, 
             tags=["scenario"])
async def generate_final_words(generator_final_words_schema: scenario_router_schema.GenerateFinalWordsInput):
    print(generator_final_words_schema.model_dump_json(indent=2))
    # previousStory 이용 안함

    if not scenario_crud.get_character_info(generator_final_words_schema.murderer):
        raise HTTPException(status_code=404, detail="Murderer not found in the character list.")
    
    input_data_json, input_data_pydantic = scenario_crud.generate_final_words_input(generator_final_words_schema)

    answer, tokens, execution_time = chatbot.generate_final_words(input_data_pydantic)

    final_response = {
        "answer": answer, 
        "tokens": tokens
    }
    print(f"answer : {answer}\ntokens : {tokens}\nexecution_time : {execution_time}")
    return final_response