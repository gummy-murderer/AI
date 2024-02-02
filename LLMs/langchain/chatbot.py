from langchain_community.callbacks import get_openai_callback
import time

from LLMs.langchain import chains
from LLMs.langchain.prompt import prompts_schema
from lib.response_format_check import response_format
from lib import const


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
            if retry_attempts >= const.MAX_RETRY_LIMIT:
                print("Exceeded maximum attempt limit, terminating response generation.")
                break

# scenario
def generate_intro(inputs):
    return execute_conversation(chains.generate_intro, response_format, prompts_schema.IntroSchema, inputs)

def generate_victim(inputs):
    return execute_conversation(chains.generate_victim_chain, response_format, prompts_schema.GenerateVictimSchema, inputs)

def generate_final_words(inputs):
    return execute_conversation(chains.generate_final_words, response_format, prompts_schema.FinalWordsSchema, inputs)

# user
def conversation_with_user(inputs):
    return execute_conversation(chains.conversation_with_user_chain, response_format, prompts_schema.ConversationWithUserSchema, inputs)

def conversation_between_npc(inputs):
    return execute_conversation(chains.conversation_between_npc_chain, response_format, prompts_schema.ConversationBetweenNPCSchema, inputs)

def conversation_between_npcs_each(inputs):
    return execute_conversation(chains.conversation_between_npc_each_chain, response_format, prompts_schema.ConversationBetweenNPCEachSchema, inputs)

