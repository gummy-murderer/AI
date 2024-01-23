from langchain.chains import LLMChain
from langchain_openai import ChatOpenAI
from pathlib import Path
import os, dotenv

from LLMs.langchain import memory, prompts_scenario, prompts_user

dotenv_file = dotenv.find_dotenv(str(Path("./").absolute().joinpath(".env")))
dotenv.load_dotenv(dotenv_file)
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

# llm = ChatOpenAI(model="gpt-3.5-turbo-1106", openai_api_key=OPENAI_API_KEY)
llm = ChatOpenAI(model="gpt-4-1106-preview", openai_api_key=OPENAI_API_KEY)
# llm = ChatOpenAI(model="gpt-4", openai_api_key=OPENAI_API_KEY)


generate_intro = LLMChain(
    prompt=prompts_scenario.intro_prompt,
    llm=llm,
    verbose=True,
)

generate_final_words = LLMChain(
    prompt=prompts_scenario.final_words_prompt,
    llm=llm,
    verbose=True,
)

generate_victim_chain = LLMChain(
    prompt=prompts_scenario.generate_victim_prompt,
    llm=llm,
    verbose=True,
)

conversation_with_user_chain = LLMChain(
    prompt=prompts_user.conversation_with_user_prompt,
    llm=llm,
    memory=memory.memory,
    verbose=True,
)

conversation_between_npc_chain = LLMChain(
    prompt=prompts_user.conversation_between_npc_prompt,
    llm=llm,
    memory=memory.memory,
    verbose=True,
)