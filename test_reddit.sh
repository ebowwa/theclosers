#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color
BLUE='\033[0;34m'

echo -e "${BLUE}Starting Reddit API Test Script${NC}"

# Check if .env file exists
if [ ! -f .env ]; then
    echo -e "${RED}Error: .env file not found!${NC}"
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo -e "${BLUE}Creating virtual environment...${NC}"
    python3 -m venv venv
fi

# Activate virtual environment
echo -e "${BLUE}Activating virtual environment...${NC}"
source venv/bin/activate

# Install requirements
echo -e "${BLUE}Installing requirements...${NC}"
pip install -r requirements.txt

# Start the FastAPI server in the background
echo -e "${BLUE}Starting FastAPI server...${NC}"
uvicorn app.main:app --reload --port 8000 &
SERVER_PID=$!

# Wait for server to start
echo -e "${BLUE}Waiting for server to start...${NC}"
sleep 5

# Test 1: Create Reddit Account
echo -e "\n${BLUE}Test 1: Creating Reddit Account${NC}"
ACCOUNT_RESPONSE=$(curl -s -X POST http://localhost:8000/api/reddit/accounts \
  -H "Content-Type: application/json" \
  -d "{
    \"username\": \"$REDDIT_USERNAME\",
    \"client_id\": \"$REDDIT_CLIENT_ID\",
    \"client_secret\": \"$REDDIT_CLIENT_SECRET\",
    \"user_agent\": \"$REDDIT_USER_AGENT\",
    \"password\": \"$REDDIT_PASSWORD\"
  }")
echo $ACCOUNT_RESPONSE

# Test 2: Get Account Info
echo -e "\n${BLUE}Test 2: Getting Account Info${NC}"
curl -s http://localhost:8000/api/reddit/accounts/$REDDIT_USERNAME

# Test 3: Create Reddit Post
echo -e "\n${BLUE}Test 3: Creating Reddit Post${NC}"
POST_RESPONSE=$(curl -s -X POST http://localhost:8000/api/reddit/posts \
  -H "Content-Type: application/json" \
  -d "{
    \"title\": \"Test Post from Marketing API\",
    \"content\": \"This is a test post from our marketing automation API\",
    \"subreddit\": \"test\",
    \"account_username\": \"$REDDIT_USERNAME\",
    \"flair\": \"Test\"
  }")
echo $POST_RESPONSE

# Extract post ID from response for later use
POST_ID=$(echo $POST_RESPONSE | grep -o '"platform_post_id":"[^"]*' | cut -d'"' -f4)

# Test 4: Get Subreddit Info
echo -e "\n${BLUE}Test 4: Getting Subreddit Info${NC}"
curl -s http://localhost:8000/api/reddit/subreddits/test/info?account_username=$REDDIT_USERNAME

# Test 5: Get Subreddit Rules
echo -e "\n${BLUE}Test 5: Getting Subreddit Rules${NC}"
curl -s http://localhost:8000/api/reddit/subreddits/test/rules?account_username=$REDDIT_USERNAME

# Test 6: Get Subreddit Stats
echo -e "\n${BLUE}Test 6: Getting Subreddit Stats${NC}"
curl -s http://localhost:8000/api/reddit/subreddits/test/stats?account_username=$REDDIT_USERNAME

# Test 7: Search Subreddits
echo -e "\n${BLUE}Test 7: Searching Subreddits${NC}"
curl -s "http://localhost:8000/api/reddit/subreddits/search?query=python&account_username=$REDDIT_USERNAME"

# Test 8: List All Posts
echo -e "\n${BLUE}Test 8: Listing All Posts${NC}"
curl -s http://localhost:8000/api/reddit/posts

# Test 9: Delete Post (if we have a post ID)
if [ ! -z "$POST_ID" ]; then
    echo -e "\n${BLUE}Test 9: Deleting Post${NC}"
    curl -s -X DELETE http://localhost:8000/api/reddit/posts/$POST_ID?account_username=$REDDIT_USERNAME
fi

# Cleanup: Kill the server
echo -e "\n\n${BLUE}Cleaning up...${NC}"
kill $SERVER_PID

# Deactivate virtual environment
deactivate

echo -e "\n${GREEN}Tests completed!${NC}"
