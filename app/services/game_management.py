import random
from app.utils.data_loader import (
    load_npcs_data,
    load_features_data,
    load_personalities_data,
    load_places_data,
    load_weapons_data,
    load_times_data,
    load_names_data,
    load_wealth_data,
    load_scenarios_data
)
from app.utils.game_utils import get_name, get_weapon_name, get_location_name, get_time_name, get_personality_detail, get_feature_detail

# 개별 게임 상태 관리
class GameManagement:
    def __init__(self):
        self.npcs = load_npcs_data()["npcs"]
        self.features = load_features_data()["features"]
        self.personalities = load_personalities_data()["personalities"]
        self.places = load_places_data()["places"]
        self.weapons = load_weapons_data()["weapons"]
        self.times = load_times_data()["times"]
        self.names = load_names_data()["names"]
        self.wealth = load_wealth_data()["wealth"]
        self.scenarios = load_scenarios_data()["scenarios"]
        self.game_state = None

    # 새로운 게임을 초기화하는 메서드
    def initialize_game(self, language, characters, murderer):
        # characters와 murderer는 이제 NPC ID(영어)로 받음
        # 유효한 NPC ID 목록
        valid_npc_ids = [npc["name"] for npc in self.npcs]
        
        # 유효성 검사
        invalid_chars = [char for char in characters if char not in valid_npc_ids]
        if invalid_chars:
            raise ValueError(f"Invalid NPC IDs: {', '.join(invalid_chars)}")
        
        if murderer not in characters:
            raise ValueError(f"Murderer {murderer} is not in the character list")

        # 선택된 NPC 목록 생성
        selected_npcs = [npc for npc in self.npcs if npc["name"] in characters]
        murderer_npc = next((npc for npc in selected_npcs if npc["name"] == murderer), None)
        
        if murderer_npc is None:
            raise ValueError(f"Murderer {murderer} not found in NPC list")

        # 첫 번째 희생자 선택 (선택된 NPC 중 살인자가 아닌 사람)
        potential_victims = [npc for npc in selected_npcs if npc != murderer_npc]
        if not potential_victims:
            raise ValueError("Not enough NPCs for victim selection")
        
        murdered_npc = random.choice(potential_victims)

        # 무기를 랜덤으로 할당
        weapons = load_weapons_data()["weapons"]
        for npc in selected_npcs:
            npc["preferredWeapons"] = random.sample([weapon["id"] for weapon in weapons], min(3, len(weapons)))

        # 장소를 랜덤으로 할당
        places = load_places_data()["places"]
        for npc in selected_npcs:
            npc["preferredLocations"] = random.sample([place["id"] for place in places], min(3, len(places)))

        # 시간을 랜덤으로 할당
        times = load_times_data()["times"]
        for npc in selected_npcs:
            npc["preferredTimes"] = random.sample([time["id"] for time in times], min(3, len(times)))

        murder_weapon = random.choice(murderer_npc["preferredWeapons"])
        murder_location = random.choice(murderer_npc["preferredLocations"])
        murder_time = random.choice(murderer_npc["preferredTimes"])

        self.game_state = {
            "language": language,
            "suspects": selected_npcs,
            "murderer": murderer_npc,
            "murdered_npc": murdered_npc,
            "murder_weapon": murder_weapon,
            "murder_location": murder_location,
            "murder_time": murder_time,
            "conversations_left": 5,
            "npcs": selected_npcs,
            "places": self.places,
            "weapons": self.weapons,
            "conversations": [],
            "current_day": 1,
            "alive": {npc["name"]: (npc != murdered_npc) for npc in selected_npcs},
            "murdered_npcs": [{"name": murdered_npc["name"], "day": 1}],
            "interrogation": None
        }

        return self.game_state

    # 게임 상태를 반환하는 메서드
    def get_game_status(self):
        lang = self.game_state["language"]
        npc_info = [
            {
                "id": npc["name"],  # NPC ID (영어)
                "name": get_name(npc["name"], lang, self.names),  # 표시 이름 (언어별)
                "age": npc["age"],
                "gender": npc["gender"],
                "personality": get_personality_detail(npc["personality"], self.personalities, lang),
                "feature": get_feature_detail(npc["feature"], self.features, lang),
                "preferredWeapons": [get_weapon_name(weapon, self.weapons, lang) for weapon in npc["preferredWeapons"]],
                "preferredLocations": [get_location_name(location, self.places, lang) for location in npc["preferredLocations"]],
                "preferredTimes": [get_time_name(time, self.times, lang) for time in npc["preferredTimes"]],
                "alive": self.game_state['alive'][npc['name']],
                "alibi": self.game_state.get('alibis', {}).get(get_name(npc["name"], lang, self.names), "")
            }
            for npc in self.game_state["npcs"]
        ]
        murderer_info = {
            "id": self.game_state["murderer"]["name"],  # NPC ID (영어)
            "name": get_name(self.game_state["murderer"]["name"], lang, self.names),  # 표시 이름 (언어별)
            "age": self.game_state["murderer"]["age"],
            "gender": self.game_state["murderer"]["gender"],
            "personality": get_personality_detail(self.game_state["murderer"]["personality"], self.personalities, lang),
            "feature": get_feature_detail(self.game_state["murderer"]["feature"], self.features, lang)
        }
        murdered_npc_info = {
            "id": self.game_state["murdered_npc"]["name"],  # NPC ID (영어)
            "name": get_name(self.game_state["murdered_npc"]["name"], lang, self.names),  # 표시 이름 (언어별)
            "age": self.game_state["murdered_npc"]["age"],
            "gender": self.game_state["murdered_npc"]["gender"],
            "personality": get_personality_detail(self.game_state["murdered_npc"]["personality"], self.personalities, lang),
            "feature": get_feature_detail(self.game_state["murdered_npc"]["feature"], self.features, lang)
        }
        
        witness_info = self.game_state.get('witness', {})
        witness_name = witness_info.get('name', '')
        eyewitness_information = witness_info.get('information', '')
        
        return {
            "suspects": npc_info,
            "murderer": murderer_info,
            "murdered_npc": murdered_npc_info,
            "murder_weapon": get_weapon_name(self.game_state["murder_weapon"], self.weapons, lang),
            "murder_location": get_location_name(self.game_state["murder_location"], self.places, lang),
            "murder_time": get_time_name(self.game_state["murder_time"], self.times, lang),
            "current_day": self.game_state["current_day"],
            "alive": self.game_state["alive"],
            "murdered_npcs": self.game_state["murdered_npcs"],
            "witness": witness_name,
            "eyewitnessInformation": eyewitness_information
        }
