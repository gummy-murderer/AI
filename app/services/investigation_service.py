from app.utils.game_utils import (
    get_name,
    get_weapon_name,
    get_location_name,
    get_time_name
)
from app.utils.gpt_helper import get_gpt_response
import random

class InvestigationService:
    def __init__(self, game_state, weapons, places, times, names):
        self.game_state = game_state
        self.weapons = weapons
        self.places = places
        self.times = times
        self.names = names

    def _generate_time_analysis(self, victim_name: str, time_name: str, lang: str) -> str:
        """
        시체의 상태를 통해 사망 시각을 추리하는 내용을 생성합니다
        """
        prompt = f"""You are a detective bear examining a murder victim's body to determine time of death.
The victim {victim_name} was found, and based on initial reports, the estimated time of death is around {time_name}.

Create a brief monologue where you deduce the time of death by examining:
- Body temperature
- Rigor mortis (stiffness)
- Other physical signs

Start with a thoughtful interjection like {"'흠...', '음...'" if lang == 'ko' else "'Hmm...', 'Well...'"}.
Keep it to 1-2 natural, conversational sentences focused on confirming the time of death through observation.

Response MUST be in {'Korean' if lang == 'ko' else 'English'} ONLY."""
        return get_gpt_response(prompt, max_tokens=100)

    def _generate_method_analysis(self, victim_name: str, weapon_name: str, lang: str) -> str:
        """시체의 상처를 통해 살해 도구를 추리하는 내용을 생성합니다"""
        prompt = f"""You are a detective bear examining wounds on a murder victim's body.
The victim is {victim_name}, and through your analysis, you need to deduce that the murder weapon was {weapon_name}.

Create a brief monologue where you:
1. First describe the wound characteristics (shape, depth, pattern, impact force)
2. Then make a logical deduction about the specific weapon type
3. Finally confirm it was {weapon_name}

Start with a thoughtful interjection like {"'음...', '으음...'" if lang == 'ko' else "'Well...', 'Let's see...'"}.
Keep it to 1-2 natural, conversational sentences showing your deductive process.

Response MUST be in {'Korean' if lang == 'ko' else 'English'} ONLY."""
        return get_gpt_response(prompt, max_tokens=100)

    def _generate_scene_analysis(self, victim_name: str, location_name: str, time_name: str, lang: str) -> str:
        """
        범행 현장과 정황을 추리하고 다음 수사 단계를 결정하는 내용을 생성합니다
        """
        # 생존해 있는 NPC 목록 가져오기
        alive_npcs = [
            get_name(npc["name"], lang, self.names)
            for npc in self.game_state["npcs"]
            if self.game_state["alive"].get(npc["name"], False)
        ]

        # 대화할 NPC 1-2명을 무작위로 선택 (생존자가 있는 경우)
        npcs_to_question = []
        if alive_npcs:
            num_npcs = min(2, len(alive_npcs))
            npcs_to_question = random.sample(alive_npcs, num_npcs)

        prompt = f"""You are a detective bear analyzing a murder scene in your bear village.
The victim {victim_name} was found at {location_name}, and the estimated time of death is {time_name}.

Create a brief monologue where you:
1. Explicitly mention the specific location ({location_name}) while questioning why the victim was there
2. Consider who among the surviving villagers might have useful information
3. Specifically mention you should talk to {' and '.join(npcs_to_question) if npcs_to_question else 'any surviving bears'}

Start with a thoughtful interjection like {"'흠...', '그런데...'" if lang == 'ko' else "'Hmm...', 'Now...'"}.
Keep it to 1-2 natural, conversational sentences that must include the specific location name.
Remember this is a bear village - all residents are bears, and modern investigation methods aren't available.

Response MUST be in {'Korean' if lang == 'ko' else 'English'} ONLY."""
        return get_gpt_response(prompt, max_tokens=100)

    def investigate_corpse(self) -> dict:
        """
        현재 날짜의 피해자 시체를 조사하여 범행 정보를 반환합니다.
        
        Returns:
            dict: 피해자, 범행 시간, 장소, 도구 정보와 탐정의 조사 보고를 포함한 딕셔너리
        """
        lang = self.game_state["language"]
        current_day = self.game_state["current_day"]
        
        # 현재 날짜의 피해자 찾기
        victim = next(
            (npc for npc in self.game_state["murdered_npcs"] 
             if npc.get("day", 1) == current_day),
            None
        )
        
        if not victim:
            raise ValueError(f"No victim found for day {current_day}")
            
        # 해당 날짜의 범행 정보 가져오기
        murder_weapon = self.game_state["murder_weapons"][current_day - 1] if "murder_weapons" in self.game_state else self.game_state["murder_weapon"]
        murder_location = self.game_state["murder_locations"][current_day - 1] if "murder_locations" in self.game_state else self.game_state["murder_location"]
        murder_time = self.game_state["murder_times"][current_day - 1] if "murder_times" in self.game_state else self.game_state["murder_time"]
        
        victim_name = get_name(victim["name"], lang, self.names)
        weapon_name = get_weapon_name(murder_weapon, self.weapons, lang)
        location_name = get_location_name(murder_location, self.places, lang)
        time_name = get_time_name(murder_time, self.times, lang)
        
        # 각 부분별 분석 생성
        time_analysis = self._generate_time_analysis(victim_name, time_name, lang)
        method_analysis = self._generate_method_analysis(victim_name, weapon_name, lang)
        scene_analysis = self._generate_scene_analysis(victim_name, location_name, time_name, lang)
        
        return {
            "victim": victim_name,
            "crimeTime": time_name,
            "crimeScene": location_name,
            "method": weapon_name,
            "investigationReport": {
                "timeAnalysis": time_analysis,
                "methodAnalysis": method_analysis,
                "sceneAnalysis": scene_analysis
            }
        } 