from langchain.prompts.prompt import PromptTemplate
from LLMs.langchain.prompts_data import synopsis, characters


conversation_with_user_chain_prefix = """
1. target_npc_info의 설명을 참고하여 해당 캐릭터를 연기해야 함.
2. 시놉시스와 시나리오를 참고하여 플래이어에게 대답해야함.
3. 이모지는 답변에 포함되면 안됨.
4. 답변의 길이는 2~3 문장 안으로 제한함.
5. 대화내용이 주어진다면 해당 대화에 맞는 답변을 생성해야 함.
"""

conversation_between_npc_chain_prefix = """
1. 등장인물 설정을 참고하여 target_npc_1과 target_npc_2사이의 대화를 생성하야 함.
2. 플래이어와의 대화가 아니라 npc들 사이의 대화를 만들어야 함.
3. 시놉시스와 시나리오를 참고하여야함.
3. 등장인물 설정을 참고하여 힌트를 흘리는데 설정에 따라 가짜 힌트가 될 수도 있고 진짜 힌트가 될 수도 있음.
4. 대화는 3~4번 정도 주고 받고 답변의 형식은 npc_name_1 : , npc_name_2 : , ... 과 같은 형식이여야 함.
5. 답변은 모두 한국어여야 함.
"""

# conversation_between_npc_stepwise_chain_prefix = """
# 1. 등장인물 설정을 참고하여 target_npc_1과 target_npc_2사이의 대화를 생성하야 함.
# 2. 플래이어와의 대화가 아니라 npc들 사이의 대화를 만들어야 함.
# 3. 시놉시스와 시나리오를 참고하여야함.
# 4. 등장인물 설정을 참고하여 힌트를 흘리는데 설정에 따라 가짜 힌트가 될 수도 있고 진짜 힌트가 될 수도 있음.
# 5. 대화 내용을 참고하여 다음 사람이 할 말을 생성해야 함. 대화 내용이 주어지지 않으면 해당 npc가 다른 npc 에게 말을 거는 상황임.
# """
conversation_between_npc_stepwise_chain_prefix = """
1. 등장인물 설정을 참고하여 target_npc_1이 target_npc_2에게 하는 말을 생성하야 함.
3. 시놉시스와 시나리오를 참고하여야함.
4. 등장인물 설정을 참고하여 힌트를 흘리는데 설정에 따라 가짜 힌트가 될 수도 있고 진짜 힌트가 될 수도 있음.
5. 대화 내용을 참고하여 다음 사람이 할 말을 생성해야 함. 대화 내용이 주어지지 않으면 해당 npc가 다른 npc 에게 말을 거는 상황임.
"""

conversation_chain_suffix = """
{input}
"""

conversation_with_user_template = synopsis + conversation_with_user_chain_prefix + conversation_chain_suffix
conversation_with_user_prompt = PromptTemplate(template=conversation_with_user_template, input_variables=["input"])

conversation_between_npc_template = synopsis + conversation_between_npc_chain_prefix + conversation_chain_suffix
conversation_between_npc_prompt = PromptTemplate(template=conversation_between_npc_template, input_variables=["input"])

conversation_between_npc_stepwise_template = synopsis + conversation_between_npc_stepwise_chain_prefix + conversation_chain_suffix
conversation_between_npc_stepwise_prompt = PromptTemplate(template=conversation_between_npc_stepwise_template, input_variables=["input"])