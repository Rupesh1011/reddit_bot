import os
import time
import logging
from datetime import datetime
import schedule
import praw  
from groq import Groq
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env

REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
REDDIT_USERNAME = os.getenv("REDDIT_USERNAME")
REDDIT_PASSWORD = os.getenv("REDDIT_PASSWORD")
REDDIT_USER_AGENT = "testBot"

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

SUBREDDIT = "KeepWriting"

# Reddit API initialization
reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    username=REDDIT_USERNAME,
    password=REDDIT_PASSWORD,
    user_agent=REDDIT_USER_AGENT,  
)

# Groq API initialization
groq_client = Groq(api_key=GROQ_API_KEY)

# Set up logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def generate_content(prompt=f"Generate an engaging Reddit post relevant to the r/{SUBREDDIT} community. The content should be fun, interesting, or relatable, and sound natural and human-written without indicating it's AI-generated. Do not include a title or anything that would suggest this was AI-generated."):
    """Generate content using the Groq API."""
    try:
        chat_completion = groq_client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile",
        )
        return chat_completion.choices[0].message.content.strip()
    except Exception as e:
        logging.error(f"Error communicating with Groq API: {e}")
        return None


def post_to_reddit():
    """Post generated content to Reddit."""
    content = generate_content()
    if not content:
        logging.error("Content generation failed. Skipping post.")
        return

    # Dynamically create the title based on the content
    title = content.split('\n')[0]  # Extract the first line as a possible title
    if len(title) > 100:  # Ensure title length is reasonable
        title = title[:97] + "..."  # Trim if too long
    
    # Add '?' only if the subreddit contains "ask"
    if "ask" in SUBREDDIT.lower():
        title += "?"  # Ensure title is formatted as a question

    # Remove any "Title:" prefix or unnecessary text in the title
    title = title.replace("Title: ", "").strip()

    # For "askreddit", use only the title and no body text
    try:
        subreddit = reddit.subreddit(SUBREDDIT)
        if "ask" in SUBREDDIT.lower():
            # If it's askreddit, only post the title
            subreddit.submit(title=title)
            logging.info("Post submitted successfully (AskReddit).")
        else:
            # For other subreddits, include both title and content
            subreddit.submit(title=title, selftext=content)
            logging.info("Post submitted successfully.")
    except Exception as e:
        logging.error(f"Error posting to Reddit: {e}")



def comment_on_posts():
    """Generate and post comments on other posts in the subreddit."""
    try:
        subreddit = reddit.subreddit(SUBREDDIT)
        for submission in subreddit.hot(limit=5):  # Comment on the top 5 hot posts
            if submission.author == REDDIT_USERNAME:
                continue  # Skip posts by the bot itself
            
            # Fetch the title and the first few sentences of the post as context
            post_context = submission.title + "\n" + submission.selftext[:200]  # Limiting the selftext for brevity

            # Create a context-aware prompt based on the post content
            comment_prompt = f"Generate a thoughtful and engaging brief comment with an unexpected but realistic answer for the following post. Keep the comment relevant to the content, and make it appear as if it was written by a human. \nPost: {post_context}\nYour comment:"

            # Generate comment content
            comment_content = generate_content(prompt=comment_prompt)
            if not comment_content:
                continue
            
            try:
                submission.reply(comment_content)
                logging.info(f"Commented on post: {submission.title}")
                time.sleep(30)  # Add a longer delay to avoid rate limits
            except praw.exceptions.APIException as api_e:
                if "RATELIMIT" in str(api_e):
                    logging.warning(f"Oh snap! Rate limit encountered. We're waiting for 10 minutes before retrying...")
                    time.sleep(600)  # Wait for 10 minutes before retrying
                else:
                    logging.error(f"API Error: {api_e}")
    except Exception as e:
        logging.error(f"Error commenting on posts: {e}")


def schedule_posts():
    """Schedule daily posts and comments."""
    schedule.every().day.at("09:00").do(post_to_reddit)
    schedule.every().day.at("12:00").do(comment_on_posts)

    while True:
        schedule.run_pending()
        time.sleep(1)

# The following block runs the bot for testing
if __name__ == "__main__":
    logging.info("Starting Reddit bot for testing...")

    # Test post generation and posting
    logging.info("Testing post creation and submission...")
    post_to_reddit()

    # Test commenting on posts
    logging.info("Testing commenting on posts...")
    comment_on_posts()

# Uncomment the following block to run the bot as a scheduled task
# if __name__ == "__main__":
#     logging.info("Starting Reddit bot...")
#     schedule_posts()
