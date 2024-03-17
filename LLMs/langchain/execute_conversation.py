from langchain_community.callbacks import get_openai_callback
import time

from tts.tts import define_text_to_speech
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
            
            # generate_intro - answer.content 값이 있는지 확인
            # if hasattr(answer, 'content') and answer.content:
            #     tts_answer = define_text_to_speech(answer.greeting + answer.content + answer.closing)
            # conversation_with_user - answer.chatContent 값이 있는지 확인
            # elif hasattr(answer, 'chatContent') and answer.chatContent:
            #     tts_answer = define_text_to_speech(answer.chatContent)
            # else:
            #     tts_answer = None
            
            if answer:
                return answer, tokens, execution_time
        except:
            print("#"*10 + "I got Error...Try again!" + "#"*10)
            retry_attempts += 1
            print("Format is not correct, retrying...")
            if retry_attempts >= const.MAX_RETRY_LIMIT:
                print("Exceeded maximum attempt limit, terminating response generation.")
                break  # Ensure function exits after max retries