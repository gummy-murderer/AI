from app.utils.game_utils import (
    get_name,
    get_weapon_name,
    get_location_name,
    get_time_name
)
from app.utils.gpt_helper import get_gpt_response

class InvestigationService:
    def __init__(self, game_state, weapons, places, times, names):
        self.game_state = game_state
        self.weapons = weapons
        self.places = places
        self.times = times
        self.names = names

    def investigate_corpse(self) -> dict:
        """
        현재 날짜의 피해자 시체를 조사하여 범행 정보를 반환합니다.
        
        Returns:
            dict: 범행 시간, 장소, 도구 정보와 탐정의 조사 보고를 포함한 딕셔너리
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
        
        # GPT를 사용하여 탐정스러운 조사 보고서 생성
        investigation_prompt = f"""You are a detective bear investigating a murder case in a village where only bears live.
The victim {victim_name} was found at {location_name}. The time of death appears to be around {time_name}.

Create an investigation report as if you're thinking aloud to yourself while examining the body.
Your response must be ONLY in {'Korean' if lang == 'ko' else 'English'} language.

Please follow this thought process in your monologue:
1. Start with thoughtful interjections like {"'흠...', '음...'" if lang == 'ko' else "'Hmm...', 'Well...'"} and maintain a conversational tone
2. First, look at the body temperature and stiffness to confirm the time of death
3. Then, examine the wounds and injuries to deduce what kind of weapon was used:
   - First describe the wounds and what they suggest (shape, size, force of impact)
   - Then conclude by specifically identifying the weapon as {weapon_name}
4. Consider why the victim was at this location at such a time
5. End with a casual mention of which bear villagers you should talk to next

Write 2-3 sentences in a natural, stream-of-consciousness style. The deductions should flow naturally from your observations.
Remember this is a village of bears - all residents and suspects are bears.

Important:
- Use casual, self-talking style (avoid formal language)
- First describe wounds, then conclude with the specific weapon
- Always refer to villagers/residents as bears
- Response MUST be in {'Korean' if lang == 'ko' else 'English'} ONLY

Example wound analysis style in {'Korean' if lang == 'ko' else 'English'}:
{'''
"이 깊은 원형 자국을 보니... 무겁고 둥근 걸로 맞았군... 아, 돌망치로 맞은 거야."
"이렇게 넓게 멍이 들었네... 넓은 면으로 가격당했어... 밀대가 분명해."
''' if lang == 'ko' else '''
"These deep, circular marks... must have been hit with something heavy and round... ah, a stone hammer for sure."
"Such wide bruising... struck with something flat and broad... definitely a mop handle."
'''}
"""
        
        investigation_report = get_gpt_response(investigation_prompt, max_tokens=200)
        
        return {
            "victim": victim_name,
            "crimeTime": time_name,
            "crimeScene": location_name,
            "method": weapon_name,
            "investigationReport": investigation_report
        } 