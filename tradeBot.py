import praw

reddit = praw.Reddit('Trade Bot')

subreddit = reddit.subreddit("orangeandblueleauge")

trades = reddit.submission(id='6y39j2')
print(trades)
