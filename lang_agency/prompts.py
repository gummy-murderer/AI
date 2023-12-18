from langchain.prompts.prompt import PromptTemplate


# specifier_chain
# specifier_chain_prefix = """
# 1. 사용자의 입력과 current_time을 분석하여 일정의 구성 요소를 추정합니다.
# 2. 일정의 구성 요소에는 "schedule_management_type", "schedule_content", "members", "year", "month", "date", "hour", "minute"가 포함되어야 합니다.
# 3. "year", "month", "date", "hour", "minute"의 값은 숫자입니다.
# 4. 'members'의 값은 일정에 참여하는 개인의 이름을 담은 배열이며, 현재 대화 상에서 사용자의 이름이 기본적으로 포함됩니다. 챗봇의 이름은 포함되지 않습니다.
# 5. 일정 관리의 유형은 "create", "retrieve,", "update", 또는 "delete" 중 하나입니다.
# 6. 출력 형식은 "schedule_management_type", "schedule_content", "members", "year", "month", "date", "hour", "minute", "next_action"을 포함한 JSON 형식의 문자열입니다.
# 7. 사용자의 입력에서 추정할 수 없는 요소가 있다면 해당 요소의 값은 null이 됩니다.
# 8. 일정 구성 요소 중 null인 요소가 없다면 "next_action"은 "schedule_management"이 됩니다.
# 9. 일정 구성 요소 중 null인 요소가 있거나 "현재 시간"에서 추정된 요소가 있다면 "next_action"은 "general_conversation"이 됩니다.
# """

# specifier_chain_suffix = """
# Human: {input}
# AI Assistant:
# """

# template = specifier_chain_prefix + specifier_chain_suffix
# specifier_chain_prompt = PromptTemplate(template=template, input_variables=["input"])

# general_conversation_chain
conversation_chain_prefix = """
시놉시스
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

1. 해당 시놉시스를 이용해서 마을의 촌장이 탐정에게 처음 상황을 설명하듯이 답변을 반말로 생성해야 함.
"""

conversation_chain_suffix = """
Human: {input}
AI Assistant:
"""

template = conversation_chain_prefix + conversation_chain_suffix
conversation_chain_prompt = PromptTemplate(template=template, input_variables=["input"])