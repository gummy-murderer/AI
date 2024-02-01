from langchain.prompts.prompt import PromptTemplate
from langchain.output_parsers import PydanticOutputParser

from LLMs.langchain.prompt.prompts_data import synopsis
from LLMs.langchain.prompt.prompts_schema import IntroSchema, GenerateVictimSchema, FinalWordsSchema



intro_chain_prefix = """
1. 시놉시스를 이용해서 마을의 촌장의 입장으로 탐정에게 보내는 편지를 만들어야 함.
2. 답변의 길이는 7문장은 넘지 말아야 함.
"""

generate_victim_prefix ="""
1. 주어진 information을 보고 eyewitnessInformation, dailySummary를 생성해야 함
2. dailySummary에는 누가 어디서 살해되었는 지 간단히 설명으로 지정해야 함. 'day 0 - '과 같은 식으로 시작해야 함
3. 지정된 목격자가 플레이어의 추리에 도움이 될 수 있도록 목격정보를 지정해야 함
4. previousStory를 참고하여 이후의 스토리를 만들어야하며 previousStory의 내용은 들어가면 안됨
5. 모든 답변은 단답식으로 작성되어야 함
"""

final_words_chain_prefix = """
1. information을 참고하여 살인자의 마지막 한마디를 생성해야 함.
2. 마지막 한마디의 내용은 gameResult에 따라 달려져야 함. 'victory'라면 살인자의 패배이고 'defeat'면 살인자가 모든 마을 주민을 죽이고 승리한 상황임.
3. 답변의 길이는 4문장은 넘지 말아야 함.
"""

conversation_chain_suffix = """
{format_instructions}
{input}
"""


intro_parser = PydanticOutputParser(pydantic_object=IntroSchema)
intro_template = synopsis + intro_chain_prefix + conversation_chain_suffix
intro_prompt = PromptTemplate(template=intro_template, 
                              input_variables=["input"], 
                              partial_variables={"format_instructions": intro_parser.get_format_instructions()})
                              
generate_victim_parser = PydanticOutputParser(pydantic_object=GenerateVictimSchema)
generate_victim_template = synopsis + generate_victim_prefix + conversation_chain_suffix
generate_victim_prompt = PromptTemplate(template=generate_victim_template, 
                                        input_variables=["input"], 
                                        partial_variables={"format_instructions": generate_victim_parser.get_format_instructions()})
                              
final_words_parser = PydanticOutputParser(pydantic_object=FinalWordsSchema)
final_words_template = synopsis + final_words_chain_prefix + conversation_chain_suffix
final_words_prompt = PromptTemplate(template=final_words_template, 
                                    input_variables=["input"], 
                                    partial_variables={"format_instructions": final_words_parser.get_format_instructions()})