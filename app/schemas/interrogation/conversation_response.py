from fastapi_camelcase import CamelModel

class ConversationResponse(CamelModel):
    response: str
    heart_rate: int