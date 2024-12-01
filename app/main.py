from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Social Media Marketing Automation API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import routers
from api.reddit import router as reddit_router
from api.twitter import router as twitter_router
from api.linkedin import router as linkedin_router

# Include routers
app.include_router(reddit_router, prefix="/api")
app.include_router(twitter_router, prefix="/api")
app.include_router(linkedin_router, prefix="/api")

@app.get("/")
async def root():
    return {
        "message": "Social Media Marketing Automation API",
        "version": "1.0.0",
        "available_platforms": {
            "reddit": "/api/reddit",
            "twitter": "/api/twitter",
            "linkedin": "/api/linkedin"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
