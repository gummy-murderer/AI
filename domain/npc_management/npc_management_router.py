from fastapi import APIRouter, HTTPException
import requests
import json

# from domain.npc_management import 
from lib.npc_management import make_ramdom_npc


router = APIRouter(
    prefix="/api/npc_management",
)


@router.get("/make_npc", tags=["conversation_with_user"])
async def conversation_between_npc(npc_number: int):
    result = make_ramdom_npc(npc_number)
    if not result:
        raise HTTPException(status_code=400, detail="make npc error")
    else:
        return {"message": "success"}