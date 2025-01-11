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

    # NPC에게 질문을 생성하는 메서드
    def generate_questions(self, npc_name, keyword=None, keyword_type=None):
        if 'scenario' not in self.game_state:
            self.game_state['scenario'] = {}

        lang = self.game_state["language"]
        npc = next((npc for npc in self.game_state["npcs"] if get_name(npc["name"], lang, self.names) == npc_name), None)
        if not npc:
            raise ValueError("NPC not found")

        personality_key = npc["personality"]
        feature_key = npc["feature"]

        personality = next((p for p in self.personalities if p["id"] == personality_key), None)
        feature = next((f for f in self.features if f["id"] == feature_key), None)

        if personality is None or feature is None:
            raise ValueError("Personality or feature not found in NPC data")

        scenario_description = self.game_state["scenario"].get("description", "")

        question_prompt = ""

        # 무기에 대한 질문 생성
        if keyword_type == "weapon":
            weapon_name = get_weapon_name(keyword, self.weapons, lang)
            question_prompt = (
                f"Generate a concise question in {lang} for a player to ask an NPC named {npc_name} with the personality '{personality['personality'][lang]}' "
                f"and feature '{feature['feature'][lang]}'. The NPC is a suspect in the following scenario: {scenario_description}. "
                f"Ask them about their knowledge or possession of the weapon '{weapon_name}'."
            )
        # 장소에 대한 질문 생성
        elif keyword_type == "place":
            location_name = get_location_name(keyword, self.places, lang)
            question_prompt = (
                f"Generate a concise question in {lang} for a player to ask an NPC named {npc_name} with the personality '{personality['personality'][lang]}' "
                f"and feature '{feature['feature'][lang]}'. The NPC is a suspect in the following scenario: {scenario_description}. "
                f"Ask them about their connection to the location '{location_name}'."
            )
        # 시간에 대한 질문 생성
        elif keyword_type == "time":
            time_name = get_time_name(keyword, self.times, lang)
            question_prompt = (
                f"Generate a concise question in {lang} for a player to ask an NPC named {npc_name} with the personality '{personality['personality'][lang]}' "
                f"and feature '{feature['feature'][lang]}'. The NPC is a suspect in the following scenario: {scenario_description}. "
                f"Ask about their alibi or activities during the time '{time_name}'."
            )
        else:
            raise ValueError("Invalid keyword_type")

        question = self.clean_response(get_gpt_response(question_prompt, max_tokens=80))

        self.game_state["current_questions"] = question
        return question

    # NPC와 대화하는 메서드
    def talk_to_npc(self, npc_name, keyword=None, keyword_type=None):
        if "current_questions" not in self.game_state:
            raise ValueError("No questions generated")

        question = self.game_state["current_questions"]
        conversation_chain = get_conversation_chain()

        lang = self.game_state["language"]
        npc = next((npc for npc in self.game_state["npcs"] if get_name(npc["name"], lang, self.names) == npc_name), None)
        if not npc:
            raise ValueError("NPC not found")

        is_murderer = npc == self.game_state["murderer"]

        if 'scenario' not in self.game_state:
            self.game_state['scenario'] = {}

        scenario_description = self.game_state["scenario"].get("description", "")

        response_prompt = ""

        print("범인 여부 = ", is_murderer)

        # 무기에 대한 답변 생성
        if keyword_type == "weapon":
            weapon_name = get_weapon_name(keyword, self.weapons, lang)
            if keyword in npc["preferredWeapons"]:
                if is_murderer:
                    response_prompt = (
                        f"Generate a response in {lang} for the murderer NPC named {npc_name} with the personality '{npc['personality']}' "
                        f"and feature '{npc['feature']}'. The NPC is asked about the weapon '{weapon_name}' which they actually prefer. "
                        f"The response should show signs of nervousness, anger, or unusual behavior, subtly indicating their guilt. "
                        f"Their reaction should be consistent with their personality but noticeably different from their usual demeanor. "
                        f"However, they should not explicitly confirm their preference for the weapon."
                    )
                else:
                    response_prompt = (
                        f"Generate an enthusiastic response in {lang} for an innocent NPC named {npc_name} with the personality '{npc['personality']}' "
                        f"and feature '{npc['feature']}'. The NPC is asked about the weapon '{weapon_name}' which they genuinely like and use often. "
                        f"The response should clearly show their preference and excitement about this weapon. They might ask how the player knew about their preference "
                        f"or share a personal story related to the weapon."
                    )
            else:
                response_prompt = (
                    f"Generate a response in {lang} for an NPC named {npc_name} with the personality '{npc['personality']}' "
                    f"and feature '{npc['feature']}'. The NPC is asked about the weapon '{weapon_name}' which they dislike or rarely use. "
                    f"The response should clearly indicate their lack of preference for this weapon without mentioning any specific weapons they do prefer."
                )
        # 장소에 대한 답변 생성
        elif keyword_type == "place":
            location_name = get_location_name(keyword, self.places, lang)
            if keyword in npc["preferredLocations"]:
                if is_murderer:
                    response_prompt = (
                        f"Generate a response in {lang} for the murderer NPC named {npc_name} with the personality '{npc['personality']}' "
                        f"and feature '{npc['feature']}'. The NPC is asked about the location '{location_name}' which they actually prefer. "
                        f"The response should show signs of defensiveness, attempts to change the subject, or unusual behavior, subtly indicating their guilt. "
                        f"Their reaction should be consistent with their personality but noticeably different from their usual demeanor. "
                        f"However, they should not explicitly confirm their preference for the location."
                    )
                else:
                    response_prompt = (
                        f"Generate an excited response in {lang} for an innocent NPC named {npc_name} with the personality '{npc['personality']}' "
                        f"and feature '{npc['feature']}'. The NPC is asked about the location '{location_name}' which they genuinely like and visit often. "
                        f"The response should clearly show their fondness for this place. They might ask how the player knew about their preference "
                        f"or share a memorable experience they had at this location."
                    )
            else:
                response_prompt = (
                    f"Generate a response in {lang} for an NPC named {npc_name} with the personality '{npc['personality']}' "
                    f"and feature '{npc['feature']}'. The NPC is asked about the location '{location_name}' which they dislike or rarely visit. "
                    f"The response should clearly indicate their lack of preference for this place without mentioning any specific locations they do prefer."
                )
        # 시간에 대한 답변 생성
        elif keyword_type == "time":
            time_name = get_time_name(keyword, self.times, lang)
            if keyword in npc["preferredTimes"]:
                if is_murderer:
                    response_prompt = (
                        f"Generate a response in {lang} for the murderer NPC named {npc_name} with the personality '{npc['personality']}' "
                        f"and feature '{npc['feature']}'. The NPC is asked about their activities during '{time_name}', which is a time they are often active. "
                        f"The response should show signs of evasiveness, inconsistency, or unusual behavior, subtly indicating their guilt. "
                        f"Their reaction should be consistent with their personality but noticeably different from their usual demeanor. "
                        f"However, they should not explicitly confirm their preference for this time period."
                    )
                else:
                    response_prompt = (
                        f"Generate a cheerful response in {lang} for an innocent NPC named {npc_name} with the personality '{npc['personality']}' "
                        f"and feature '{npc['feature']}'. The NPC is asked about their activities during '{time_name}', which is a time they genuinely enjoy. "
                        f"The response should clearly show their preference for this time period. They might ask how the player knew about their schedule "
                        f"or share what they typically do during this time."
                    )
            else:
                response_prompt = (
                    f"Generate a response in {lang} for an NPC named {npc_name} with the personality '{npc['personality']}' "
                    f"and feature '{npc['feature']}'. The NPC is asked about their activities during '{time_name}', which is a time they are usually not active. "
                    f"The response should indicate their unfamiliarity with this time period without mentioning any specific times they prefer to be active."
                )
        else:
            response_prompt = (
                f"Generate a response in {lang} for an NPC named {npc_name} with the personality '{npc['personality']}' "
                f"and feature '{npc['feature']}'. The NPC is asked: '{question}'. The response should clearly reflect their personality and feature "
                f"without revealing any specific preferences for weapons, locations, or times."
            )

        response_content = self.clean_response(get_gpt_response(response_prompt, max_tokens=150))

        add_conversation(question, response_content)
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