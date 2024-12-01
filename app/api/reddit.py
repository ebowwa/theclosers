from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from database.config import get_db
from database.models import SocialAccount, Post
from services.reddit.client import RedditClient
from schemas.reddit import RedditPostCreate, RedditAccountCreate

router = APIRouter()

@router.post("/accounts")
async def create_account(account: RedditAccountCreate, db: Session = Depends(get_db)):
    db_account = SocialAccount(
        platform="reddit",
        username=account.username,
        credentials={
            "client_id": account.client_id,
            "client_secret": account.client_secret,
            "user_agent": account.user_agent,
            "username": account.username,
            "password": account.password
        }
    )
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    return db_account

@router.post("/post")
async def create_post(post: RedditPostCreate, db: Session = Depends(get_db)):
    account = db.query(SocialAccount).filter(
        SocialAccount.platform == "reddit",
        SocialAccount.username == post.account_username
    ).first()
    
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    
    client = RedditClient(account.credentials)
    result = await client.create_post(
        subreddit=post.subreddit,
        title=post.title,
        content=post.content
    )
    
    if result["status"] == "error":
        raise HTTPException(status_code=500, detail=result["error"])
    
    db_post = Post(
        account_id=account.id,
        platform="reddit",
        content={
            "title": post.title,
            "content": post.content,
            "subreddit": post.subreddit
        },
        status="posted",
        posted_time=datetime.utcnow(),
        platform_post_id=result["post_id"],
        platform_post_url=result["url"]
    )
    
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

@router.get("/posts")
async def list_posts(db: Session = Depends(get_db)):
    return db.query(Post).filter(Post.platform == "reddit").all()
