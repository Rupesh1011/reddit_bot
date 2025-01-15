# Reddit Bot: Easy Setup Guide (INCLUDES BONUS FEATURE)

This guide will walk you through setting up and running a Reddit bot that generates posts and comments using the Groq API and the Reddit API.

---

## Prerequisites

1. **Python Installed**: Ensure you have Python 3.8 or higher installed. Download it from [python.org](https://www.python.org/downloads/).
2. **Pip Installed**: Pip is usually included with Python. Verify by running:

   ```bash
   pip --version
   ```

3. **Reddit Developer Account**:
   - Go to [Reddit Apps](https://www.reddit.com/prefs/apps/).
   - Create a new application and note the `client_id`, `client_secret`, and `user_agent`.

4. **Groq API Key**:
   - Sign up at [Groq](https://groq.com/) and generate an API key.

---

## Setup Instructions

### 1. Clone the Repository

Clone the GitHub repository containing the bot code:

```bash
git clone https://github.com/Rupesh1011/reddit_bot.git
cd reddit_bot.git
```

### 2. Install Dependencies

Install required libraries using pip:

```bash
pip install -r requirements.txt
```

### 3. Create a `.env` File

In the root directory of the project, create a `.env` file to store your API keys and credentials. Add the following lines:

```
REDDIT_CLIENT_ID=<your-reddit-client-id>
REDDIT_CLIENT_SECRET=<your-reddit-client-secret>
REDDIT_USERNAME=<your-reddit-username>
REDDIT_PASSWORD=<your-reddit-password>
GROQ_API_KEY=<your-groq-api-key>
```

### 4. Verify the Libraries

Ensure the following libraries are installed:

- praw
- python-dotenv
- schedule
- groq

To install any missing libraries, use:

```bash
pip install <library-name>
```

---

## Running the Bot (NOTE: DONT FORGET TO REPLACE VALUE OF SUBREDDIT VARIABLE IN THE CODE WITH THE SUBREDDIT NAME)

1. **Replace the variable SUBREDDIT variable with your subreddit name**

2. **Test Post Creation and Commenting**:
   
   Run the bot to test post creation and commenting:

   ```bash
   python redditBot.py
   ```

   - The bot will:
     - Generate a post for the specified subreddit.
     - Comment on the top 5 hot posts in the subreddit (BONUS FEATURE).

3. **Optional: Schedule Daily Posts and Comments (uncomment the schedule main function and comment out the testing main function from the code)**:

   To run the bot continuously and schedule daily tasks uncomment the schedule main funtion and comment out the testing main function:

   ```bash
   python redditBot.py
   ```

---

## Deliverables

### 1. Working Code

The bot is available in the GitHub repository. Clone the repository to access the code.

### 2. Basic README

This document provides detailed setup instructions to help you run the bot easily.

### 3. Sample Output

#### Generated Instructions
![image](https://github.com/user-attachments/assets/99bc45e7-7192-404d-9bff-c1b069233b5b)

#### Generated Post
![image](https://github.com/user-attachments/assets/6c5bf613-2dcd-40e5-83d7-0fed4def9c8f)
![image](https://github.com/user-attachments/assets/02c24614-b72e-4ace-8a73-9e0d847f8be8)




#### Generated Comments
![image](https://github.com/user-attachments/assets/efce8a4c-4f11-4e26-ad13-4e6519c6499a)
![image](https://github.com/user-attachments/assets/5dad0d0c-fe78-4556-98a7-3113f7d56ba4)



---

## Technical Requirements Fulfilled

### Reddit API Authentication
- Successfully authenticated using Reddit API with `praw`, enabling seamless interaction with Reddit for posting content and generating comments.
- Credentials are securely managed via environment variables.

### Groq API Integration
- Integrated Groq API for generating high-quality, human-like content and comments.
- API requests are dynamically handled for content generation using the `groq` library.

### Basic Scheduling Functionality
- Implemented task scheduling with the `schedule` library to automate post submissions and comment generation at predefined intervals, ensuring consistent bot activity.



---

## Notes

- For `askreddit` or similar subreddits, posts will only include the title.
- The bot automatically handles rate limits when posting comments.

Enjoy automating your Reddit posts and comments!
