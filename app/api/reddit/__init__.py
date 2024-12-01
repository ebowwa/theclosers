from fastapi import APIRouter
from .account_router import router as account_router
from .post_router import router as post_router
from .subreddit_router import router as subreddit_router

router = APIRouter(prefix="/reddit", tags=["reddit"])

# Include all Reddit-related routers
router.include_router(account_router)
router.include_router(post_router)
router.include_router(subreddit_router)

# Root endpoint for Reddit API
@router.get("/")
async def reddit_root():
    return {
        "message": "Reddit Marketing API",
        "endpoints": {
            "accounts": "/reddit/accounts",
            "posts": "/reddit/posts",
            "subreddits": "/reddit/subreddits"
        }
    }
