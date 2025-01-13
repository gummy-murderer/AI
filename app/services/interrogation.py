import random
import json
import re
from pprint import pprint
from app.utils.gpt_helper import get_gpt_response
from app.utils.memory import add_conversation, get_conversation_chain
from app.utils.game_utils import (
    create_context,
    get_name,
    get_personality_detail,
    get_feature_detail,
    get_weapon_name,
    get_location_name
)
from app.core.logger_config import setup_logger
logger = setup_logger()

class Interrogation:
    def __init__(self, game_state, personalities, features, weapons, places, times, names):
        self.game_state = game_state
        self.personalities = personalities
        self.features = features
        self.weapons = weapons
        self.places = places
        self.times = times
        self.names = names

    def start_interrogation(self, npc_name, data):
        lang = self.game_state["language"]

        # Get NPC information
        npc = next((npc for npc in self.game_state["npcs"] if get_name(npc["name"], lang, self.names) == npc_name), None)
        murdered = next((npc for npc in self.game_state["npcs"] if npc["name"] == self.game_state["murdered_npc"]["name"]), None)
        
        # Get weapon, location, and time details
        weapon = next((weapon for weapon in self.weapons if weapon['weapon'][lang] == data['murder_weapon']), None)
        place = next((place for place in self.places if place['place'][lang] == data['murder_location']), None)
        time = next((time for time in self.times if time['time'][lang] == data['murder_time']), None)

        # Get names and details in current language
        interrogation_data = {
            "lang": lang,
            "npc": npc,
            "murdered": murdered,
            "weapon": weapon,
            "place": place,
            "time": time,
            "npc_name": get_name(npc["name"], lang, self.names),
            "victim_name": get_name(murdered["name"], lang, self.names),
            "weapon_name": weapon["weapon"][lang] if weapon else "",
            "location_name": place["place"][lang] if place else "",
            "time_name": time["time"][lang] if time else ""
        }

        # Calculate heart rate
        # heart_rate = 60
        heart_rate = 120

        if weapon['id'] == self.game_state['murder_weapon']:
            heart_rate += 20
        if place['id'] == self.game_state['murder_location']:
            heart_rate += 20
        if time['id'] == self.game_state['murder_time']:
            heart_rate += 20

        # Handle interrogation based on whether NPC is murderer
        if npc['name'] == self.game_state['murderer']['name']:
            if heart_rate >= 120:
                self.generate_confession(interrogation_data)
            else:
                # 자유질문
                pass
        else:
            if heart_rate >= 120:
                print("억울해 억울해")
                self.generate_innocence_claim(interrogation_data)
            else:
                # 자유질문
                pass


        # if npc is None:
        #     raise ValueError(f"NPC with name {npc_name} not found")

        # weapon = next((w for w in self.weapons if w['id'] == weapon_id), None) if weapon_id else None
        
        # weapon_name = weapon['weapon'][self.game_state["language"]] if weapon_id else None

        # if weapon_id in npc['preferredWeapons']:
        #     heart_rate = 80

        # self.game_state['interrogation'] = {
        #     "heart_rate": heart_rate,
        #     "suspect_name": npc_name,
        #     "weapon": weapon_id,  # 무기의 ID를 저장
        #     "weapon_name": weapon_name,  # 현재 언어로 된 무기 이름 저장
        #     "conversation_history": []
        # }

    # def generate_confession(self):
    #     pprint(self.game_state['murdered_npc'])
    #     pprint(self.game_state['murderer'])
    #     pprint(self.game_state['murder_weapon'])
    #     pprint(self.game_state['murder_location'])
    #     pprint(self.game_state['murder_time'])

    def generate_confession(self, data):
        confession_prompt = (
            f"Generate a single emotional confession in {data['lang']} as the suspect finally breaks down and confesses to the detective during interrogation.\n"
            f"Context:\n"
            f"- Suspect's name: {data['npc_name']}\n"
            f"- Suspect's personality: {data['npc']['personality']}\n"
            f"- Suspect's feature: {data['npc']['feature']}\n"
            f"- Victim's name: {data['victim_name']}\n"
            f"- Murder weapon: {data['weapon_name']}\n"
            f"- Murder location: {data['location_name']}\n"
            f"- Murder time: {data['time_name']}\n\n"
            f"Requirements:\n"
            f"- Write as a single emotional confession spoken directly to the detective\n"
            f"- Include emotional state but without script-style formatting or dialogue markers\n"
            f"- Reflect the murderer's personality and feature\n"
            f"- Explain both the motive and how they committed the murder\n"
            f"- Use natural spoken language showing distress"
        )

        confession = get_gpt_response(confession_prompt, max_tokens=200)
        print(f"\n[CONFESSION] {data['npc_name']}'s Confession:")
        print("=" * 50)
        print(confession)
        print("=" * 50)

    def generate_innocence_claim(self, data):
        innocence_prompt = (
            f"Generate an emotional plea of innocence in {data['lang']} from a suspect under intense interrogation who is actually innocent.\n"
            f"Context:\n"
            f"- Suspect's name: {data['npc_name']}\n"
            f"- Suspect's personality: {data['npc']['personality']}\n"
            f"- Suspect's feature: {data['npc']['feature']}\n"
            f"- Being accused of killing: {data['victim_name']}\n"
            f"- Suspected weapon: {data['weapon_name']}\n"
            f"- Crime location: {data['location_name']}\n"
            f"- Crime time: {data['time_name']}\n\n"
            f"Requirements:\n"
            f"- Express strong emotional distress and frustration at being falsely accused\n"
            f"- Provide a believable alibi or explanation for their innocence\n"
            f"- Show appropriate emotional reaction based on their personality and feature\n"
            f"- Include genuine confusion and hurt about being suspected\n"
            f"- Maintain a desperate but sincere tone\n"
            f"- Use natural spoken language as someone pleading their innocence"
        )

        innocence_claim = get_gpt_response(innocence_prompt, max_tokens=200)
        print(f"\n[INNOCENCE CLAIM] {data['npc_name']}'s Plea:")
        print("=" * 50)
        print(innocence_claim)
        print("=" * 50)

    def generate_interrogation_response(self, npc_name: str, content: str):
        logger.info(f"▶️  User message received: npc_name: {npc_name}, contents: {content}")

        npc = next((npc for npc in self.game_state["npcs"] if get_name(npc["name"], self.game_state["language"], self.names) == npc_name), None)

        conversation_history = self.game_state['interrogation']['conversation_history']
        formatted_conversation_history = "\n".join([f"{entry['role']}: {entry['content']}" for entry in conversation_history])

        current_heart_rate = self.game_state['interrogation']['heart_rate']
        # print(f"current_heart_rate: {current_heart_rate}")

        response_prompt = (
            f"Based on the conversation history below, generate a response in {self.game_state['language']} "
            f"for an NPC named {npc_name} who has the personality '{npc['personality']}' and the feature '{npc['feature']}'. "
            f"The NPC is currently being interrogated, accused of being the murderer in the village. "
            f"The NPC's current heart rate is {current_heart_rate} bpm. The NPC's heart rate changes depending on the sharpness of the question. "
            f"Sharp questions will increase the heart rate, while irrelevant questions will decrease it. "
            f"The change in heart rate (delta) ranges from -10 to +10 bpm but cannot be 0. The delta must be at least -1 or +1. "
            f"If the heart rate is below 80, respond in a dismissive and arrogant manner with a short answer. "
            f"If the heart rate is between 80 and 120, respond normally and cooperatively. "
            f"If the heart rate is above 120, refuse to answer and show signs of distress. "
            f"The response should clearly reflect their personality and feature. "
            f'The murdered person was {self.game_state["murdered_npc"]}, the murder weapon was {self.game_state["murder_weapon"]}, and the murder took place at {self.game_state["murder_location"]}. '
            f'Provide the response in the format(json): {{"response": str, "heartRateDelta": int}}\n\n'
            f"Conversation History:\n{formatted_conversation_history}\n\n"
            f"The NPC is asked: '{content}'"
        )

        response_content = get_gpt_response(response_prompt, max_tokens=150)
    
        # JSON 파싱 시도
        try:
            response = json.loads(response_content)
        except json.JSONDecodeError:
            # JSON 파싱에 실패한 경우, 정규 표현식을 사용하여 필요한 정보 추출
            response_match = re.search(r'"response"\s*:\s*"(.+?)"', response_content)
            delta_match = re.search(r'"heartRateDelta"\s*:\s*(-?\d+)', response_content)
            
            if response_match and delta_match:
                response = {
                    "response": response_match.group(1),
                    "heartRateDelta": int(delta_match.group(1))
                }
            else:
                # 정규 표현식으로도 추출 실패 시 기본값 설정
                response = {
                    "response": "미안해. 무슨 말인지 모르겠어.",
                    "heartRateDelta": 0
                }
        
        # 심박수 변화 적용
        current_heart_rate += int(response['heartRateDelta'])
        current_heart_rate = min(max(current_heart_rate, 60), 130)
        self.game_state['interrogation']['heart_rate'] = current_heart_rate

        # 대화 기록 추가
        conversation_history.append({"role": "user", "content": content})
        conversation_history.append({"role": npc_name, "content": response['response']})

        logger.info(f"▶️  Bot response sent: npc_name: {npc_name}, heart_rate: {current_heart_rate}, response: {response['response']}")
        return {"response": response['response'], "heartRate": current_heart_rate}
