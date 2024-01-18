from langchain_openai import ChatOpenAI
from langchain_community.callbacks import get_openai_callback
from langchain.prompts import PromptTemplate
import time

from LLMs.langchain import chains


def intro(inputs: str) -> str:
    return chains.intro_chain.predict(input=inputs)

def scenario(inputs: str) -> str:
    return chains.scenario_chain.predict(input=inputs)

def execute_conversation(chain_predict, inputs):
    start_time = time.time()

    with get_openai_callback() as cb:
        response = chain_predict.predict(input=inputs)
        tokens = {"Total_Tokens": cb.total_tokens, 
                  "Prompt_Tokens": cb.prompt_tokens, 
                  "Completion_Tokens": cb.completion_tokens,
                  "Total_Cost_(USD)": f"${cb.total_cost}"}

    end_time = time.time()
    execution_time = round(end_time - start_time, 3)

    return response, tokens, execution_time

def conversation_with_user(inputs: str) -> str:
    return execute_conversation(chains.conversation_with_user_chain, inputs)

def conversation_between_npc(inputs: str) -> str:
    return execute_conversation(chains.conversation_between_npc_chain, inputs)

def generate_victim(inputs: str) -> str:
    return execute_conversation(chains.generate_victim_chain, inputs)