from langchain.prompts.prompt import PromptTemplate
from langchain.output_parsers import PydanticOutputParser

from LLMs.langchain.prompt.prompts_data import synopsis
from LLMs.langchain.prompt.prompts_schema import ConversationWithUserSchema, ConversationBetweenNPCSchema


conversation_with_user_chain_prefix = """
1. information을 참고하여 character를 연기하여 user의 chatContent에 대답해야 함
2. 답변의 길이는 2~3 문장 안으로 제한함.
3. PreviousChatContents가 주어진다면 해당 대화에 맞는 답변을 생성해야 함.
4. 지난 밤에 무엇을 했는지 물어본다면 alibi 항목을 참고
5. 답변을 만들 때 personalityDescription, featureDescription을 참고해야 함
"""

conversation_between_npc_chain_prefix = """
1. 등장인물 설정을 참고하여 character1과 character2 사이의 대화를 생성하야 함.
2. 플래이어와의 대화가 아니라 npc들 사이의 대화를 만들어야 함.
3. 시놉시스와 시나리오를 참고하여야함.
3. 등장인물 설정을 참고하여 힌트를 흘리는데 설정에 따라 가짜 힌트가 될 수도 있고 진짜 힌트가 될 수도 있음.
4. 대화는 3~4번 정도 주고 받아야 함
"""

conversation_chain_suffix = """
{format_instructions}
{input}
"""


conversation_with_user_parser = PydanticOutputParser(pydantic_object=ConversationWithUserSchema)
conversation_with_user_template = synopsis + conversation_with_user_chain_prefix + conversation_chain_suffix
conversation_with_user_prompt = PromptTemplate(template=conversation_with_user_template, 
                                               input_variables=["input"], 
                                               partial_variables={"format_instructions": conversation_with_user_parser.get_format_instructions()})

conversation_between_npc_parser = PydanticOutputParser(pydantic_object=ConversationBetweenNPCSchema)
conversation_between_npc_template = synopsis + conversation_between_npc_chain_prefix + conversation_chain_suffix
conversation_between_npc_prompt = PromptTemplate(template=conversation_between_npc_template, 
                                               input_variables=["input"], 
                                               partial_variables={"format_instructions": conversation_between_npc_parser.get_format_instructions()})