import os
import random
import re
import json
import aiohttp
import discord
import tweepy
from discord.ext import commands, tasks
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
API_KEY = os.getenv("API_KEY")
API_SECRET_KEY = os.getenv("API_SECRET_KEY")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")

# OpenRouter API endpoint
API_ENDPOINT = "https://openrouter.ai/api/v1/completions"

# Load Cobie's prompts from finetune_cobie.jsonl
def load_finetune_prompts():
    try:
        with open("finetune_cobie.jsonl", "r", encoding="utf-8") as jsonl_file:
            prompts = [json.loads(line)["text"] for line in jsonl_file]
        print("Loaded Cobie prompts from finetune_cobie.jsonl successfully.")
        return prompts
    except FileNotFoundError:
        print("finetune_cobie.jsonl file not found. Using fallback prompt.")
        return ["Fallback prompt text for Cobie AI."]

# Load Cobie's character traits from cobie.character.json
def load_cobie_character():
    try:
        with open("cobie.character.json", "r", encoding="utf-8") as json_file:
            character_data = json.load(json_file)
        print("Loaded Cobie character data successfully.")
        return character_data
    except FileNotFoundError:
        print("cobie.character.json file not found. Using fallback data.")
        return {"message examples": [], "post examples": []}

# Load knowledge base
cobie_prompts = load_finetune_prompts()
cobie_character = load_cobie_character()
message_examples = cobie_character.get("message examples", [])
post_examples = cobie_character.get("post examples", [])

# Create the prompt for generating responses
def create_response_prompt(user_message: str) -> str:
    # Randomly choose examples from both finetune and character data
    example_prompt = random.choice(cobie_prompts).strip()
    example_message = (
        random.choice(message_examples).get("prompt", "") + " -> " + 
        random.choice(message_examples).get("response", "")
    ) if message_examples else "Fallback message example."

    return (
        f"You are Cobie, a crypto influencer known for your sharp wit, humor, and sarcasm. "
        f"Your responses are sharp, sarcastic, and unapologetically direct.\n\n"
        f"Example tweet from finetune_cobie.jsonl:\n{example_prompt}\n\n"
        f"Example dialogue from cobie.character.json:\n{example_message}\n\n"
        f"User: {user_message}\n"
        f"Cobie's response:"
    )

# Clean up response text to remove unwanted characters
def clean_reply(reply: str) -> str:
    emoji_pattern = re.compile(
        "["u"\U0001F600-\U0001F64F"u"\U0001F300-\U0001F5FF"u"\U0001F680-\U0001F6FF"
        u"\U0001F700-\U0001F77F"u"\U0001F780-\U0001F7FF"u"\U0001F800-\U0001F8FF"u"\U0001F900-\U0001F9FF"u"\U0001FA00-\U0001FA6F"
        u"\U0001FA70-\U0001FAFF"u"\U00002702-\U000027B0"u"\U000024C2-\U0001F251]+", flags=re.UNICODE)
    return emoji_pattern.sub('', reply).replace("#", "").replace("@", "")

# Determine if the bot should respond based on mention of "Cobie" or @Cobie
async def _shouldRespond(user_message: str, message) -> bool:
    # Respond only if "Cobie" is mentioned in the message or the bot is directly mentioned
    if "Cobie" in user_message or client.user.mentioned_in(message):
        print("Cobie mentioned; responding.")
        return True
    print("No mention of Cobie; ignoring.")
    return False

# Set up the Discord client
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}!')
    print("Bot is up and running.")

@client.event
async def on_message(message):
    # Ignore messages sent by the bot itself
    if message.author == client.user:
        return

    # Clean up and print received message for debugging
    user_message = message.content.strip()
    print(f"Received message: {user_message}")
    
    # Decide if the bot should respond
    if await _shouldRespond(user_message, message):
        # Create the AI prompt
        prompt = create_response_prompt(user_message)

        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "openai/gpt-3.5-turbo",
            "prompt": prompt,
            "max_tokens": 60,
            "temperature": 1.2,
            "top_p": 0.8,
            "frequency_penalty": 0.7,
            "presence_penalty": 0.9,
        }

        try:
            # Use aiohttp to make asynchronous HTTP request
            async with aiohttp.ClientSession() as session:
                async with session.post(API_ENDPOINT, headers=headers, json=payload, timeout=10) as response:
                    if response.status == 200:
                        response_data = await response.json()
                        if 'choices' in response_data and response_data['choices']:
                            reply = response_data['choices'][0]['text'].strip()
                            reply = clean_reply(reply)
                        else:
                            print("Unexpected response format or empty choices.")
                            print("Full response data:", response_data)
                            reply = "I'm here, but I encountered an issue generating a response."
                    else:
                        print(f"Error in response API: {response.status}")
                        reply = "Unable to generate a response."

            # Send the generated response back in the channel
            await message.channel.send(reply)
        except Exception as e:
            print(f"Error generating response: {e}")
            await message.channel.send("Sorry, I'm experiencing technical issues.")
    else:
        print("Cobie Bot chose not to respond.")

# Twitter Authentication and Posting
auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
twitter_api = tweepy.API(auth)

@tasks.loop(hours=1)
async def tweet_periodically():
    tweet_content = random.choice(cobie_prompts).strip()
    try:
        twitter_api.update_status(tweet_content)
        print("Tweeted:", tweet_content)
    except tweepy.TweepyException as e:
        print("Error posting tweet:", e)

# Start the bot and tweet periodically
@client.event
async def on_ready():
    print(f'{client.user} is connected to Discord!')
    tweet_periodically.start()

client.run(DISCORD_TOKEN)
