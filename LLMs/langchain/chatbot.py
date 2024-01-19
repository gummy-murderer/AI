from langchain_community.callbacks import get_openai_callback
import time

from LLMs.langchain import chains
from lib.response_format_check import conversation_with_user_format, conversation_between_npcs_format, generate_victim_format

MAX_RETRY_LIMIT = 3


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


def intro(inputs: str) -> str:
    return chains.intro_chain.predict(input=inputs)


def scenario(inputs: str) -> str:
    return chains.scenario_chain.predict(input=inputs)


def conversation_with_user(inputs: str) -> str:
    retry_attempts = 0
    while True:
        try:
            answer, tokens, execution_time = execute_conversation(chains.conversation_with_user_chain, inputs)
            if conversation_with_user_format(answer):
                break
        except IndexError as e:
            print("#"*10 + "I got IndexError...Try again!" + "#"*10)
        retry_attempts += 1
        print("Format is not correct, retrying...")
        if retry_attempts >= MAX_RETRY_LIMIT:
            print("Exceeded maximum attempt limit, terminating response generation.")
            break

    return answer, tokens, execution_time


def conversation_between_npc(inputs: str, name1, name2):
    retry_attempts = 0
    while True:
        try:
            answer, tokens, execution_time = execute_conversation(chains.conversation_between_npc_chain, inputs)
            answer_list = conversation_between_npcs_format(name1, name2, answer)
            if answer_list:
                break
        except IndexError as e:
            print("#"*10 + "I got IndexError...Try again!" + "#"*10)
        retry_attempts += 1
        print("Format is not correct, retrying...")
        if retry_attempts >= MAX_RETRY_LIMIT:
            print("Exceeded maximum attempt limit, terminating response generation.")
            break

    return answer_list, tokens, execution_time


def generate_victim(inputs: str) -> str:
    retry_attempts = 0
    while True:
        try:
            answer, tokens, execution_time = execute_conversation(chains.generate_victim_chain, inputs)
            answer_dic = generate_victim_format(answer)
            if answer_dic:
                break
        except IndexError as e:
            print("#"*10 + "I got IndexError...Try again!" + "#"*10)
        retry_attempts += 1
        print("Format is not correct, retrying...")
        if retry_attempts >= MAX_RETRY_LIMIT:
            print("Exceeded maximum attempt limit, terminating response generation.")
            break

    return answer_dic, tokens, execution_time