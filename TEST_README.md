# Testing the Social Media Marketing API

## Reddit API Testing

### Prerequisites
1. Make sure you have your Reddit API credentials ready
2. Update the `.env` file with your credentials:
   ```env
   REDDIT_CLIENT_ID=your_client_id_here
   REDDIT_CLIENT_SECRET=your_client_secret_here
   REDDIT_USERNAME=your_reddit_username
   REDDIT_PASSWORD=your_reddit_password
   REDDIT_USER_AGENT=CaringMindBot/1.0
   ```

### Running the Tests
1. Make the test script executable:
   ```bash
   chmod +x test_reddit.sh
   ```

2. Run the test script:
   ```bash
   ./test_reddit.sh
   ```

### Test Coverage
The script tests the following endpoints:

1. Account Management:
   - Create new Reddit account in the system
   - Retrieve account information

2. Post Management:
   - Create a test post in r/test subreddit
   - List all posts
   - Delete a post

3. Subreddit Operations:
   - Get subreddit information
   - Retrieve subreddit rules
   - Get subreddit statistics
   - Search for subreddits

### Expected Output
For each test, you should see:
- A blue header indicating the test being run
- The API response in JSON format
- Success or error messages

Successful tests will show:
- Account creation confirmation
- Post creation with URL
- Subreddit information
- List of subreddit rules
- Subreddit statistics
- Search results
- Post deletion confirmation

### Error Handling
The script checks for:
1. Missing .env file
2. Server startup issues
3. API response errors
4. Post deletion verification

### Troubleshooting
If you get errors:
1. Check that your Reddit credentials are correct in `.env`
2. Ensure you have Python 3.7+ installed
3. Make sure you have write permissions in the directory
4. Check that port 8000 is not in use
5. Verify your Reddit account has appropriate permissions
6. Check your network connection
7. Ensure the subreddit 'test' is accessible

### Additional Notes
- The script creates a virtual environment if it doesn't exist
- All dependencies are automatically installed
- The server is started and stopped automatically
- Failed requests will show detailed error messages
- The script cleans up after itself (kills server, deactivates venv)

### Advanced Usage
You can modify the script to:
- Test different subreddits
- Add custom flairs
- Test scheduled posts
- Test multiple accounts
- Add more error checking

For development purposes, you can comment out tests by adding # before the test lines you want to skip.

## Twitter API Setup
1. Go to https://developer.twitter.com/en/portal/dashboard
2. Create a new project and app
3. Generate consumer keys and access tokens
4. Add to your `.env` file:
   ```env
   TWITTER_CONSUMER_KEY=your_consumer_key_here
   TWITTER_CONSUMER_SECRET=your_consumer_secret_here
   TWITTER_ACCESS_TOKEN=your_access_token_here
   TWITTER_ACCESS_TOKEN_SECRET=your_access_token_secret_here
   ```

## What the Tests Do
1. Creates a Reddit account in the system
2. Creates a test post in r/test subreddit
3. Fetches all posts made through the API
4. Creates a Twitter account in the system
5. Creates a test tweet
6. Fetches all tweets made through the API

## Expected Output
- You should see three successful API calls
- The second API call should return a Reddit post URL
- The third API call should show a list of posts including the one just created
