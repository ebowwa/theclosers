import tweepy
from typing import Dict, Optional, List
from datetime import datetime

class TwitterClient:
    def __init__(self, credentials: Dict):
        auth = tweepy.OAuthHandler(
            credentials.get("consumer_key"),
            credentials.get("consumer_secret")
        )
        auth.set_access_token(
            credentials.get("access_token"),
            credentials.get("access_token_secret")
        )
        self.api = tweepy.API(auth)
        self.client = tweepy.Client(
            consumer_key=credentials.get("consumer_key"),
            consumer_secret=credentials.get("consumer_secret"),
            access_token=credentials.get("access_token"),
            access_token_secret=credentials.get("access_token_secret")
        )
    
    async def create_tweet(self, content: str, media_ids: Optional[List[str]] = None) -> Dict:
        try:
            if media_ids:
                tweet = self.client.create_tweet(
                    text=content,
                    media_ids=media_ids
                )
            else:
                tweet = self.client.create_tweet(
                    text=content
                )
            
            return {
                "status": "success",
                "tweet_id": str(tweet.data['id']),
                "url": f"https://twitter.com/user/status/{tweet.data['id']}"
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }
    
    async def delete_tweet(self, tweet_id: str) -> Dict:
        try:
            self.client.delete_tweet(id=tweet_id)
            return {"status": "success"}
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }
    
    async def upload_media(self, media_path: str) -> Optional[str]:
        try:
            media = self.api.media_upload(media_path)
            return media.media_id_string
        except Exception as e:
            return None
