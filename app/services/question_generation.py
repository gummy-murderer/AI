import random
import re
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

class QuestionGeneration:
    # 초기화 메서드
    def __init__(self, game_state, personalities, features, weapons, places, times, names):
        self.game_state = game_state
        self.personalities = personalities
        self.features = features
        self.weapons = weapons
        self.places = places
        self.times = times
        self.names = names

    def talk_to_npc(self, npc_name, keyword=None, keyword_type=None):
        if 'scenario' not in self.game_state:
            self.game_state['scenario'] = {}
        
        lang = self.game_state["language"]
        npc = next((npc for npc in self.game_state["npcs"] if get_name(npc["name"], lang, self.names) == npc_name), None)
        if not npc:
            raise ValueError("NPC not found")

        is_murderer = npc == self.game_state["murderer"]
        scenario_description = self.game_state["scenario"].get("description", "")
        response_prompt = ""

        # 무기에 대한 답변 생성
        if keyword_type == "weapon":
            weapon_name = get_weapon_name(keyword, self.weapons, lang)
            if keyword in npc["preferredWeapons"]:
                if is_murderer:
                    response_prompt = (
                        f"Generate a brief response in {lang} (without any greeting) for an NPC named {npc_name} with the personality '{npc['personality']}' "
                        f"and feature '{npc['feature']}' about the weapon '{weapon_name}'. Start directly with their opinion or experience. "
                        f"They frequently use and really like this weapon, but should show slight nervousness or defensiveness when talking about it. "
                        f"Make them either overexplain their legitimate reasons for using it or try to downplay their expertise with it. "
                        f"Keep their personality traits consistent while showing this subtle unease."
                    )
                else:
                    response_prompt = (
                        f"Generate a brief response in {lang} (without any greeting) for an NPC named {npc_name} with the personality '{npc['personality']}' "
                        f"and feature '{npc['feature']}' about the weapon '{weapon_name}'. Start directly with their opinion or experience. "
                        f"They should enthusiastically express their fondness for this weapon, mentioning either recent use, "
                        f"how often they use it, or why they prefer it. Their excitement should match their personality."
                    )
            else:
                response_prompt = (
                    f"Generate a brief response in {lang} (without any greeting) for an NPC named {npc_name} with the personality '{npc['personality']}' "
                    f"and feature '{npc['feature']}' about the weapon '{weapon_name}'. Start directly with their opinion or experience. "
                    f"They strongly dislike or never use this weapon. Have them explain in detail (2-3 sentences) why they avoid it, "
                    f"including both their emotional reaction to it and a specific past experience or practical reason. "
                    f"Their explanation should clearly reflect their personality traits."
                )

        # 장소에 대한 답변 생성
        elif keyword_type == "place":
            location_name = get_location_name(keyword, self.places, lang)
            if keyword in npc["preferredLocations"]:
                if is_murderer:
                    response_prompt = (
                        f"Generate a brief response in {lang} (without any greeting) for an NPC named {npc_name} with the personality '{npc['personality']}' "
                        f"and feature '{npc['feature']}' about the location '{location_name}'. Start directly with their opinion or experience. "
                        f"They frequently visit and like this place, but should become slightly evasive or contradictory when discussing recent visits. "
                        f"Make them either change details about when they were last there or become overly specific about unimportant details. "
                        f"Keep their personality traits consistent while showing this subtle unease."
                    )
                else:
                    response_prompt = (
                        f"Generate a brief response in {lang} (without any greeting) for an NPC named {npc_name} with the personality '{npc['personality']}' "
                        f"and feature '{npc['feature']}' about the location '{location_name}'. Start directly with their opinion or experience. "
                        f"They should clearly express their attachment to this place, mentioning either a recent visit, "
                        f"how often they go there, or why they love it. Their enthusiasm should match their personality."
                    )
            else:
                response_prompt = (
                    f"Generate a brief response in {lang} (without any greeting) for an NPC named {npc_name} with the personality '{npc['personality']}' "
                    f"and feature '{npc['feature']}' about the location '{location_name}'. Start directly with their opinion or experience. "
                    f"They actively avoid or strongly dislike this place. Have them explain in detail (2-3 sentences) their aversion, "
                    f"including both their emotional response to the place and a specific memory or practical reason they avoid it. "
                    f"Their explanation should clearly reflect their personality traits."
                )

        # 시간에 대한 답변 생성
        elif keyword_type == "time":
            time_name = get_time_name(keyword, self.times, lang)
            if keyword in npc["preferredTimes"]:  # 깨어있던 시간
                if is_murderer:
                    response_prompt = (
                        f"Generate a brief response in {lang} (without any greeting) for an NPC named {npc_name} with the personality '{npc['personality']}' "
                        f"and feature '{npc['feature']}' about their activities during '{time_name}'. Start directly with their opinion or experience. "
                        f"They were awake at this time. Include one subtle suspicious element: either a small inconsistency "
                        f"in their story, a slight hesitation, or an unnecessarily defensive tone. "
                        f"Keep the response natural and matching their personality, with just a hint that something might be off."
                    )
                else:
                    response_prompt = (
                        f"Generate a brief response in {lang} (without any greeting) for an NPC named {npc_name} with the personality '{npc['personality']}' "
                        f"and feature '{npc['feature']}' about their activities during '{time_name}'. Start directly with their opinion or experience. "
                        f"They were awake and doing their usual activities. Include one or two specific but mundane details "
                        f"that match their personality and daily routine."
                    )
            else:  # 자고 있던 시간
                if is_murderer:
                    response_prompt = (
                        f"Generate a brief response in {lang} (without any greeting) for an NPC named {npc_name} with the personality '{npc['personality']}' "
                        f"and feature '{npc['feature']}' about '{time_name}'. Start directly with their opinion or experience. "
                        f"They claim to have been sleeping, but their response should be detailed (2-3 sentences). Include their usual sleep routine, "
                        f"a small detail that seems slightly off - like being unusually specific about their sleep time, "
                        f"and perhaps a comment about why they need their rest at this time. Keep it subtle and natural to their personality."
                    )
                else:
                    response_prompt = (
                        f"Generate a brief response in {lang} (without any greeting) for an NPC named {npc_name} with the personality '{npc['personality']}' "
                        f"and feature '{npc['feature']}' about '{time_name}'. Start directly with their opinion or experience. "
                        f"They were sleeping at this time. Have them explain in detail (2-3 sentences) about their sleep habits, "
                        f"including their usual bedtime routine, why they prefer sleeping at this time, and how it fits with their daily schedule. "
                        f"Their explanation should naturally reflect their personality."
                    )
        else:
            raise ValueError("Invalid keyword_type")

        response_content = self.clean_response(get_gpt_response(response_prompt, max_tokens=150))
        
        # 대화 기록 추가 및 남은 대화 횟수 감소
        add_conversation(f"{keyword_type}: {keyword}", response_content)
        self.game_state["conversations_left"] -= 1

        return response_content

    # 응답을 정리하는 메서드
    def clean_response(self, response):
        # 쌍따옴표 제거
        response = response.replace('"', '')
        
        # NPC 이름과 콜론 제거 (예: "태근티비: " 제거)
        response = re.sub(r'^[^:]+:\s*', '', response)
        
        # 앞뒤 공백 제거
        response = response.strip()
        
        return response