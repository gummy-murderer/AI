from pathlib import Path
import os

# from langchain.agents import AgentType, initialize_agent
from langchain_openai import ChatOpenAI
import dotenv

from LLMs.langchain import tools, memory, chains


# llm
dotenv_file = dotenv.find_dotenv(str(Path("./").absolute().joinpath(".env")))
dotenv.load_dotenv(dotenv_file)
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

# llm = ChatOpenAI(model="gpt-3.5-turbo-1106", openai_api_key=OPENAI_API_KEY)
llm = ChatOpenAI(model="gpt-4-1106-preview", openai_api_key=OPENAI_API_KEY)
# llm = ChatOpenAI(model="gpt-4", openai_api_key=OPENAI_API_KEY)

# agent
# agent_chain = initialize_agent(
#     llm=llm,
#     tools=tools.tools,
#     agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
#     agent_kwargs=memory.agent_kwargs,
#     memory=memory.memory,
#     # prompt="",
#     max_iterations=10,
#     # max_execution_time=5,
#     verbose=False,
#     handle_parsing_errors=True,
#     # return_intermediate_steps=True,
#     early_stopping_method="generate",
# )

def intro(inputs: str) -> str:
    return chains.intro_chain.predict(input=inputs)


def scenario(inputs: str) -> str:
    return chains.scenario_chain.predict(input=inputs)


def conversation_with_user(inputs: str) -> str:
    return chains.conversation_with_user_chain.predict(input=inputs)


def conversation_between_npc(inputs: str) -> str:
    return chains.conversation_between_npc_chain.predict(input=inputs)

# def chatbot(inputs: str) -> str:
#     answer = agent_chain.run(input=inputs)
#     return chains.conversation_chain.predict(input=answer)