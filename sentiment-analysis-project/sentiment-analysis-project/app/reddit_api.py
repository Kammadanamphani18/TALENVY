import praw
import configparser

def get_reddit_comments(subreddit_name, search_query, limit=100):
    config = configparser.ConfigParser()
    config.read('config.ini')
    
    reddit = praw.Reddit(
        client_id=config['REDDIT']['client_id'],
        client_secret=config['REDDIT']['client_secret'],
        user_agent=config['REDDIT']['user_agent']
    )
    
    subreddit = reddit.subreddit(subreddit_name)
    comments = []
    
    for submission in subreddit.search(search_query, limit=limit):
        submission.comments.replace_more(limit=0)
        for comment in submission.comments.list():
            comments.append({
                'author': str(comment.author),
                'text': comment.body,
                'score': comment.score
            })
    
    return comments[:limit]  # Return only specified limit