from langchain_openai import ChatOpenAI
from langchain_community.callbacks import get_openai_callback
from langchain.prompts import PromptTemplate
import time

from LLMs.langchain import chains


def intro(inputs: str) -> str:
    return chains.intro_chain.predict(input=inputs)


def scenario(inputs: str) -> str:
    return chains.scenario_chain.predict(input=inputs)


def conversation_with_user(inputs: str) -> str:
    start_time = time.time()

    with get_openai_callback() as cb:
        result = chains.conversation_with_user_chain.predict(input=inputs)
        tokens = {"Total_Tokens": cb.total_tokens, 
                  "Prompt_Tokens": cb.prompt_tokens, 
                  "Completion_Tokens": cb.completion_tokens,
                  "Total_Cost_(USD)": f"${cb.total_cost}"}
    
    end_time = time.time()
    execution_time = round(end_time - start_time, 3)

    return result, tokens, execution_time


def conversation_between_npc(prompt_template: PromptTemplate, npc_name_1: str, npc_name_2: str) -> str:
    # PromptTemplate 객체에서 실제 템플릿 문자열을 가져옴
    prompt_str = prompt_template.template
    
    # 문자열에서 npc_name_1과 npc_name_2를 실제 NPC 이름으로 대체
    updated_prompt = prompt_str.replace("npc_name_1", npc_name_1).replace("npc_name_2", npc_name_2)

    # 대화 생성
    response = chains.conversation_between_npc_chain.predict(input=updated_prompt)
    return response