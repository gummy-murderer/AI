from fastapi_camelcase import CamelModel

from .enum import EvidenceType

class SubmitEvidenceRequest(CamelModel):
    type: EvidenceType
    name: str