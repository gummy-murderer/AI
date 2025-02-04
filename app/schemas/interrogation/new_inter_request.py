from fastapi_camelcase import CamelModel

class NewInterRequest(CamelModel):
    game_no: int
    npc_name: str = "박동식"