from github import Github
import ssl
import certifi
from slack_sdk import WebClient
from dotenv import load_dotenv
import os
import random

# load .env
load_dotenv()

reviewer_array = [{
    'githubName': 'CEethan',
    'slackUserId': 'U069RPHRU95'
}]


# 랜덤하게 리뷰어 선택
def select_random_reviewer(pull_user):
    selected_reviewer = random.choice(reviewer_array)
    while pull_user == selected_reviewer['githubName']:
        selected_reviewer = random.choice(reviewer_array)

    return selected_reviewer


# using an access token
g = Github(os.environ.get('Git_Token'))
repo = g.get_user().get_repo('nest-study')
ssl_context = ssl.create_default_context(cafile=certifi.where())
slack_token = os.environ.get('assign_slack_token')
client = WebClient(token=slack_token, ssl=ssl_context)

print(repo.owner)
print(repo.full_name)
print(repo.get_pulls().totalCount)

for pull in repo.get_pulls(
        state="open",
        sort="updated",
):
    if not pull.requested_reviewers:
        reviewer = select_random_reviewer(pull.user.login)
        github_id, slack_id = reviewer['githubName'], reviewer['slackUserId']

        # 리뷰어 할당
        pull.create_review_request([github_id])

        # Slack 알림 전송
        message = f"[{repo.full_name}]\n{pull.title}의 PR 리뷰어로 할당되었습니다! 빠른 리뷰 부탁드립니다.\n{pull.url}\n'"
        print(slack_id)
        client.chat_postMessage(
            channel=slack_id,
            text=message,
        )
