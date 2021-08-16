import mysql.connector
from mysql.connector import errorcode
import os
import sys
import json
from prawcore.exceptions import NotFound, Forbidden, OAuthException
from praw.exceptions import InvalidURL

sys.path.append(os.path.join(os.getcwd(), "crawler"))
from reddit_crawler import RedditCrawler

class Database:
    def __init__(self, user, password, host, port, database):
        try:
            self.cnx = mysql.connector.connect(user=user, 
                                                password=password,
                                                host=host,
                                                port=port,
                                                database=database)

            self.__state = ""
            print("Database connected!")

        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
        else:
            self.cursor = self.cnx.cursor()

    @property
    def state(self):
        return self.__state

    @state.setter
    def state(self, state: str):
        self.__state = state

    def close_connection(self):
        self.cursor.close()
        self.cnx.close()
        print("Database connection closed.")

    def get_tables(self):
        query = "Show tables;"
        self.cursor.execute(query)
        results = self.cursor.fetchall()
        for result in results:
            print(result)

    def clear_all_tables(self):
        query = "DELETE FROM author;"
        self.cursor.execute(query)
        query = "DELETE FROM comment;"
        self.cursor.execute(query)
        query = "DELETE FROM submission;"
        self.cursor.execute(query)
        self.cnx.commit()
        return

    def insert_data(self, subreddit, submission):
        
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
                print("Crawler initialized")
                reddit_crawler.subreddit = subreddit
                reddit_crawler.submission = submission
                submission_data = reddit_crawler.get_info_from_submission()
                print("Completed scanning for submission and comment data")

                if submission_data:

                    authors = reddit_crawler.get_authors_in_submission(submission_data)
                    author_data = reddit_crawler.get_info_from_authors(authors, limit=5)
                    print("Completed scanning for author data")

                    submission_dict = submission_data.get("submission", None)
                    for k, v in submission_dict.items():
                        submission_id = k
                        submission_author_name = v.get("submission_author_name", None)
                        submission_author_id = v.get("submission_author_id", None)
                        submission_time = v.get("submission_time", None)
                        submission_title = v.get("submission_title", None)
                        submission_text = v.get("submission_text", None)
                        submission_upvote_ratio = v.get("submission_upvote_ratio", None)
                        submission_score = v.get("submission_score", None)
                        submission_permalink = v.get("submission_permalink", None)

                    submission_input = {
                                        "submission_id": submission_id,
                                        "submission_author_name": submission_author_name,
                                        "submission_author_id": submission_author_id,
                                        "submission_time": submission_time,
                                        "submission_title": submission_title,
                                        "submission_text": submission_text,
                                        "submission_upvote_ratio": submission_upvote_ratio,
                                        "submission_score": submission_score,
                                        "submission_permalink": submission_permalink 
                    }
                    
                    add_submission = (
                                        """
                                        INSERT INTO submission
                                        (id, author_name, author_id, time, title, text, upvote_ratio, score, permalink)
                                        VALUES (%(submission_id)s, %(submission_author_name)s, %(submission_author_id)s, %(submission_time)s, 
                                                %(submission_title)s, %(submission_text)s, %(submission_upvote_ratio)s, %(submission_score)s, %(submission_permalink)s)
                                        ON DUPLICATE KEY UPDATE
                                            text = %(submission_text)s,
                                            upvote_ratio = %(submission_upvote_ratio)s,
                                            score = %(submission_score)s;
                                        """
                                    )

                    self.cursor.execute(add_submission, submission_input)
                    self.cnx.commit()

                    comment_dict = submission_data.get("comments", None)
                    for k, v in comment_dict.items():
                        comment_id = k
                        parent_id = v.get("parent_id", None)
                        comment_author_name = v.get("comment_author_name", None)
                        comment_author_id = v.get("comment_author_id", None)
                        comment_text = v.get("comment_text", None)
                        comment_time = v.get("comment_time", None)
                        comment_score = v.get("comment_score", None)
                        submission_id = submission_id

                        comment_input = {
                            "comment_id": comment_id,
                            "parent_id": parent_id,
                            "comment_author_name": comment_author_name,
                            "comment_author_id": comment_author_id,
                            "comment_text": comment_text,
                            "comment_time": comment_time,
                            "comment_score": comment_score,
                            "submission_id": submission_id
                        }

                        add_comment = (
                                        """
                                        INSERT INTO comment
                                        (id, parent_id, author_name, author_id, text, time, score, submission_id)
                                        VALUES (%(comment_id)s, %(parent_id)s, %(comment_author_name)s, %(comment_author_id)s, 
                                                %(comment_text)s, %(comment_time)s, %(comment_score)s, %(submission_id)s)
                                        ON DUPLICATE KEY UPDATE
                                            text = %(comment_text)s,
                                            score = %(comment_score)s;
                                        """
                                    )

                        self.cursor.execute(add_comment, comment_input)
                        self.cnx.commit()

                    for author_k, author_v in author_data.items():
                        name = author_k

                        for k, v in author_v.items():
                            comment_id = k
                            parent_id = v.get("parent_id", None)
                            comment_text = v.get("comment_text", None)
                            comment_time = v.get("comment_time", None)
                            comment_score = v.get("comment_score", None)
                            comment_permalink = v.get("comment_permalink", None)

                            author_input = {
                                "name": name,
                                "comment_id": comment_id,
                                "parent_id": parent_id,
                                "comment_text": comment_text,
                                "comment_time": comment_time,
                                "comment_score": comment_score,
                                "comment_permalink": comment_permalink
                            }

                            add_author = (
                                            """
                                            INSERT INTO author
                                            (name, comment_id, parent_id, comment_text, comment_time, comment_score, comment_permalink)
                                            VALUES (%(name)s, %(comment_id)s, %(parent_id)s, %(comment_text)s, 
                                                    %(comment_time)s, %(comment_score)s, %(comment_permalink)s)
                                            ON DUPLICATE KEY UPDATE
                                                comment_text = %(comment_text)s,
                                                comment_score = %(comment_score)s;
                                            """
                                        )

                            self.cursor.execute(add_author, author_input)
                            self.cnx.commit()

                    self.__state = "Data adding successful"

                else:
                    self.__state = "Data adding failed"

            except OAuthException as e:
                print("Invalid praw login details")

        except FileNotFoundError:
            print("Praw login details are missing")

        return

def add_data(subreddit, submission):
    try:
        with open("login/database_login.json") as json_file:
            login = json.load(json_file)

        db = Database(user=login["user"], password=login["password"], host=login["host"], port=login["port"], database=login["database"])
        db.insert_data(subreddit, submission)
        db.close_connection()
        return db.state

    except FileNotFoundError:
        print("Database login details are missing")

def delete_data():
    try:
        with open("login/database_login.json") as json_file:
            login = json.load(json_file)

        db = Database(user=login["user"], password=login["password"], host=login["host"], port=login["port"], database=login["database"])
        db.clear_all_tables()
        db.close_connection()
        return db.state

    except FileNotFoundError:
        print("Database login details are missing")


if __name__ == "__main__":
    # subreddit = "Singapore"
    # submission = "https://www.reddit.com/r/singapore/comments/ku4nla/for_science_122_mrt_stations_6_lrt_stations/"

    subreddit = "redditdev"
    submission = "https://www.reddit.com/r/redditdev/comments/g6p9gu/how_to_get_all_comments_using_praw/"
    add_data(subreddit, submission)
