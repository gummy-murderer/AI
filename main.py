from fastapi import FastAPI
import uvicorn

from domain.chatbot import chatbot_router
from domain.npc_management import npc_management_router

description = """
#### 두근두근 놀러와요 마피아의 숲! 구미머더러! 지금 플레이하세요(찡긋)

기능 목록:

* **Say Hello** (_completely implemented_).
* **generator** (_not implemented_).
* **management** (_not implemented_).
"""

tags_metadata = [
    {
        "name": "generator",
        "description": "사용자 입력에 기반하여 답변을 생성합니다."
    },
    {
        "name": "management",
        "description": "npc 생성 등 부가기능입니다."
    },
]

app = FastAPI(
    title="AI Mafia",
    description=description,
    version="0.0.1",
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
    openapi_tags=tags_metadata
)

app.include_router(chatbot_router.router)
# app.include_router(npc_management_router.router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=9090, reload=False)
