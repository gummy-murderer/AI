from langchain.chains import LLMChain
from langchain_openai import ChatOpenAI

from LLMs.langchain.prompt import prompts_scenario, prompts_user

MODEL = "gpt-4-1106-preview"


def define_llm_chain(key, prompt):
    llm = ChatOpenAI(model=MODEL, openai_api_key=key)
    return LLMChain(
        prompt=prompt,
        llm=llm,
        verbose=True,
    )

# scenario
def define_intro_chain(key):
    return define_llm_chain(key, prompts_scenario.intro_prompt)

def define_victim_chain(key):
    return define_llm_chain(key, prompts_scenario.generate_victim_prompt)

def define_final_words_chain(key):
    return define_llm_chain(key, prompts_scenario.final_words_prompt)

# user
def define_conversation_with_user_chain(key):
    return define_llm_chain(key, prompts_user.conversation_with_user_prompt)

def define_conversation_between_npc_chain(key):
    return define_llm_chain(key, prompts_user.conversation_between_npc_prompt)

def define_conversation_between_npcs_each_chain(key):
    return define_llm_chain(key, prompts_user.conversation_between_npc_each_prompt)