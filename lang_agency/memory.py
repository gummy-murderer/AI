from langchain.prompts import MessagesPlaceholder
from langchain.memory import ConversationBufferWindowMemory


agent_kwargs = {
    "extra_prompt_messages": [MessagesPlaceholder(variable_name="chat_history")],
}
memory = ConversationBufferWindowMemory(memory_key="chat_history", return_messages=True, k=5)