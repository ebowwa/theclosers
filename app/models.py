from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class RedditAccount(Base):
    __tablename__ = "reddit_accounts"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    client_id = Column(String)
    client_secret = Column(String)
    user_agent = Column(String)
    password = Column(String)  # This should be encrypted in production
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_used = Column(DateTime, nullable=True)

class Post(Base):
    __tablename__ = "posts"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    content = Column(String)
    subreddit = Column(String)
    account_id = Column(Integer)
    status = Column(String)  # pending, posted, failed
    scheduled_time = Column(DateTime, nullable=True)
    posted_time = Column(DateTime, nullable=True)
    reddit_post_id = Column(String, nullable=True)
    reddit_post_url = Column(String, nullable=True)
