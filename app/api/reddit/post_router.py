from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from database.config import get_db
from database.models import SocialAccount, Post
from services.reddit.client import RedditClient
from schemas.reddit import RedditPostCreate, RedditPostResponse, RedditPostUpdate

router = APIRouter(prefix="/posts", tags=["reddit-posts"])

@router.post("/", response_model=RedditPostResponse)
async def create_post(post: RedditPostCreate, db: Session = Depends(get_db)):
    account = db.query(SocialAccount).filter(
        SocialAccount.platform == "reddit",
        SocialAccount.username == post.account_username
    ).first()
    
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    
    client = RedditClient(account.credentials)
    
    # Handle scheduled posts
    if post.schedule_time and post.schedule_time > datetime.utcnow():
        db_post = Post(
            account_id=account.id,
            platform="reddit",
            content={
                "title": post.title,
                "content": post.content,
                "subreddit": post.subreddit,
                "flair": post.flair
            },
            status="scheduled",
            scheduled_time=post.schedule_time
        )
        db.add(db_post)
        db.commit()
        return db_post
    
    # Post immediately
    result = await client.create_post(
        subreddit=post.subreddit,
        title=post.title,
        content=post.content,
        flair=post.flair
    )
    
    if result["status"] == "error":
        raise HTTPException(status_code=500, detail=result["error"])
    
    db_post = Post(
        account_id=account.id,
        platform="reddit",
        content={
            "title": post.title,
            "content": post.content,
            "subreddit": post.subreddit,
            "flair": post.flair
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

@router.get("/", response_model=List[RedditPostResponse])
async def list_posts(
    status: Optional[str] = None,
    subreddit: Optional[str] = None,
    account_username: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Post).filter(Post.platform == "reddit")
    
    if status:
        query = query.filter(Post.status == status)
    if subreddit:
        query = query.filter(Post.content["subreddit"].astext == subreddit)
    if account_username:
        account = db.query(SocialAccount).filter(
            SocialAccount.platform == "reddit",
            SocialAccount.username == account_username
        ).first()
        if account:
            query = query.filter(Post.account_id == account.id)
    
    return query.all()

@router.delete("/{post_id}")
async def delete_post(post_id: str, account_username: str, db: Session = Depends(get_db)):
    post = db.query(Post).filter(
        Post.platform == "reddit",
        Post.platform_post_id == post_id
    ).first()
    
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    account = db.query(SocialAccount).filter(
        SocialAccount.platform == "reddit",
        SocialAccount.username == account_username
    ).first()
    
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    
    client = RedditClient(account.credentials)
    result = await client.delete_post(post_id)
    
    if result["status"] == "error":
        raise HTTPException(status_code=500, detail=result["error"])
    
    db.delete(post)
    db.commit()
    
    return {"status": "success", "message": "Post deleted"}
