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
repo = g.get_user().get_repo(os.environ.get('Git_Repo_Name'))
print(repo.owner)
print(repo.full_name)

for pull in repo.get_pulls(
            state="open",
            sort="updated",
    ):
    print(pull.user)

# def _select_random_reviewer():





# ssl_context = ssl.create_default_context(cafile=certifi.where())
# slack_token = os.environ.get('slack_token')
# client = WebClient(token=slack_token, ssl=ssl_context)
#
# try:
#     if count > 0:
#         message = f"<!nest-study> 👋🏻 총 {count}개의 Pull Request가 리뷰를 기다리고 있습니다!\n"
#         for pull in pulls:
#             message += pull.title + ' ' + pull.url + '\n'
#         response = client.chat_postMessage(
#             channel='#pr-bot',
#             text=message
#         )
#     else:
#         message = f"<!nest-study> 👋🏻 남아있는 PR이 없습니다!\n"
#         response = client.chat_postMessage(
#             channel='#pr-bot',
#             text=message
#         )
#
# except SlackApiError as e:
#     # You will get a SlackApiError if "ok" is False
#     assert e.response["error"]
