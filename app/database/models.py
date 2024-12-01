from sqlalchemy import Column, Integer, String, DateTime, Boolean, JSON, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class SocialAccount(Base):
    __tablename__ = "social_accounts"
    
    id = Column(Integer, primary_key=True, index=True)
    platform = Column(String)  # reddit, twitter, linkedin, etc.
    username = Column(String)
    credentials = Column(JSON)  # Store platform-specific credentials
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_used = Column(DateTime, nullable=True)
    
    posts = relationship("Post", back_populates="account")

class Post(Base):
    __tablename__ = "posts"
    
    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey("social_accounts.id"))
    platform = Column(String)
    content = Column(JSON)  # Store platform-specific content structure
    status = Column(String)  # pending, posted, failed
    scheduled_time = Column(DateTime, nullable=True)
    posted_time = Column(DateTime, nullable=True)
    platform_post_id = Column(String, nullable=True)
    platform_post_url = Column(String, nullable=True)
    metadata = Column(JSON, nullable=True)  # Additional platform-specific data
    
    account = relationship("SocialAccount", back_populates="posts")
