import praw
from reddit.models.SortCategories import SortCategories
from reddit.models.Submission import Submission
from dotenv import load_dotenv
import os

class Reddit:
    def __init__(self) -> None:
        load_dotenv()

        self.reddit = praw.Reddit(
            client_id=os.getenv("reddit_client_id"),
            client_secret=os.getenv("reddit_client_secret"),
            password=os.getenv("reddit_password"),
            user_agent="script by u/generateRandomUname",
            username="generateRandomUname",
        )

    def get_comments(self, subreddit: str, nr_of_comments: int = 4, sort_comments_by: SortCategories = SortCategories.top) -> Submission:
        for submission in self.reddit.subreddit(subreddit).hot(limit=20):
            if submission.link_flair_text == 'Breaking News' or submission.over_18:
                continue

            response = Submission(submission.title, submission.author)
            skip_submission = False

            submission.comment_sort = sort_comments_by.value
            submission.comments.replace_more(limit=0)
            for comment in submission.comments.list()[:nr_of_comments]:
                # Skip the submission if the comments are too short
                if len(comment.body.split(' ')) < 3:
                    skip_submission = True
                response.add_comment(comment)

            if skip_submission:
                continue
                

            return response

