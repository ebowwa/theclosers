from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def linkedin_root():
    return {"message": "LinkedIn API endpoints coming soon"}
