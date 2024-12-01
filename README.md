# Reddit Marketing Automation

This FastAPI server manages automated Reddit posting with support for multiple accounts and scheduled posts.

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:
```bash
cp .env.example .env
```
Edit `.env` with your Reddit API credentials and other configurations.

4. Run the server:
```bash
uvicorn app.main:app --reload
```

## Features

- Multiple Reddit account management
- Scheduled posting
- Post status tracking
- Secure credential storage
- RESTful API interface

## API Endpoints

- `POST /reddit/post`: Create a new Reddit post
- `GET /reddit/accounts`: List configured Reddit accounts

## Adding Reddit Accounts

1. Create a Reddit account
2. Create a Reddit application at https://www.reddit.com/prefs/apps
3. Add the credentials to the system using the API

## Security Notes

- Store credentials securely
- Use environment variables for sensitive data
- Implement rate limiting for production use
