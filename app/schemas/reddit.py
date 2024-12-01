from pydantic import BaseModel
from typing import Optional, List, Dict
from datetime import datetime

class RedditAccountCreate(BaseModel):
    username: str
    client_id: str
    client_secret: str
    user_agent: str
    password: str

class RedditAccountUpdate(BaseModel):
    client_id: Optional[str] = None
    client_secret: Optional[str] = None
    user_agent: Optional[str] = None
    password: Optional[str] = None

class RedditAccountResponse(BaseModel):
    id: int
    username: str
    platform: str
    is_active: bool
    created_at: datetime
    last_used: Optional[datetime]
    
    class Config:
        from_attributes = True

class RedditPostCreate(BaseModel):
    title: str
    content: str
    subreddit: str
    account_username: str
    flair: Optional[str] = None
    schedule_time: Optional[datetime] = None

class RedditPostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    flair: Optional[str] = None

class RedditPostResponse(BaseModel):
    id: int
    platform_post_id: str
    platform_post_url: str
    content: Dict
    status: str
    posted_time: Optional[datetime]
    scheduled_time: Optional[datetime]
    
    class Config:
        from_attributes = True

class SubredditInfo(BaseModel):
    display_name: str
    title: str
    description: str
    subscribers: int
    active_users: int
    created_utc: datetime
    over18: bool
    public: bool

class SubredditRule(BaseModel):
    title: str
    description: str
    created_utc: datetime

class SubredditStats(BaseModel):
    timeframe: str
    post_count: int
    average_score: float
    average_comments: float
    total_score: int
    total_comments: int
