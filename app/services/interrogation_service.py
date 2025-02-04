from fastapi import HTTPException
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
    get_location_name,
    get_time_name
)
from app.core.logger_config import setup_logger
logger = setup_logger()

class InterrogationService:
    def __init__(self, game_state, personalities, features, weapons, places, times, names):
        self.game_state = game_state
        self.personalities = personalities
        self.features = features
        self.weapons = weapons
        self.places = places
        self.times = times
        self.names = names
    
    def interrogation(self, npc_name: str, start_data: dict = None, content: str = None) -> dict:
        """
        취조 메인 로직을 정의합니다. 필요 시 새로운 취조 데이터를 만들고 심박수에 따라 답변을 생성합니다.
        Args:
            npc_name (str): 취조 대상이 되는 npc 이름
            start_data (dict): 취조 생성 시 필요한 데이터
            content(str): 자유 대화 시 유저 입력 값값
        Returns:
            dict: 취조에 대한 response 데이터
        """
        # 취조 시작 데이터 생성
        if start_data:
            print("new game!")
            logger.info(f"✨ New interrogation started with npc_name: {npc_name}")

            self.new_interrogation(npc_name, start_data)

        interrogation_data: dict = self.game_state['interrogation']
        if not interrogation_data:
            raise HTTPException(status_code=404, detail="Interrogation not found")

        is_murderer = interrogation_data["is_murderer"]
        heart_rate = interrogation_data["heart_rate"]

        # 심박수와 범인 여부에 따른 행동 구분
        # 초기 대화일 때
        if start_data:
            if is_murderer:
                if heart_rate >= 120:
                    confession = self.generate_confession(interrogation_data)
                    interrogation_data.update({
                        "status": "CONFESSION",
                        "response": confession
                    })
                else:
                    initial_response = self.generate_initial_response(interrogation_data)
                    # initial_response = self.generate_interrogation_response(interrogation_data)
                    interrogation_data.update({
                        "status": "CONTINUE",
                        "response": initial_response
                    })
            else:
                if heart_rate >= 120:
                    innocence_claim = self.generate_innocence_claim(interrogation_data, content)
                    interrogation_data.update({
                        "status": "INNOCENT_PROTEST",
                        "response": innocence_claim
                    })
                else:
                    initial_response = self.generate_initial_response(interrogation_data)
                    interrogation_data.update({
                        "status": "CONTINUE",
                        "response": initial_response
                    })
        # 자유 대화 중일 때
        else:
            if is_murderer:
                if heart_rate >= 120:
                    confession = self.generate_confession(interrogation_data)
                    interrogation_data.update({
                        "status": "CONFESSION",
                        "response": confession
                    })
                else:
                    initial_response = self.generate_interrogation_response(interrogation_data)
                    interrogation_data.update({
                        "status": "CONTINUE",
                        "response": initial_response
                    })
            else:
                if heart_rate >= 120:
                    innocence_claim = self.generate_innocence_claim(interrogation_data)
                    interrogation_data.update({
                        "status": "INNOCENT_PROTEST",
                        "response": innocence_claim
                    })
                else:
                    initial_response = self.generate_interrogation_response(interrogation_data)
                    interrogation_data.update({
                        "status": "CONTINUE",
                        "response": initial_response
                    })

        # 대화 내용 저장
        interrogation_data["conversation_history"].append({"role": npc_name, "content": interrogation_data["response"]})

        # print("="*50)
        # from pprint import pprint
        # pprint(self.game_state['interrogation'])
        # print("="*50)

        logger.info(f"▶️  Interrogation with npc_name: {npc_name}, status: {interrogation_data['status']}")

        return {
            "npc_name": npc_name,
            "status": interrogation_data["status"],
            "is_murderer": interrogation_data["is_murderer"],
            "heart_rate": interrogation_data["heart_rate"],
            "response": interrogation_data["response"]
        }

    def new_interrogation(self, npc_name: str, data: dict):
        """
        취조 생성 시 필요한 데이터를 정리/저장합니다.
        Args:
            npc_name (str): 취조 대상이 되는 npc 이름
            data (dict): user input 값
        Returns:
            dict: 취조 데이터를 가지고 있는 response 데이터
        """
        lang = self.game_state["language"]

        # Get NPC information
        npc = next((npc for npc in self.game_state["npcs"] if get_name(npc["name"], lang, self.names) == npc_name), None)
        murdered = next((npc for npc in self.game_state["npcs"] if npc["name"] == self.game_state["murdered_npc"]["name"]), None)
        
        # Get weapon, location, and time details
        weapon = next((weapon for weapon in self.weapons if weapon['id'] == data['murder_weapon']), None)
        place = next((place for place in self.places if place['id'] == data['murder_location']), None)
        time = next((time for time in self.times if time['id'] == data['murder_time']), None)

        is_murderer = npc['name'] == self.game_state['murderer']['name']

        # Calculate heart rate
        heart_rate = 60

        if weapon['id'] == self.game_state['murder_weapon']:
            heart_rate += 20
        if place['id'] == self.game_state['murder_location']:
            heart_rate += 20
        if time['id'] == self.game_state['murder_time']:
            heart_rate += 20

        interrogation_data = {
            "lang": lang,
            "status": "CONTINUE",
            "is_murderer": is_murderer,
            "heart_rate": heart_rate,
            "npc_name": get_name(npc["name"], lang, self.names),
            "victim_name": get_name(murdered["name"], lang, self.names),
            "weapon_name": weapon["weapon"][lang] if weapon else "",
            "location_name": place["place"][lang] if place else "",
            "time_name": time["time"][lang] if time else "",
            "details": {
                "npc": npc,
                "murdered": murdered,
                "weapon": weapon,
                "place": place,
                "time": time,
            },
            "suspect_name": npc_name,
            "conversation_history": [],
            "response": None
        }

        self.game_state['interrogation'] = interrogation_data
        logger.info(f"▶️  Interrogation started with npc_name: {npc_name}, status: {interrogation_data['status']}")
        return interrogation_data

    def _clean_response(self, response: str) -> str:
        """
        생성한 답변의 형식을 깔끔하게 정리합니다.
        Args:
            response (str): ai로 생성한 문장
        Returns:
            str: 정규식으로 정리한 문장
        """
        cleaned_response = response.strip()
        cleaned_response = re.sub(r'^\"|\"$', '', cleaned_response)
        cleaned_response = re.sub(r'“,”$', '', cleaned_response)
        return cleaned_response

    def generate_initial_response(self, data: dict) -> str:
        """
        취조 시작 시 간단한 시작 대화를 생성합니다.
        Args:
            data (dict): 취조에서 사용되는 범인, 무기, 장소 등의 정보
        Return:
            str: 생성된 ai 답변
        """
        prompt = (
            f"Generate a single short response in {data['lang']} from a suspect during interrogation.\n"
            f"Context:\n"
            f"- Suspect's name: {data['npc_name']}\n"
            f"- Suspect's personality: {data['details']['npc']['personality']}\n"
            f"- Suspect's feature: {data['details']['npc']['feature']}\n"
            f"Requirements:\n"
            f"- Keep it very short (1-2 sentences)\n"
            f"- Show slight nervousness but willingness to talk\n"
            f"- Match the character's personality and feature\n"
            f"- Use natural spoken language"
        )
        response = get_gpt_response(prompt, max_tokens=50)
        return self._clean_response(response)

    def generate_confession(self, data: dict) -> str:
        """
        범인의 자백을 생성합니다.
        Args:
            data (dict): 취조에서 사용되는 범인, 무기, 장소 등의 정보
        Return:
            str: 생성된 ai 답변
        """
        confession_prompt = (
            f"Generate a single emotional confession in {data['lang']} as the suspect finally breaks down and confesses to the detective during interrogation.\n"
            f"Context:\n"
            f"- Suspect's name: {data['npc_name']}\n"
            f"- Suspect's personality: {data['details']['npc']['personality']}\n"
            f"- Suspect's feature: {data['details']['npc']['feature']}\n"
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
        return self._clean_response(confession)

    def generate_innocence_claim(self, data: dict) -> str:
        """
        무고한 시민의 억울함 호소를 생성합니다.
        Args:
            data (dict): 취조에서 사용되는 범인, 무기, 장소 등의 정보
        Return:
            str: 생성된 ai 답변
        """
        innocence_prompt = (
            f"Generate an emotional plea of innocence in {data['lang']} from a suspect under intense interrogation who is actually innocent.\n"
            f"Context:\n"
            f"- Suspect's name: {data['npc_name']}\n"
            f"- Suspect's personality: {data['details']['npc']['personality']}\n"
            f"- Suspect's feature: {data['details']['npc']['feature']}\n"
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
        return self._clean_response(innocence_claim)

    # =============================================================================================================================

    def generate_interrogation_response(self, data: dict, content: str = ""):
        npc_name = data["npc_name"]
        logger.info(f"▶️  User message received: npc_name: {npc_name}, contents: {content}")

        npc = next((npc for npc in self.game_state["npcs"] if get_name(npc["name"], self.game_state["language"], self.names) == npc_name), None)

        conversation_history = self.game_state['interrogation']['conversation_history']
        formatted_conversation_history = "\n".join([f"{entry['role']}: {entry['content']}" for entry in conversation_history])

        current_heart_rate = self.game_state['interrogation']['heart_rate']

        response_prompt = (
            f"Based on the conversation history below, generate a response in {self.game_state['language']} "
            f"for an NPC named {npc_name} who has the personality '{npc['personality']}' and the feature '{npc['feature']}'. "
            f"The NPC is currently being interrogated, accused of being the murderer in the village. "
            f"The NPC's current heart rate is {current_heart_rate} bpm. The NPC's heart rate changes depending on the sharpness of the question. "
            f"Sharp and accusatory questions will increase the heart rate (1), while irrelevant or casual questions will decrease it (-1). "
            f"If the question is neutral, maintain the current heart rate (0). "
            f"If the heart rate is below 80, respond in a dismissive and arrogant manner with a short answer. "
            f"If the heart rate is between 80 and 120, respond normally and cooperatively. "
            f"If the heart rate is above 120, refuse to answer and show signs of distress. "
            f"The response should clearly reflect their personality and feature. "
            f'The murdered person was {self.game_state["murdered_npc"]}, the murder weapon was {self.game_state["murder_weapon"]}, and the murder took place at {self.game_state["murder_location"]}. '
            f'Provide the response in the format(json): {{"response": str, "heartRateChange": int}}\n\n'
            f"Note: heartRateChange must be one of these values: -1 (decrease), 0 (maintain), 1 (increase)\n\n"
            f"Conversation History:\n{formatted_conversation_history}\n\n"
            f"The NPC is asked: '{content}'"
        )

        response_content = get_gpt_response(response_prompt, max_tokens=150)
    
        # JSON 파싱 시도
        try:
            response = json.loads(response_content)
            # heartRateChange 값이 -1, 0, 1 중 하나인지 확인
            if response['heartRateChange'] not in [-1, 0, 1]:
                response['heartRateChange'] = 0
        except json.JSONDecodeError:
            # JSON 파싱에 실패한 경우, 정규 표현식을 사용하여 필요한 정보 추출
            response_match = re.search(r'"response"\s*:\s*"(.+?)"', response_content)
            change_match = re.search(r'"heartRateChange"\s*:\s*(-?\d+)', response_content)
            
            if response_match and change_match:
                change_value = int(change_match.group(1))
                # 값을 -1, 0, 1 범위로 제한
                if change_value < -1:
                    change_value = -1
                elif change_value > 1:
                    change_value = 1
                
                response = {
                    "response": response_match.group(1),
                    "heartRateChange": change_value
                }
            else:
                # 정규 표현식으로도 추출 실패 시 기본값 설정
                response = {
                    "response": "미안해. 무슨 말인지 모르겠어.",
                    "heartRateChange": 0
                }
        
        # 심박수 변화 적용
        heart_rate_delta = response['heartRateChange'] * 10  # -1 → -10, 0 → 0, 1 → 10
        current_heart_rate += heart_rate_delta
        current_heart_rate = min(max(current_heart_rate, 60), 120)
        self.game_state['interrogation']['heart_rate'] = current_heart_rate
        self.game_state['interrogation']['heart_rate'] = 120

        # 대화 기록 추가
        conversation_history.append({"role": "user", "content": content})
        conversation_history.append({"role": npc_name, "content": response['response']})

        logger.info(f"▶️  Bot response sent: npc_name: {npc_name}, heart_rate_delta: {heart_rate_delta}, current_heart_rate: {current_heart_rate}, response: {response['response']}")
        # return {"response": response['response'], "heartRate": current_heart_rate}
        return response['response']
