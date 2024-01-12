from langchain.chains import LLMChain
from langchain_openai import ChatOpenAI
from pathlib import Path
import os, dotenv

from LLMs.langchain import prompts, memory

dotenv_file = dotenv.find_dotenv(str(Path("./").absolute().joinpath(".env")))
dotenv.load_dotenv(dotenv_file)
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

# llm = ChatOpenAI(model="gpt-3.5-turbo-1106", openai_api_key=OPENAI_API_KEY)
llm = ChatOpenAI(model="gpt-4-1106-preview", openai_api_key=OPENAI_API_KEY)
# llm = ChatOpenAI(model="gpt-4", openai_api_key=OPENAI_API_KEY)

intro_chain = LLMChain(
    prompt=prompts.intro_prompt,
    llm=llm,
    verbose=True,
)

scenario_chain = LLMChain(
    prompt=prompts.scenario_prompt,
    llm=llm,
    verbose=True,
)

conversation_with_user_chain = LLMChain(
    prompt=prompts.conversation_with_user_prompt,
    llm=llm,
    memory=memory.memory,
    verbose=True,
)

conversation_between_npc_chain = LLMChain(
    prompt=prompts.conversation_between_npc_prompt,
    llm=llm,
    memory=memory.memory,
    verbose=True,
)