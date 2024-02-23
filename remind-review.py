from github import Github
import ssl
import certifi
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from dotenv import load_dotenv
import os

# load .env
load_dotenv()

# using an access token
g = Github(os.environ.get('Git_Token'))
repo = g.get_user().get_repo('nest-study')
print(repo.owner)
print(repo.full_name)
print(repo.get_pulls().totalCount)

for pull in repo.get_pulls(
            state="open",
            sort="updated",
    ):
    print(pull.user)
    print(pull.requested_reviewers)
    print(pull.requested_reviewers[0].login)


