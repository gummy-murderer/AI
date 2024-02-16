from langchain_community.callbacks import get_openai_callback
import time

from LLMs.langchain import chains
from LLMs.langchain.prompt import prompts_schema
from lib.validation_check import response_format
from lib import const


def execute_conversation(chain_function, format_check_function, schema, inputs):
    """
    Executes a conversation chain function and formats the response.
    
    Args:
        chain_function (function): The chain function to execute.
        format_check_function (function): The function to format and validate the response.
        schema (Pydantic schema): The schema to validate and serialize the response.
        inputs (str): The input string to the conversation chain.
        
    Returns:
        Tuple containing the validated and serialized response, token counts, and execution time.
        Returns None if the maximum retry limit is exceeded or formatting fails.
    """
    retry_attempts = 0
    while True:
        try:
            start_time = time.time()

            with get_openai_callback() as cb:
                response = chain_function.predict(input=inputs)
                tokens = {"totalTokens": cb.total_tokens, 
                          "promptTokens": cb.prompt_tokens, 
                          "completionTokens": cb.completion_tokens,
                        #   "totalCost(USD)": Uncomment to include cost
                          }

            end_time = time.time()
            execution_time = round(end_time - start_time, 3)

            answer = schema(**format_check_function(response))
            if answer:
                return answer, tokens, execution_time
        except:
            print("#"*10 + "I got Error...Try again!" + "#"*10)
            retry_attempts += 1
            print("Format is not correct, retrying...")
            if retry_attempts >= const.MAX_RETRY_LIMIT:
                print("Exceeded maximum attempt limit, terminating response generation.")
                break  # Ensure function exits after max retries


# scenario
def generate_intro(key: str, inputs: str):
    intro_chain = chains.define_intro_chain(key)
    return execute_conversation(intro_chain, response_format, prompts_schema.IntroSchema, inputs)

def generate_victim(key: str, inputs: str):
    victim_chain = chains.define_victim_chain(key)
    return execute_conversation(victim_chain, response_format, prompts_schema.GenerateVictimSchema, inputs)

def generate_final_words(key: str, inputs: str):
    final_words_chain = chains.define_final_words_chain(key)
    return execute_conversation(final_words_chain, response_format, prompts_schema.FinalWordsSchema, inputs)

# user
def generate_conversation_with_user(key: str, inputs: str):
    conversation_with_user_chain = chains.define_conversation_with_user_chain(key)
    return execute_conversation(conversation_with_user_chain, response_format, prompts_schema.ConversationWithUserSchema, inputs)

def generate_conversation_between_npc(key: str, inputs: str):
    conversation_between_npc_chain = chains.define_conversation_between_npc_chain(key)
    return execute_conversation(conversation_between_npc_chain, response_format, prompts_schema.ConversationBetweenNPCSchema, inputs)

def generate_conversation_between_npcs_each(key: str, inputs: str):
    conversation_between_npcs_each_chain = chains.define_conversation_between_npcs_each_chain(key)
    return execute_conversation(conversation_between_npcs_each_chain, response_format, prompts_schema.ConversationBetweenNPCEachSchema, inputs)

