import praw
from typing import Dict, Optional, List
from datetime import datetime

class RedditClient:
    def __init__(self, credentials: Dict):
        self.reddit = praw.Reddit(
            client_id=credentials.get("client_id"),
            client_secret=credentials.get("client_secret"),
            user_agent=credentials.get("user_agent"),
            username=credentials.get("username"),
            password=credentials.get("password")
        )
    
    async def create_post(self, subreddit: str, title: str, content: str, flair: Optional[str] = None) -> Dict:
        try:
            subreddit = self.reddit.subreddit(subreddit)
            submission = subreddit.submit(title=title, selftext=content)
            
            if flair and submission.flair.choices():  # If flair exists
                submission.flair.select(flair)
            
            return {
                "status": "success",
                "post_id": submission.id,
                "url": submission.url
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }
    
    async def delete_post(self, post_id: str) -> Dict:
        try:
            submission = self.reddit.submission(id=post_id)
            submission.delete()
            return {"status": "success"}
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }
    
    async def get_subreddit_info(self, subreddit_name: str) -> Dict:
        try:
            subreddit = self.reddit.subreddit(subreddit_name)
            return {
                "status": "success",
                "data": {
                    "display_name": subreddit.display_name,
                    "title": subreddit.title,
                    "description": subreddit.description,
                    "subscribers": subreddit.subscribers,
                    "active_users": subreddit.active_user_count,
                    "created_utc": datetime.fromtimestamp(subreddit.created_utc),
                    "over18": subreddit.over18,
                    "public": subreddit.subreddit_type == "public"
                }
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }
    
    async def get_subreddit_rules(self, subreddit_name: str) -> Dict:
        try:
            subreddit = self.reddit.subreddit(subreddit_name)
            rules = subreddit.rules()
            return {
                "status": "success",
                "data": [
                    {
                        "title": rule.short_name,
                        "description": rule.description,
                        "created_utc": datetime.fromtimestamp(rule.created_utc)
                    } for rule in rules
                ]
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }
    
    async def get_subreddit_stats(self, subreddit_name: str, timeframe: str = "month") -> Dict:
        try:
            subreddit = self.reddit.subreddit(subreddit_name)
            top_posts = subreddit.top(time_filter=timeframe, limit=100)
            
            total_score = 0
            total_comments = 0
            post_count = 0
            
            for post in top_posts:
                total_score += post.score
                total_comments += post.num_comments
                post_count += 1
            
            return {
                "status": "success",
                "data": {
                    "timeframe": timeframe,
                    "post_count": post_count,
                    "average_score": total_score / post_count if post_count > 0 else 0,
                    "average_comments": total_comments / post_count if post_count > 0 else 0,
                    "total_score": total_score,
                    "total_comments": total_comments
                }
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }
    
    async def search_subreddits(self, query: str, limit: int = 10) -> Dict:
        try:
            subreddits = self.reddit.subreddits.search(query, limit=limit)
            return {
                "status": "success",
                "data": [
                    {
                        "display_name": subreddit.display_name,
                        "title": subreddit.title,
                        "description": subreddit.description,
                        "subscribers": subreddit.subscribers
                    } for subreddit in subreddits
                ]
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }
