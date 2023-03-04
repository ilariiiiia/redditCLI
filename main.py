from datetime import datetime

from PIL import Image
from numerize import numerize
from img2txt import convert
from functions import *
from config import Config
import dotenv
import os
import praw
import requests

c = Config()

dotenv.load_dotenv(r"secrets.env")

reddit = praw.Reddit(
    client_id=os.environ["client_id"],
    client_secret=os.environ["client_secret"],
    password=os.environ["pw"],
    username=os.environ["user_name"],
    user_agent=os.environ["user_agent"]
)

resize = True
size = 80



commands = {"upvote": upvote,
            "downvote": downvote,
            "clear vote": clear_vote,
            "save": save,
            "unsave": unsave,
            "help-award": help_award,
            "help-crosspost": help_crosspost,
            "help": helpme,
            "settings": settings}


def main():
    init = True
    while True:
        submissions = reddit.subreddit(c.c.get("app", "subreddit")).hot(limit=100)
        for submission in submissions:
            if submission.over_18 and not c.c.get("user", "NSFW"):
                continue
            try:
                if submission.polldata:
                    print(
                        f"""
                                        
Poll post in r/{submission.subreddit}
{submission.title}; {numerize.numerize(submission.score)} votes ({submission.upvote_ratio * 100}%)
{submission.polldata}
Created: {datetime.fromtimestamp(submission.created_utc)}
Permalink: https://reddit.com{submission.permalink}
                                        
                                        """
                    )
            except AttributeError:  # not a poll
                if submission.is_self:  # text only post
                    print(
                        f"""
                        
Text post in r/{submission.subreddit}
{submission.title}; {numerize.numerize(submission.score)} votes ({submission.upvote_ratio})

{submission.selftext}

Created: {datetime.fromtimestamp(submission.created_utc)}
Permalink: https://reddit.com{submission.permalink}
                                        
                                        """
                    )
                elif submission.url != submission.permalink or 'https://'+submission.url[22:] != submission.permalink:  # video, photo or link post

                    if submission.url.startswith("https://i.redd.it"):  # photo post
                        subphoto = convert.Convert(
                            Image.open(
                                requests.get(submission.url, stream=True).raw
                            ),
                            width=size
                        ).toText(resize)
                        print(
                            f"""
                    
Image post in r/{submission.subreddit}
{submission.title}; {numerize.numerize(submission.score)} votes ({submission.upvote_ratio})
Post link: {submission.url}

{subphoto}

Created: {datetime.fromtimestamp(submission.created_utc)}
Permalink: https://reddit.com{submission.permalink}

                                        """
                        )
                    else:
                        print(
                            f"""
    
    Video/link post in r/{submission.subreddit}
    {submission.title}; {numerize.numerize(submission.score)} votes ({submission.upvote_ratio})
    Post link: {submission.url}
    Created: {datetime.fromtimestamp(submission.created_utc)}
    Permalink: https://reddit.com{submission.permalink}
    
                                            """
                        )
            a = ""
            while a != "next":
                a = input("Command please. Type 'help' for help: ")
                if a == "next":
                    continue
                if a.startswith("award"):
                    try:
                        args = a.split(" ", maxsplit=4)
                        submission.award(gild_type=args[1], is_anonymous=args[2], message=args[3])
                    except Exception as e:
                        print(f"Error while parsing the command. Error details: \n {e}")
                elif a.startswith("var"):
                    try:
                        args = a.split(" ", maxsplit=3)
                        exec(f"{args[1]} = {args[2]}")
                    except Exception as e:
                        print(f"Error while parsing the command. Error details: \n {e}")
                elif a.startswith("crosspost"):
                    try:
                        args = a.split(" ", maxsplit=2)
                        submission.crosspost(args[1])
                    except Exception as e:
                        print(f"Error while parsing the command. Error details: \n {e}")
                else:
                    try:
                        fun = commands[a]
                        try:
                            fun(submission)
                        except Exception as e:
                            print(f"Error while parsing the command. Error details: \n {e}")
                    except KeyError:
                        if a != '':
                            print("Error: unknown command")


if __name__ == '__main__':
    main()
