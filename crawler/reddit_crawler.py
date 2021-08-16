import praw
from prawcore.exceptions import NotFound, Forbidden, OAuthException
from praw.exceptions import InvalidURL
import datetime
import pytz
import json

class RedditCrawler:
    def __init__(self, client_id, client_secret, password, user_agent, username):
        self.__reddit = praw.Reddit(client_id=client_id, client_secret=client_secret, password=password, user_agent=user_agent, username=username)
        self.__subreddit = ""
        self.__submission = ""
        self.__subreddit_valid = False
        self.__submission_valid = False
    
    @property
    def reddit(self):
        return self.__reddit

    @property
    def subreddit(self):
        return self.__subreddit

    @property
    def submission(self):
        return self.__submission

    @property
    def subreddit_valid(self):
        return self.__subreddit_valid
    
    @property
    def submission_valid(self):
        return self.__submission_valid

    @subreddit.setter
    def subreddit(self, subreddit: str):
        try:
            self.__reddit.subreddits.search_by_name(subreddit, exact=True)
            self.__subreddit = subreddit
            self.__subreddit_valid = True
        except NotFound as e:
            self.__subreddit_valid = False
            pass

    @submission.setter
    def submission(self, submission: str):
        try:
            self.__reddit.submission(url=submission).author
            self.__submission = submission
            self.__submission_valid = True
        except (NotFound, InvalidURL) as e:
            self.__submission_valid = False
            pass

    def get_info_from_submission(self):
        if self.__subreddit_valid and self.__submission_valid:
            submission = self.__reddit.submission(url=self.__submission)
            submission_dict = {}
            try:
                submission_author_name = submission.author.name
            except AttributeError:
                submission_author_name = None
            try:
                submission_author_id = submission.author.id
            except AttributeError:
                submission_author_id = submission_author_id

            submission_id = submission.id
            submission_time = datetime.datetime.fromtimestamp(submission.created, pytz.timezone("Singapore")).strftime("%Y-%m-%d %H:%M:%S")
            submission_title = submission.title
            submission_text = submission.selftext
            submission_upvote_ratio = submission.upvote_ratio
            submission_score = submission.score
            submission_permalink = submission.permalink

            submission_dict[submission_id] = {
                                            "submission_author_name": submission_author_name,
                                            "submission_author_id": submission_author_id,
                                            "submission_time": submission_time,
                                            "submission_title": submission_title,
                                            "submission_text": submission_text,
                                            "submission_upvote_ratio": submission_upvote_ratio,
                                            "submission_score": submission_score,
                                            "submission_permalink": submission_permalink
                                            }

            comments = submission.comments
            comment_dict = {}
            for comment in comments.list():
                comment_id = comment.id
                parent_id = comment.parent_id
                try:
                    comment_author_name = comment.author.name
                except AttributeError:
                    comment_author_name = None
                try:
                    comment_author_id = comment.author.id
                except AttributeError:
                    comment_author_id = None
                comment_text = comment.body
                comment_time = datetime.datetime.fromtimestamp(comment.created_utc, pytz.timezone("Singapore")).strftime("%Y-%m-%d %H:%M:%S")
                comment_score = comment.score
                comment_dict[comment_id] = {
                                            "parent_id": parent_id,
                                            "comment_author_name": comment_author_name,
                                            "comment_author_id": comment_author_id,
                                            "comment_text": comment_text,
                                            "comment_time": comment_time,
                                            "comment_score": comment_score
                                            }

            submission_data = {}
            submission_data["submission"] = submission_dict
            submission_data["comments"] = comment_dict
            return submission_data

        else:
            print("Please enter the correct subreddit and submission url")
            return None

    def get_authors_in_submission(self, submission_data: dict):
        authors = []
        submission_dict = submission_data.get("submission", None)
        for k, v in submission_dict.items():
            submission_author_name = v.get("submission_author_name", None)
            authors.append(submission_author_name)

        comment_dict = submission_data.get("comments", None)
        for k, v in comment_dict.items():
            comment_author_name = v.get("comment_author_name", None)
            authors.append(comment_author_name)

        authors = list(filter(None, authors)) # Remove None
        authors = list(set(authors)) # Remove duplicates
        return authors

    def get_info_from_authors(self, authors: list, limit: int):
        author_dict = {}
        for author in authors:

            try:
                redditor = self.__reddit.redditor(author)
                comments = redditor.comments.new(limit=limit)
                comment_dict = {}

                for comment in comments:
                    comment_id = comment.id
                    parent_id = comment.parent_id
                    comment_text = comment.body
                    comment_time = datetime.datetime.fromtimestamp(comment.created_utc, pytz.timezone("Singapore")).strftime("%Y-%m-%d %H:%M:%S")
                    comment_score = comment.score
                    comment_permalink = comment.permalink

                    comment_dict[comment_id] = {
                                                "parent_id": parent_id,
                                                "comment_text": comment_text,
                                                "comment_time": comment_time,
                                                "comment_score": comment_score,
                                                "comment_permalink": comment_permalink
                                                }

                author_dict[author] = comment_dict

            except Forbidden as e:
                print(f"Access to {author} is forbidden")

        return author_dict

if __name__ == "__main__":

    # login = {
    #         "client_id": "RWCcYftuTqygcUTC6EYGBw",
    #         "client_secret": "7y_ZVwwCPnpF_gKDV7sp7Vymq52nZQ",
    #         "password": "89Aether",
    #         "user_agent": "test-agent",
    #         "username": "Stardustorwell"
    #         }

    # with open("login/praw_login.json", "w") as json_file:
    #     json.dump(login, json_file, indent=2)

    try: 
        with open("login/praw_login.json") as json_file:
            login = json.load(json_file)

        try:
            reddit_crawler = RedditCrawler(
                                            client_id=login["client_id"],
                                            client_secret=login["client_secret"],
                                            password=login["password"],
                                            user_agent=login["user_agent"],
                                            username=login["username"]
                                            )

            # reddit_crawler.subreddit = "singapore"
            # reddit_crawler.submission = "https://www.reddit.com/r/singapore/comments/ku4nla/for_science_122_mrt_stations_6_lrt_stations/"

            reddit_crawler.subreddit = "redditdev"
            reddit_crawler.submission = "https://www.reddit.com/r/redditdev/comments/g6p9gu/how_to_get_all_comments_using_praw/"

            submission_data = reddit_crawler.get_info_from_submission()
            authors = reddit_crawler.get_authors_in_submission(submission_data)
            author_data = reddit_crawler.get_info_from_authors(authors, limit=5)

        except OAuthException as e:
            print("Invalid praw login details")

    except FileNotFoundError:
        print("Praw login details are missing")
