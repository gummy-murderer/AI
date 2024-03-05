from langchain.output_parsers import PydanticOutputParser
from langchain.prompts.prompt import PromptTemplate

synopsis = """
주요 캐릭터:

1. 탐정 (플레이어): 유명한 탐정으로, 특이한 사건을 해결하는 데 능숙함.
2. 촌장: 마을의 촌장으로, 마을을 이끌고 있는 지혜로운 촌장.
3. 마을 주민들: 각기 다른 특성과 배경을 가진 주민들.

스토리 개요:

- 시작: 탐정인 플레이어는 마을의 촌장으로부터 마을에서 발생한 충격적인 살인 사건에 대한 의뢰를 받음. 평화로웠던 마을에서 처음으로 발생한 이 사건은 모두를 불안하게 만듬.
- 게임 진행: 탐정은 낮 동안 마을을 돌아다니며 주민들과 대화를 통해 힌트나 거짓말 을 판별하여 범인을 추리해야함.
- 밤 시간: 밤이 되면 범인은 또 다른 주민을 살해함. 이로 인해 다음 날의 조사는 더 어려워지며, 새로운 증거와 정보가 등장.
- 결말: 탐정은 모든 대화를 통해 범인을 추리해야 함. 범인을 정확히 지목하면 게임에서 승리, 실패 시 게임 오버.
"""

characters = """
등장인물
1. 촌장 : 거만하고 게으른 성격
2. 레오 : 용감함, 용기 있게 행동함, 뮤지션, 노래를 부르듯이 대답함
3. 소피아 : 지혜로움, 깊은 통찰력과 현명한 판단을 가짐, 조용함, 대화보다는 관찰을 선호함
4. 알렉스 : 모험적임, 새로운 것을 경험하려는 강한 욕구를 가짐, 떠돌이, 여러 마을을 떠돌아 다니는 떠돌이임
5. 자스민 : 회의적, 주변 사건에 대해 의심을 품으며 진실을 탐구함, 학자, 지식을 추구하고 책과 연구에 몰두함
6. 애쉬 : 유머러스함, 재치 있고 유머러스한 성격을 지님, 유머러스한 말투, 대화 중에 종종 재치 있는 농담을 섞어 말함
7. 짠짠영 : 기발함, 독창적이고 창의적인 생각으로 눈길을 끔, 발명가, 새롭고 혁신적인 아이디어로 다양한 발명품을 만듦
8. 김쿵야 : 장난꾸러기, 재미있고 유쾌한 성격으로 주변 사람들을 즐겁게 함, 마술사, 기발한 마술과 재치 있는 퍼포먼스로 사람들을 놀라게 함
9. 플레이어 : 플레이어는 탐정 역할로 이 마을에 벌어진 살인사건을 조사하는 중임.
"""

conversation_chain_suffix = """
{format_instructions}
{input}
"""

def prompt_template(schema, chain_prefix):
    parser = PydanticOutputParser(pydantic_object=schema)
    template = synopsis + chain_prefix + conversation_chain_suffix
    prompt = PromptTemplate(template=template, 
                            input_variables=["input"], 
                            partial_variables={"format_instructions": parser.get_format_instructions()})
    return prompt