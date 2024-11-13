Here’s the updated project documentation, including the latest changes to the `Cobie Bot` code for Discord and Twitter integration.

---

# Cobie Bot - Combined Discord and Twitter Bot

This project is a combined Discord and Twitter bot inspired by Cobie's style. The bot periodically posts tweets on Twitter with a Cobie-style perspective and responds to commands on Discord, offering humorous and skeptical responses about the crypto market.

## Project Overview

The Cobie Bot project includes:
1. A script to generate Cobie-style responses for both Twitter posts and Discord messages.
2. A knowledge base created from scraped tweets using the `eliza` repository.

## Project Structure

```
cobie-bot/
├── cobie_bot.py                 # Main Python script for combined Discord + Twitter bot
├── finetune_cobie.jsonl         # JSONL file with Cobie fine-tuning data
├── cobie_character.json         # JSON file with Cobie character details
├── cobie_prompts.txt            # Text file with example Cobie prompts
├── .env.example                 # Example .env file (without sensitive info)
├── requirements.txt             # Dependencies for the project
├── README.md                    # Documentation for the project
├── .gitignore                   # File to exclude sensitive files from being uploaded
```

---

## Step 1: Setting Up the Knowledge Base

To give Cobie Bot a unique, Cobie-like tone, you’ll need to create a knowledge base of tweets. This is done using the [eliza Twitter Scraper](https://github.com/ai16z/twitter-scraper-finetune) repository, which allows you to scrape tweets and save them in JSON format.

### 1.1 Collecting JSON Files Using the `eliza` Twitter Scraper

#### Instructions

1. **Clone the `eliza` Repository**:
   ```bash
   git clone https://github.com/ai16z/twitter-scraper-finetune
   cd twitter-scraper-finetune
   ```

2. **Set Up Twitter API Credentials**:
   - Register for a Twitter Developer account if you haven’t done so.
   - Create a new Twitter app to get your API keys.
   - Create a `.env` file in the `eliza` repository and add your Twitter API credentials as follows:

     ```plaintext
     TWITTER_CONSUMER_KEY=your_consumer_key
     TWITTER_CONSUMER_SECRET=your_consumer_secret
     TWITTER_ACCESS_TOKEN=your_access_token
     TWITTER_ACCESS_TOKEN_SECRET=your_access_token_secret
     ```

3. **Run the Scraper**:
   - Customize the `eliza` script to scrape tweets from a specific account, such as Cobie’s account.
   - Run the script:
     ```bash
     python scrape_tweets.py --username cobie --output cobie_tweets.jsonl
     ```
   - This will create a JSONL file (`cobie_tweets.jsonl`) containing the tweets, which you can use as input for the Cobie Bot project.

### 1.2 Preparing the Data for Fine-Tuning

Once you have the scraped tweets:
- **Clean and process** the tweets if necessary, removing non-relevant data.
- Split the data into two files:
  - **`finetune_cobie.jsonl`**: Contains Cobie tweets for generating responses.
  - **`cobie_character.json`**: Provides character details for Cobie (personality traits, style) for contextual use.

Example content for `finetune_cobie.jsonl`:
```jsonl
{"text": "Crypto markets are like a rollercoaster, but without any of the fun."}
{"text": "Just when you think you've seen it all, someone buys the top again."}
{"text": "The only guarantee in crypto is that nothing's guaranteed."}
```

Example content for `cobie_character.json`:
```json
{
    "message examples": [
        {"prompt": "What do you think about meme coins?", "response": "They're like lotto tickets for people who hate money."}
    ],
    "post examples": [
        {"prompt": "Market is down; what's new?", "response": "Another day, another crypto panic."}
    ]
}
```

---

## Step 2: Setting Up the Cobie Bot (Discord and Twitter)

### 2.1 Environment Variables

Create a `.env` file in the project directory to store API keys and tokens for the bot. Here’s the required format:

```plaintext
API_KEY=your_twitter_api_key
API_SECRET_KEY=your_twitter_api_secret_key
ACCESS_TOKEN=your_twitter_access_token
ACCESS_TOKEN_SECRET=your_twitter_access_token_secret
OPENROUTER_API_KEY=your_openrouter_api_key
DISCORD_TOKEN=your_discord_bot_token
```

### 2.2 Installing Dependencies

Install the necessary dependencies by running:

```bash
pip install -r requirements.txt
```

The `requirements.txt` file should contain:

```plaintext
discord.py
tweepy
requests
python-dotenv
aiohttp
```

---

## Step 3: Running the Combined Bot

The `cobie_bot.py` file combines both Discord and Twitter functionalities. Here’s the content for `cobie_bot.py`:


## Step 4: Running the Bot

1. Make sure your `.env` file is correctly configured with all necessary API keys.
2. Run the bot:

   ```bash
   python cobie_bot.py
   ```

   - The bot will post tweets on Twitter at regular intervals.
   - The bot will respond to commands on Discord with a Cobie-style response.

--- 

Let me know if there’s anything more you’d like!
