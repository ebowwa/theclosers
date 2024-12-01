from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
import os
from database.config import get_db
from database.models import SocialAccount, Post
from services.twitter.client import TwitterClient
from schemas.twitter import TwitterAccountCreate, TwitterTweetCreate, TwitterTweetResponse

router = APIRouter()

@router.get("/")
async def twitter_root():
    return {"message": "Twitter API endpoints coming soon"}

@router.post("/accounts")
async def create_account(account: TwitterAccountCreate, db: Session = Depends(get_db)):
    db_account = SocialAccount(
        platform="twitter",
        username=account.username,
        credentials={
            "consumer_key": account.consumer_key,
            "consumer_secret": account.consumer_secret,
            "access_token": account.access_token,
            "access_token_secret": account.access_token_secret
        }
    )
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    return db_account

@router.post("/tweet")
async def create_tweet(tweet: TwitterTweetCreate, db: Session = Depends(get_db)):
    account = db.query(SocialAccount).filter(
        SocialAccount.platform == "twitter",
        SocialAccount.username == tweet.account_username
    ).first()
    
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    
    client = TwitterClient(account.credentials)
    
    # Handle media uploads if any
    media_ids = []
    if tweet.media_paths:
        for media_path in tweet.media_paths:
            media_id = await client.upload_media(media_path)
            if media_id:
                media_ids.append(media_id)
    
    result = await client.create_tweet(
        content=tweet.content,
        media_ids=media_ids if media_ids else None
    )
    
    if result["status"] == "error":
        raise HTTPException(status_code=500, detail=result["error"])
    
    db_post = Post(
        account_id=account.id,
        platform="twitter",
        content={
            "content": tweet.content,
            "media_paths": tweet.media_paths
        },
        status="posted",
        posted_time=datetime.utcnow(),
        platform_post_id=result["tweet_id"],
        platform_post_url=result["url"]
    )
    
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

@router.delete("/tweet/{tweet_id}")
async def delete_tweet(tweet_id: str, account_username: str, db: Session = Depends(get_db)):
    account = db.query(SocialAccount).filter(
        SocialAccount.platform == "twitter",
        SocialAccount.username == account_username
    ).first()
    
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    
    client = TwitterClient(account.credentials)
    result = await client.delete_tweet(tweet_id)
    
    if result["status"] == "error":
        raise HTTPException(status_code=500, detail=result["error"])
    
    return {"status": "success", "message": "Tweet deleted"}

@router.get("/tweets")
async def list_tweets(db: Session = Depends(get_db)):
    return db.query(Post).filter(Post.platform == "twitter").all()
