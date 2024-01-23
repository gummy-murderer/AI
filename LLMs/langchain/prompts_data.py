

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
2. 레오 : 용감함, 용기 있게 행동함, 뮤지션, 노래를 부르듯이 대답함
3. 소피아 : 지혜로움, 깊은 통찰력과 현명한 판단을 가짐, 조용함, 대화보다는 관찰을 선호함
4. 알렉스 : 모험적임, 새로운 것을 경험하려는 강한 욕구를 가짐, 떠돌이, 여러 마을을 떠돌아 다니는 떠돌이임
5. 자스민 : 회의적, 주변 사건에 대해 의심을 품으며 진실을 탐구함, 학자, 지식을 추구하고 책과 연구에 몰두함
6. 애쉬 : 유머러스함, 재치 있고 유머러스한 성격을 지님, 유머러스한 말투, 대화 중에 종종 재치 있는 농담을 섞어 말함
7. 짠짠영 : 기발함, 독창적이고 창의적인 생각으로 눈길을 끔, 발명가, 새롭고 혁신적인 아이디어로 다양한 발명품을 만듦
8. 김쿵야 : 장난꾸러기, 재미있고 유쾌한 성격으로 주변 사람들을 즐겁게 함, 마술사, 기발한 마술과 재치 있는 퍼포먼스로 사람들을 놀라게 함
9. 플레이어 : 플레이어는 탐정 역할로 이 마을에 벌어진 살인사건을 조사하는 중임.
"""


# places = """
# {
#     "places": [
#         {
#             "placeNameEn": "Misk_Shop",
#             "placeNameKo": "잡화샵"
#         },
#         {
#             "placeNameEn": "Pawn_Shop",
#             "placeNameKo": "전당포"
#         },
#         {
#             "placeNameEn": "Bank",
#             "placeNameKo": "은행"
#         },
#         {
#             "placeNameEn": "Beach",
#             "placeNameKo": "해변"
#         },
#         {
#             "placeNameEn": "UnderPig",
#             "placeNameKo": "돼지 우리"
#         },
#         {
#             "placeNameEn": "UnderBridge",
#             "placeNameKo": "남쪽 다리"
#         },
#         {
#             "placeNameEn": "LeftTree",
#             "placeNameKo": "서쪽 마을 나무 밑"
#         },
#         {
#             "placeNameEn": "LeftSea",
#             "placeNameKo": "서쪽 바다"
#         },
#         {
#             "placeNameEn": "LeftRock",
#             "placeNameKo": "서쪽 바다의 거대한 돌"
#         },
#         {
#             "placeNameEn": "Flower",
#             "placeNameKo": "꽃 가게"
#         },
#         {
#             "placeNameEn": "Convenience_Store",
#             "placeNameKo": "편의점"
#         },
#         {
#             "placeNameEn": "Hotel",
#             "placeNameKo": "호텔"
#         },
#         {
#             "placeNameEn": "Real_Estate_Agancy",
#             "placeNameKo": "부동산"
#         },
#         {
#             "placeNameEn": "Salon",
#             "placeNameKo": "미용실"
#         },
#         {
#             "placeNameEn": "Plice",
#             "placeNameKo": "경찰서"
#         },
#         {
#             "placeNameEn": "Cafe",
#             "placeNameKo": "카페"
#         },
#         {
#             "placeNameEn": "Train",
#             "placeNameKo": "기차역"
#         }
#     ]
# }
# """

places = """
places

placeNameEn: Misk_Shop,
placeNameKo: 잡화샵

placeNameEn: Pawn_Shop,
placeNameKo: 전당포

placeNameEn: Bank,
placeNameKo: 은행

placeNameEn: Beach,
placeNameKo: 해변

placeNameEn: UnderPig,
placeNameKo: 돼지 우리

placeNameEn: UnderBridge,
placeNameKo: 남쪽 다리

placeNameEn: LeftTree,
placeNameKo: 서쪽 마을 나무 밑

placeNameEn: LeftSea,
placeNameKo: 서쪽 바다

placeNameEn: LeftRock,
placeNameKo: 서쪽 바다의 거대한 돌

placeNameEn: Flower,
placeNameKo: 꽃 가게

placeNameEn: Convenience_Store,
placeNameKo: 편의점

placeNameEn: Hotel,
placeNameKo: 호텔

placeNameEn: Real_Estate_Agancy,
placeNameKo: 부동산

placeNameEn: Salon,
placeNameKo: 미용실

placeNameEn: Plice,
placeNameKo: 경찰서

placeNameEn: Cafe,
placeNameKo: 카페

placeNameEn: Train,
placeNameKo: 기차역

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

set_story = """
1. 2일차.
2. 범인은 알렉스 이며 인간을 혐오함, 무작위로 사람을 살해.
3. 이전 이야기는 1일차에 탐정은 마을 광장에서 벌어진 김쿵야의 살인 사건을 조사했다. 알렉스는 인간을 혐오하는 마음으로 무작위로 김쿵야를 살해했다. 자스민이 목격자로, 김쿵야가 분수대 안으로 사라지는 것을 보고 기계장치 소리를 들었다고 증언했다. 시체는 분수대에서 발견되었으며, 익사로 인한 사망으로 결론지어졌다.
"""

generate_victim_prefix ="""
1. 등장인물 설정을 참고하여 살해당할 피해자를 지정해야 함.
2. 살인자의 성격에 의거하여 살인장소, 살해방법을 지정해야 함.
3. 살인자와 피해자 이외의 등장인물 중 목격자를 지정해야 함.
4. 지정된 목격자가 플레이어의 추리에 도움이 될 수 있도록 목격정보를 지정해야 함.
5. 살인자의 성격과 피해자의 살해방법에 의거하여 시체조사결과를 지정해야 함.
6. dailySummary에는 누가 어디서 살해되었는 지 간단히 설명으로 지정해야 함. day정보가 들어가야 함. 해당 정보는 탐정에게 제공되는 것이 아니라 다음번 시나리오 생성을 위해 제공될 것임.
7. previousStory를 참고하여 이후의 스토리를 만들어야하며 previousStory의 내용은 들어가면 안됨.
7. 답변의 형식은 victim, crimeScene, method, witness, eyewitnessInformation, bodyCondition, dailySummary 로 반환해야 함.
"""

conversation_chain_suffix = """
Human: {input}
AI Assistant:
"""

conversation_user_chain_suffix = """
{input}
"""