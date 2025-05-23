from fastapi import HTTPException
import random
from typing import List
from app.schemas import game_schema
from app.services.game_management import GameManagement
from app.services.question_generation import QuestionGeneration
from app.services.hint_investigation import HintInvestigation
from app.services.scenario_generation import ScenarioGeneration

from app.services.interrogation import Interrogation
from app.services.interrogation_service import InterrogationService
from app.services.investigation_service import InvestigationService

# 여러 게임 상태 관리
class GameService:
    def __init__(self):
        self.game_managements: dict[int, GameManagement] = {}
        self.question_generations: dict[int, QuestionGeneration] = {}
        self.hint_investigations: dict[int, HintInvestigation] = {}
        self.scenario_generations: dict[int, ScenarioGeneration] = {}
        self.game_states: dict[int, dict] = {}

        self.interrogations: dict[int, Interrogation] = {}
        self.investigations: dict[int, InvestigationService] = {}

    # 새로운 게임을 시작하고 초기화하는 메서드
    def initialize_new_game(self, game_data: game_schema.GameStartRequest):
        game_management = GameManagement()
        characters = [char.npcName for char in game_data.characters]

        if "Murderer" not in [char.npcJob for char in game_data.characters]:
            raise HTTPException(status_code=400, detail="살인자가 없습니다!")
        
        murderer = next(char.npcName for char in game_data.characters if char.npcJob == "Murderer")
        
        game_state = game_management.initialize_game(game_data.language, characters, murderer)
        
        self.game_managements[game_data.gameNo] = game_management
        self.game_states[game_data.gameNo] = game_state
        self.question_generations[game_data.gameNo] = QuestionGeneration(
            game_state,
            game_management.personalities,
            game_management.features,
            game_management.weapons,
            game_management.places,
            game_management.times,
            game_management.names
        )
        self.hint_investigations[game_data.gameNo] = HintInvestigation(
            game_state,
            game_management.places,
            game_management.weapons
        )
        self.scenario_generations[game_data.gameNo] = ScenarioGeneration(
            game_state,
            game_management.personalities,
            game_management.features,
            game_management.weapons,
            game_management.places,
            game_management.times,
            game_management.names
        )
        self.investigations[game_data.gameNo] = InvestigationService(
            game_state,
            game_management.weapons,
            game_management.places,
            game_management.times,
            game_management.names
        )

        self.interrogations[game_data.gameNo] = InterrogationService(
            game_state,
            game_management.personalities,
            game_management.features,
            game_management.weapons,
            game_management.places,
            game_management.times,
            game_management.names
        )

        first_blood = self.scenario_generations[game_data.gameNo].get_first_blood()
        game_state['first_blood'] = first_blood

        return game_state

    # 게임 상태를 반환하는 메서드
    def get_game_status(self, gameNo):
        game_state = self.game_states.get(gameNo)
        if not game_state:
            raise ValueError("Game ID not found")
        game_management = self.game_managements[gameNo]
        status = game_management.get_game_status()
        status['current_day'] = game_state['current_day']
        status['alive'] = game_state['alive']
        status['murdered_npcs'] = game_state['murdered_npcs']
        return status

    # 게임 진행 상황을 저장하는 메서드
    def save_game_progress(self, gameNo, game_state):
        self.game_states[gameNo] = game_state
        return {"message": "Progress saved successfully"}

    # 초기 게임 시나리오를 생성하는 메서드
    def generate_game_scenario(self, gameNo):
        return self.scenario_generations[gameNo].create_initial_scenario()

    # 촌장의 편지를 생성하는 메서드
    def generate_chief_letter(self, gameNo):
        return self.scenario_generations[gameNo].generate_chief_letter()

    # 질문을 생성하는 메서드
    def generate_npc_questions(self, gameNo, npcName, keyWord, keyWordType):
        if gameNo not in self.question_generations:
            raise ValueError(f"Game ID {gameNo} not found in question generations.")
        return self.question_generations[gameNo].generate_questions(npcName, keyWord, keyWordType)

    # NPC와 대화를 진행하는 메서드
    def talk_to_npc(self, gameNo, npcName, keyWord, keyWordType):
        if gameNo not in self.question_generations:
            raise ValueError(f"Game ID {gameNo} not found in question generations.")
        return self.question_generations[gameNo].talk_to_npc(npcName, keyWord, keyWordType)

    # 범행 장소를 조사하는 메서드
    def investigate_location(self, gameNo, location_name):
        if gameNo not in self.hint_investigations:
            raise ValueError(f"Game ID {gameNo} not found in hint investigations.")
        return self.hint_investigations[gameNo].investigate_location(location_name)

    # 범행 도구를 조사하는 메서드
    def find_game_item(self, gameNo, item_name):
        if gameNo not in self.hint_investigations:
            raise ValueError(f"Game ID {gameNo} not found in hint investigations.")
        return self.hint_investigations[gameNo].find_item(item_name)

    # 용의자를 필터링하는 메서드
    def filter_game_suspects(self, gameNo, weapon, location):
        if gameNo not in self.hint_investigations:
            raise ValueError(f"Game ID {gameNo} not found in hint investigations.")
        return self.hint_investigations[gameNo].filter_suspects(weapon, location)

    # 다음 날로 넘어가는 메서드
    def proceed_to_next_day(self, gameNo: int, livingCharacters: List[game_schema.LivingNPCInfo]):
        if gameNo not in self.game_states:
            raise ValueError("Game ID not found")

        game_state = self.game_states[gameNo]
        scenario_generation = self.scenario_generations[gameNo]

        # LivingNPCInfo 객체를 딕셔너리로 변환
        living_characters_dict = [
            {"name": npc.name, "status": npc.status, "job": npc.job}
            for npc in livingCharacters
        ]

        # ScenarioGeneration 클래스의 메서드를 호출하여 게임 상태 업데이트 및 새로운 시나리오 생성
        murder_summary = scenario_generation.proceed_to_next_day(living_characters_dict)

        # 업데이트된 게임 상태 저장
        self.game_states[gameNo] = scenario_generation.game_state

        return murder_summary
    
    # 알리바이와 목격자 정보를 생성하는 메서드
    def generate_alibis_and_witness(self, gameNo):
        if gameNo not in self.scenario_generations:
            raise ValueError(f"Game ID {gameNo} not found in scenario generations.")
        
        alibis_and_witness = self.scenario_generations[gameNo].generate_alibis_and_witness()
        self.game_states[gameNo].update(alibis_and_witness)
        
        return alibis_and_witness
    
    def end_game(self, gameNo, game_result):
        if gameNo not in self.game_states:
            raise ValueError("Game ID not found")
        
        game_state = self.game_states[gameNo]
        scenario_generation = self.scenario_generations[gameNo]
        lang = game_state["language"]
        
        if game_result == "WIN":
            chief_letter = scenario_generation.generate_chief_win_letter()
            murderer_letter = scenario_generation.generate_murderer_win_letter()
            survivors_letters = scenario_generation.generate_survivors_letter()
            return {
                "result": "WIN",
                "chiefLetter": chief_letter,
                "murdererLetter": murderer_letter,
                "survivorsLetters": survivors_letters
            }
        elif game_result == "LOSE":
            chief_letter = scenario_generation.generate_chief_lose_letter()
            murderer_letter = scenario_generation.generate_murderer_lose_letter()
            return {
                "result": "LOSE",
                "chiefLetter": chief_letter,
                "murdererLetter": murderer_letter
            }
        else:
            raise ValueError("Invalid game result")
    

    #========================================================================================

    # 취조를 시작하는 메서드(증거 제공)
    def new_interrogation(self, gameNo, npc_name, data):
        interrogation: InterrogationService = self.interrogations.get(gameNo)
        if not interrogation:
            raise HTTPException(status_code=404, detail=f"game number not found(ID: {gameNo})")

        response = interrogation.interrogation(npc_name=npc_name, start_data=data)
        return convert_dict_keys(response)

    # 취조 시 자유 대화하는 메서드
    def generation_interrogation_response(self, gameNo, npc_name, content):
        interrogation: InterrogationService = self.interrogations.get(gameNo)
        if not interrogation:
            raise HTTPException(status_code=404, detail="Interrogation not found")

        response = interrogation.interrogation(npc_name=npc_name, content=content)
        return convert_dict_keys(response)
    
    def investigate_victim_corpse(self, gameNo: int) -> dict:
        """
        현재 날짜의 피해자 시체를 조사하여 범행 정보를 반환합니다.
        
        Args:
            gameNo (int): 게임 번호
            
        Returns:
            dict: 범행 시간, 장소, 도구 정보와 탐정의 조사 보고를 포함한 딕셔너리
        """
        if gameNo not in self.investigations:
            raise ValueError(f"Game ID {gameNo} not found")
            
        return self.investigations[gameNo].investigate_corpse()

def snake_to_camel(snake_str):
    """스네이크 케이스 문자열을 카멜 케이스로 변환합니다."""
    components = snake_str.split('_')
    return components[0] + ''.join(x.title() for x in components[1:])

def convert_dict_keys(d):
    """딕셔너리의 모든 키를 스네이크 케이스에서 카멜 케이스로 변환합니다.
    중첩된 딕셔너리와 리스트도 처리합니다."""
    if isinstance(d, list):
        return [convert_dict_keys(i) if isinstance(i, (dict, list)) else i for i in d]
    elif isinstance(d, dict):
        new_dict = {}
        for key, value in d.items():
            new_key = snake_to_camel(key)
            new_dict[new_key] = convert_dict_keys(value) if isinstance(value, (dict, list)) else value
        return new_dict
    return d