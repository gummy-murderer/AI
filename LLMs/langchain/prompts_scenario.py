from langchain.prompts.prompt import PromptTemplate
from LLMs.langchain.prompts_data import synopsis, characters, places
import json


intro_chain_prefix = """
1. 시놉시스를 이용해서 마을의 촌장의 입장으로 탐정에게 보내는 편지를 만들어야 함.
2. 답변의 길이는 5문장은 넘지 말아야 함.
3. 답변의 형식은 greeting, content, closing 이 들어가 있는 dictionary 형태로 반환해야 함.
"""

generate_victim_prefix ="""
1. 등장인물 설정을 참고하여 살해당할 피해자를 지정해야 함.
2. 살인자의 성격에 의거하여 places 중에 살인장소를 선정하고 crimeScene에 placeNameEn를 넣어야 함.
2. 살해방법은 칼을 이용한 살인임.
3. 살인자와 피해자 이외의 등장인물 중 목격자를 지정해야 함.
4. 지정된 목격자가 플레이어의 추리에 도움이 될 수 있도록 목격정보를 지정해야 함.
5. dailySummary에는 누가 어디서 살해되었는 지 간단히 설명으로 지정해야 함. day정보가 들어가야 함. 해당 정보는 탐정에게 제공되는 것이 아니라 다음번 시나리오 생성을 위해 제공될 것임.
6. previousStory를 참고하여 이후의 스토리를 만들어야하며 previousStory의 내용은 들어가면 안됨.
7. 답변의 형식은 victim, crimeScene, method, witness, eyewitnessInformation, dailySummary 이 들어가 있는 json 형태로 반환해야 함.
"""

final_words_chain_prefix = """
1. murderer information을 참고하여 해당 인물의 마지막 한마디를 생성해야 함.
2. 마지막 한마디의 내용은 game result에 따라 달려져야 함. 'victory'라면 살인자의 패배이고 'defeat'면 살인자가 모든 마을 주민을 죽이고 승리한 상황임.
3. 답변의 길이는 4문장은 넘지 말아야 함.
4. 답변의 형식은 finalWords가 들어가 있는 dictionary 형태로 반환해야 함.
"""

conversation_chain_suffix = """
{input}
"""

intro_template = synopsis + intro_chain_prefix + conversation_chain_suffix
intro_prompt = PromptTemplate(template=intro_template, input_variables=["input"])

final_words_template = synopsis + final_words_chain_prefix + conversation_chain_suffix
final_words_prompt = PromptTemplate(template=final_words_template, input_variables=["input"])

generate_victim_template = synopsis + places + generate_victim_prefix + conversation_chain_suffix
generate_victim_prompt = PromptTemplate(template=generate_victim_template, input_variables=["input"])