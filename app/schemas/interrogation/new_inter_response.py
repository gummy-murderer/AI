from fastapi_camelcase import CamelModel

class NewInterResponse(CamelModel):
    message: str