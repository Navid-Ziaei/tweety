"""
Quick test: scrape the latest tweet(s) from an X account using tweety.

Auth: X requires a logged-in session. Pick ONE method below by setting env vars.

  # Easiest - single auth_token cookie from your logged-in browser session:
  AUTH_TOKEN=xxxx  TARGET=elonmusk  python scrape_test.py

  # Or username + password:
  X_USER=you  X_PASS=secret  TARGET=elonmusk  python scrape_test.py

The session is cached to `session.tw_session`, so subsequent runs reuse it.
"""
import os
import asyncio
from dotenv import load_dotenv
from tweety import TwitterAsync

load_dotenv()  # reads values from a local .env file (copy from .env.example)


def build_proxy():
    host = os.environ.get("PROXY_HOST")
    if not host:
        return None
    port = os.environ.get("PROXY_PORT", "3128")
    user = os.environ.get("PROXY_USERNAME")
    password = os.environ.get("PROXY_PASSWORD")
    auth = f"{user}:{password}@" if user and password else ""
    return f"http://{auth}{host}:{port}"


async def main():
    target = os.environ.get("TARGET", "elonmusk")
    proxy = build_proxy()
    if proxy:
        print("Using proxy:", proxy)
    app = TwitterAsync("session", proxy=proxy)

    if os.environ.get("AUTH_TOKEN"):
        await app.load_auth_token(os.environ["AUTH_TOKEN"])
    elif os.environ.get("X_USER") and os.environ.get("X_PASS"):
        await app.sign_in(os.environ["X_USER"], os.environ["X_PASS"])
    else:
        # No new creds given - try to resume a previously saved session.
        await app.connect()

    print("Logged in as:", app.me)
    print(f"\nFetching tweets from @{target} ...\n")

    tweets = await app.get_tweets(target)
    for i, tweet in enumerate(tweets, 1):
        print(f"--- Tweet {i} ---")
        print("id:     ", tweet.id)
        print("date:   ", tweet.date)
        print("text:   ", tweet.text)
        print("likes:  ", tweet.likes, " retweets:", tweet.retweet_counts)
        print()
        if i >= 3:
            break


if __name__ == "__main__":
    asyncio.run(main())
