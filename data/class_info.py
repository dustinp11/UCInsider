import praw
import json
from datetime import datetime
import secrets

reddit = praw.Reddit(
    client_id=secrets.client_id,
    client_secret=secrets.client_secret,
    user_agent="uc-insider-script"
)

def save_class_posts(class_name):
    subreddit = reddit.subreddit("uci")
    result = []
    for post in subreddit.search(class_name, sort="new", limit=20):
        post.comments.replace_more(limit=0)
        replies = [comment.body for comment in post.comments[:5]]

        result.append({
            "title": post.title,
            "body": post.selftext,
            "date": datetime.utcfromtimestamp(post.created_utc).strftime('%Y-%m-%d'),
            "replies": replies
        })

    filename = f"{class_name.replace(' ', '_')}_reddit_posts.json"
    with open(filename, "w") as f:
        json.dump(result, f, indent=2)
    print(f"Saved {len(result)} posts to {filename}")

if __name__ == "__main__":
    class_list = [
        "ICS 31", "ICS 32", "ICS 33", "ICS 46", "ICS 6B", "ICS 6D",
        "ICS 51", "ICS 60", "ICS 53", "CS 121", "CS 122A", "CS 171", "CS 178", "CS 161", "CS 141",
        "CS 142A", "CS 117", "CS 165", "CS 162", "ICS 45J", "ICS 139W", "MATH 3A", "CS 125", "CS 122B",
        "CS 145", "CS 175", "CS 143A", "CS 143B"
    ]  # add more
    for class_name in class_list:
        save_class_posts(class_name)