from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class TwitterAccountCreate(BaseModel):
    username: str
    consumer_key: str
    consumer_secret: str
    access_token: str
    access_token_secret: str

class TwitterTweetCreate(BaseModel):
    content: str
    account_username: str
    media_paths: Optional[List[str]] = None
    schedule_time: Optional[datetime] = None

class TwitterTweetResponse(BaseModel):
    id: int
    platform_post_id: str
    platform_post_url: str
    status: str
    posted_time: datetime
    
    class Config:
        from_attributes = True
