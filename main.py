from fastapi import FastAPI

from domain.chatbot import chatbot_router
from domain.npc_management import npc_management_router

description = """
두근두근 놀러와요 마피아의 숲! 구미머더러! 지금 플레이하세요(찡긋)

## Chatbot

기능 목록:

* **Say Hello** (_completely implemented_).
* **Conversation with User** (_not implemented_).
* **Conversation between Npcs** (_not implemented_).
"""

tags_metadata = [
    {
        "name": "conversation_with_user",
        "description": "npc와 user간의 대화를 위한 API입니다.",
    },
    {
        "name": "conversation_between_npcs",
        "description": "npc와 npc간의 대화를 생성해 주는 API입니다.",
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
app.include_router(npc_management_router.router)