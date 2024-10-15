from fastapi_camelcase import CamelModel

class ConversationRequest(CamelModel):
    game_no: int
    npc_name: str = "박동식"
    content: str