from fastapi_camelcase import CamelModel

class SubmitEvidenceResponse(CamelModel):
    response: str
    heart_rate: int