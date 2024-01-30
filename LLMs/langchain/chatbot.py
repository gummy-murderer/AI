from langchain_community.callbacks import get_openai_callback
import time

from LLMs.langchain import chains
from LLMs.langchain.prompt.prompts_schema import GenerateVictimSchema, IntroSchema
from lib.response_format_check import response_format

MAX_RETRY_LIMIT = 2

def execute_conversation(chain_function, format_check_function, schema, inputs, **kwargs):
    retry_attempts = 0
    while True:
        try:
            start_time = time.time()

            with get_openai_callback() as cb:
                response = chain_function.predict(input=inputs, **kwargs)
                tokens = {"totalTokens": cb.total_tokens, 
                          "promptTokens": cb.prompt_tokens, 
                          "completionTokens": cb.completion_tokens,
                        #   "totalCost(USD)": f"${cb.total_cost}"
                          }

            end_time = time.time()
            execution_time = round(end_time - start_time, 3)

            answer = schema(**format_check_function(response))
            if answer:
                return answer, tokens, execution_time
        except IndexError as e:
            print("#"*10 + "I got IndexError...Try again!" + "#"*10)
            retry_attempts += 1
            print("Format is not correct, retrying...")
            if retry_attempts >= MAX_RETRY_LIMIT:
                print("Exceeded maximum attempt limit, terminating response generation.")
                break

# scenario
def generate_intro(inputs):
    return execute_conversation(chains.generate_intro, response_format, IntroSchema, inputs)

def generate_victim(inputs):
    return execute_conversation(chains.generate_victim_chain, response_format, GenerateVictimSchema, inputs)

def generate_final_words(inputs):
    return execute_conversation(chains.generate_final_words, response_format, inputs)

# user
def conversation_with_user(inputs):
    return execute_conversation(chains.conversation_with_user_chain, response_format_check.conversation_with_user_format, inputs)

def conversation_between_npc(inputs, name1, name2):
    return execute_conversation(chains.conversation_between_npc_chain, response_format_check.conversation_between_npcs_format, inputs, name1=name1, name2=name2)

def conversation_between_npcs_stepwise(inputs):
    return execute_conversation(chains.conversation_between_npc_stepwise_chain, response_format_check.no_check, inputs)

