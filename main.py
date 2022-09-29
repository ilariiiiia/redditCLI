from datetime import datetime

from PIL import Image
from numerize import numerize
from img2txt import convert
import dotenv
import os
import praw
import requests
import tabulate

dotenv.load_dotenv(r"secrets.env")

reddit = praw.Reddit(
    client_id=os.environ["client_id"],
    client_secret=os.environ["client_secret"],
    password=os.environ["pw"],
    username="nicolello_iiiii",
    user_agent="test by nicolello_iiiii"
)

resize = True
size = 80

def upvote(s):
    s.upvote()
    print("post upvoted!")


def downvote(s):
    s.downvote()
    print("post downvoted!")


def clear_vote(s):
    s.clear_vote()
    print("cleared vote!")


def crosspost(s):
    s.crosspost(input("Please input the subreddit to crosspost in:"))
    print("Successfully crossposted!")


def save(s):
    s.save()
    print("post saved!")


def unsave(s):
    s.unsave()
    print("post unsaved!")


def help_crosspost(s): # TODO
    print("""
    Usage:
    """)

def helpme(s):
    print("""
    Possible commands:
    next: goes to the next post
    up/downvote: up/downvotes the current post
    award: awards the current post. Type "help-award" for more info
    clear vote: clears the vote
    crosspost: crossposts the current post in another community. Type "help-crosspost" for more info
    save: saves the post
    unsave: unsaves the post
    var: changes program variables. Usage: var {variable to be changed} {new value}
    """)


def help_award(s):

    print("usage: award {gild type} {is_anonymous} {message} \n gild type: see table below \n is_anonymous: If True, "
          "the authenticated user’s username will not be revealed to the recipient \n message: the message to be sent "
          "with the award \n \n")

    with open("awards.txt", 'r') as infile:
        res = []
        i = -1
        for line in infile.readlines():
            if line == '\n':
                continue
            i += 1
            if i % 5 == 0:  # name
                res.append([line])
            else:
                res[-1].append(line)

        print(
            tabulate.tabulate(res, headers=["Name", "Icon", "Award type", "Description", "Cost"])
        )


commands = {"upvote": upvote,
            "downvote": downvote,
            "clear vote": clear_vote,
            "crosspost": crosspost,
            "save": save,
            "unsave": unsave,
            "help-award": help_award,
            "help-crosspost": help_crosspost,
            "help": helpme}


def main():
    init = True
    while True:
        submissions = reddit.subreddit("all").hot(limit=10)
        for submission in submissions:

            if init:
                init = False

            else:
                a = ""
                while a != "next":
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
                    else:
                        try:
                            fun = commands[a]
                            try:
                                fun(submission)
                            except Exception as e:
                                print(f"Error while parsing the command. Error details: \n {e}")
                        except KeyError:
                            if a != '': print("Error: unknown command")
                    a = input("Command please. Type 'help' for help: ")

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

                    continue
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
                    continue
                if submission.url != submission.permalink:  # video, photo or link post

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
                        continue

                    print(
                        f"""

Video/link post in r/{submission.subreddit}
{submission.title}; {numerize.numerize(submission.score)} votes ({submission.upvote_ratio})
Post link: {submission.url}
Created: {datetime.fromtimestamp(submission.created_utc)}
Permalink: https://reddit.com{submission.permalink}

                                        """
                    )


if __name__ == '__main__':
    main()
