import praw
import json
from datetime import datetime

reddit = praw.Reddit(
    client_id="IJEWj8AIguZwYQ-WjE1Zzw",
    client_secret="EUOh7mopF3kNZNqLCiEU5hdRYIGTcA",
    user_agent="uc-insider-script"
)

def save_class_posts(class_name):
    subreddit = reddit.subreddit("uci")
    result = []
    for post in subreddit.search(class_name, sort="new", limit=20):
        post.comments.replace_more(limit=0)
        replies = [comment.body for comment in post.comments[:3]]

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
    class_name = input("Enter a class name (e.g., ICS 45C): ")
    save_class_posts(class_name)

