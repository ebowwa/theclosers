from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database.config import get_db
from database.models import SocialAccount
from schemas.reddit import RedditAccountCreate, RedditAccountResponse, RedditAccountUpdate

router = APIRouter(prefix="/accounts", tags=["reddit-accounts"])

@router.post("/", response_model=RedditAccountResponse)
async def create_account(account: RedditAccountCreate, db: Session = Depends(get_db)):
    existing_account = db.query(SocialAccount).filter(
        SocialAccount.platform == "reddit",
        SocialAccount.username == account.username
    ).first()
    
    if existing_account:
        raise HTTPException(status_code=400, detail="Account already exists")
    
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

@router.get("/", response_model=List[RedditAccountResponse])
async def list_accounts(db: Session = Depends(get_db)):
    return db.query(SocialAccount).filter(SocialAccount.platform == "reddit").all()

@router.get("/{username}", response_model=RedditAccountResponse)
async def get_account(username: str, db: Session = Depends(get_db)):
    account = db.query(SocialAccount).filter(
        SocialAccount.platform == "reddit",
        SocialAccount.username == username
    ).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return account

@router.put("/{username}", response_model=RedditAccountResponse)
async def update_account(username: str, account_update: RedditAccountUpdate, db: Session = Depends(get_db)):
    account = db.query(SocialAccount).filter(
        SocialAccount.platform == "reddit",
        SocialAccount.username == username
    ).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    
    # Update credentials
    account.credentials.update({
        "client_id": account_update.client_id or account.credentials.get("client_id"),
        "client_secret": account_update.client_secret or account.credentials.get("client_secret"),
        "user_agent": account_update.user_agent or account.credentials.get("user_agent"),
        "password": account_update.password or account.credentials.get("password")
    })
    
    db.commit()
    db.refresh(account)
    return account

@router.delete("/{username}")
async def delete_account(username: str, db: Session = Depends(get_db)):
    account = db.query(SocialAccount).filter(
        SocialAccount.platform == "reddit",
        SocialAccount.username == username
    ).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    
    db.delete(account)
    db.commit()
    return {"status": "success", "message": "Account deleted"}
