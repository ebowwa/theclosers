from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from database.config import get_db
from database.models import SocialAccount
from services.reddit.client import RedditClient
from schemas.reddit import SubredditInfo, SubredditRules, SubredditStats

router = APIRouter(prefix="/subreddits", tags=["reddit-subreddits"])

@router.get("/{subreddit_name}/info", response_model=SubredditInfo)
async def get_subreddit_info(
    subreddit_name: str,
    account_username: str,
    db: Session = Depends(get_db)
):
    account = db.query(SocialAccount).filter(
        SocialAccount.platform == "reddit",
        SocialAccount.username == account_username
    ).first()
    
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    
    client = RedditClient(account.credentials)
    result = await client.get_subreddit_info(subreddit_name)
    
    if result["status"] == "error":
        raise HTTPException(status_code=500, detail=result["error"])
    
    return result["data"]

@router.get("/{subreddit_name}/rules", response_model=List[SubredditRules])
async def get_subreddit_rules(
    subreddit_name: str,
    account_username: str,
    db: Session = Depends(get_db)
):
    account = db.query(SocialAccount).filter(
        SocialAccount.platform == "reddit",
        SocialAccount.username == account_username
    ).first()
    
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    
    client = RedditClient(account.credentials)
    result = await client.get_subreddit_rules(subreddit_name)
    
    if result["status"] == "error":
        raise HTTPException(status_code=500, detail=result["error"])
    
    return result["data"]

@router.get("/{subreddit_name}/stats", response_model=SubredditStats)
async def get_subreddit_stats(
    subreddit_name: str,
    account_username: str,
    timeframe: Optional[str] = "month",
    db: Session = Depends(get_db)
):
    account = db.query(SocialAccount).filter(
        SocialAccount.platform == "reddit",
        SocialAccount.username == account_username
    ).first()
    
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    
    client = RedditClient(account.credentials)
    result = await client.get_subreddit_stats(subreddit_name, timeframe)
    
    if result["status"] == "error":
        raise HTTPException(status_code=500, detail=result["error"])
    
    return result["data"]

@router.get("/search", response_model=List[SubredditInfo])
async def search_subreddits(
    query: str,
    account_username: str,
    limit: Optional[int] = 10,
    db: Session = Depends(get_db)
):
    account = db.query(SocialAccount).filter(
        SocialAccount.platform == "reddit",
        SocialAccount.username == account_username
    ).first()
    
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    
    client = RedditClient(account.credentials)
    result = await client.search_subreddits(query, limit)
    
    if result["status"] == "error":
        raise HTTPException(status_code=500, detail=result["error"])
    
    return result["data"]
