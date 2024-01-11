from langchain.prompts.prompt import PromptTemplate


synopsis = """
시놉시스 :
AI 와 함께하는 마피아

낮과 밤에 따른 각자의 역할에 따른 시간 분배

직업 : 마피아, 시민, 의사, 경찰

자연스럽고 현실적인 대화가 이루어 질 수 있도록 해야함

대화 흐름에 맞는 각각의 AI 의 판단에 의거한 투표 진행 및 선택

자신의 직업이 무엇인지 숨기고 시민인 척 연기해야하는 AI

게임 제목: "젤리곰 마을의 비밀"

배경

- **장소**: 컬러풀하고 평화로운 '젤리곰 마을'
- **시간**: 현재 시대, 마법과 기술이 공존하는 세계
- **사건**: 마을에서 발생한 첫 살인 사건

### **주요 캐릭터:**

1. **탐정 (플레이어)**: 유명한 탐정으로, 특이한 사건을 해결하는 데 능숙합니다.
2. **촌장**: 젤리곰 마을의 촌장으로, 마을을 이끌고 있는 지혜로운 곰입니다.
3. **젤리곰 마을 주민들**: 각기 다른 특성과 배경을 가진 젤리곰들로 구성된 커뮤니티.

### **스토리 개요:**

- **시작**: 탐정은 젤리곰 마을의 촌장으로부터 마을에서 발생한 충격적인 살인 사건에 대한 의뢰를 받습니다. 평화로웠던 마을에서 처음으로 발생한 이 사건은 모든 젤리곰들을 불안하게 만들었습니다.
- **게임 진행**: 탐정은 낮 동안 마을을 돌아다니며 주민들과 대화를 나누고, 증거를 수집합니다. 각 주민은 자신만의 이야기와 알리바이를 가지고 있으며, 탐정은 이 중에서 거짓말과 진실을 가려내야 합니다.
- **밤 시간**: 밤이 되면 범인은 또 다른 주민을 살해합니다. 이로 인해 다음 날의 조사는 더 어려워지며, 새로운 증거와 정보가 등장합니다.
- **결말**: 탐정은 모든 증거와 대화를 통해 범인을 추리해야 합니다. 범인을 정확히 지목하면 게임에서 승리하며, 그렇지 않으면 게임 오버입니다.
"""

characters = """
등장인물
1. 촌장 : 거만하고 게으른 성격
2. 범인 : 밤마다 일어나는 살인 사건의 범인, 자기가 범인이 아니라고 다른 이들을 속여야 함.
3. 주민1 : 착하고 친절한 성격. 모든 말 끝을 냥으로 대답함.
4. 주민2 : 거짓말 쟁이. 항상 자신이 아는 것에 반대로 말해야 함.
5. 주민5 : 진지하고 말이 많이 없음. 경상도 사투리로 대답함.
6. 플래이어 : 플래이어는 탐정 역할로 이 마을에 벌어진 살인사건을 조사하는 중임.
"""

intro_chain_prefix = """
1. 해당 시놉시스를 이용해서 마을의 촌장이 탐정에게 처음 상황을 설명하듯이 답변을 반말로 생성해야 함.
2. 답변의 길이는 5문장은 넘지 말아야 함.
"""

scenario_chain_prefix = """
1. 해당 시놉시스를 이용해서 밤마다 진행되는 스토리를 만들어야 함.
2. input으로는 'n번째 밤' 형식으로 들어오면 이전 시나리오를 참고하여 해당 날의 시나리오를 생성.
3. 밤에 범인의 타겟이 되는 인물을 정해야 함.
4. 해당 밤에 일어난 사건에 대하여 힌트가 될만한 정보를 알고 있는 등장인물을 설정하고 흰트를 생성해야 함.
5. 답변의 형식은 target, character, hint로 반환해야 함.
"""

conversation_with_user_chain_prefix = """
1. target_npc_info의 설명을 참고하여 이름에 들어있는 등장인물로 답해야함.
2. 시놉시스와 시나리오를 참고하여 플래이어에게 대답해야함.
"""

conversation_between_npc_chain_prefix = """
1. 등장인물 설정을 참고하여 npc_name_1과 npc_name_2사이의 대화를 생성하야 함.
2. 플래이어와의 대화가 아니라 npc들 사이의 대화를 만들어야 함.
3. 시놉시스와 시나리오를 참고하여야함.
3. 등장인물 설정을 참고하여 힌트를 흘리는데 설정에 따라 가짜 힌트가 될 수도 있고 진짜 힌트가 될 수도 있음.
4. 대화는 3~4번 정도 주고 받고 답변의 형식은 npc_name_1 : , npc_name_2 : , ... 과 같은 형식이여야 함.
"""

conversation_chain_suffix = """
Human: {input}
AI Assistant:
"""

conversation_user_chain_suffix = """
{input}
AI Answer:
"""

intro_template = synopsis + intro_chain_prefix + conversation_chain_suffix
intro_prompt = PromptTemplate(template=intro_template, input_variables=["input"])

scenario_template = synopsis + characters + scenario_chain_prefix + conversation_chain_suffix
scenario_prompt = PromptTemplate(template=scenario_template, input_variables=["input"])

conversation_with_user_template = synopsis + conversation_with_user_chain_prefix + conversation_user_chain_suffix
conversation_with_user_prompt = PromptTemplate(template=conversation_with_user_template, input_variables=["input"])

conversation_between_npc_template = synopsis + characters + conversation_between_npc_chain_prefix + conversation_chain_suffix
conversation_between_npc_prompt = PromptTemplate(template=conversation_between_npc_template, input_variables=["input"])

# template = synopsis + conversation_chain_prefix + conversation_chain_suffix
# conversation_chain_prompt = PromptTemplate(template=template, input_variables=["input"])