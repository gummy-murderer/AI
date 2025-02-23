from fastapi import APIRouter
from fastapi.responses import FileResponse


router = APIRouter(
    prefix=""
)

@router.get("/interrogation")
async def login_page():
    return FileResponse("app/resources/interrogation_test.html")
