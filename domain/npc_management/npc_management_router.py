# from fastapi import APIRouter, HTTPException

# # from domain.npc_management import 
# from lib.npc_management import make_ramdom_npc


# router = APIRouter(
#     prefix="/api/npc_management",
# )


# @router.get("/make_npc", 
#             description="지정된 숫자에 따라 무작위로 NPC를 생성하는 API입니다.", 
#             tags=["management"])
# async def conversation_between_npc(npc_number: int):
#     result = make_ramdom_npc(npc_number)
#     if not result:
#         raise HTTPException(status_code=400, detail="make npc error")
#     else:
#         return {"message": "success"}