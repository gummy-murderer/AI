from langchain_core.pydantic_v1 import BaseModel, Field, validator


class introSchema(BaseModel):
    greeting: str = Field(description="편지의 시작부분")
    content: str = Field(description="편지 내용")
    closing: str = Field(description="마지막 누구 올림 부분")

class generateVictimSchema(BaseModel):
    victim: str = Field(description="피해자")
    crimeScene: str = Field(description="살해 장소")
    method: str = Field(description="살해 방법은 칼 밖에 없음")
    witness: str = Field(description="목격자")
    eyewitnessInformation: str = Field(description="목격 정보")
    dailySummary: str = Field(description="dailySummary에는 누가 어디서 살해되었는 지 간단히 설명으로 지정해야 함. 'day 0 - '과 같은 식으로 시작해야 함. 해당 정보는 탐정에게 제공되는 것이 아니라 다음번 시나리오 생성을 위해 제공될 것임.")

class finalWordsSchema(BaseModel):
    finalWords: str