from github import Github
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import ssl
import certifi
import os
import dotenv
import json

dotenv.load_dotenv()

author_array = {
    'EeeasyCode': 'U069RPHRU95'
}

g = Github(os.environ.get('Git_Token'))
repo = g.get_user().get_repo(os.environ.get('Git_Repo_Name'))
event_payload_path = os.getenv('GITHUB_EVENT_PATH')

with open(event_payload_path, 'r') as f:
    event_payload = json.load(f)

pr_number = event_payload['pull_request']['number']
pr = repo.get_pull(pr_number)
pr_author = pr.user.login
pr_title = pr.title
pr_reviewer = pr.get_reviews().get_page(0)[0].user.login
pr_url = pr.html_url

# Slack 메시지 작성
blocks = [{
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": " *[" + os.environ.get('Git_Repo_Name') + "]* \n " + pr_author + "님께서 요청하신 PR에 리뷰가 등록되었습니다."
                }
            }]
attachments = [
    {
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "• PR 제목: " + pr_title + "\n • 리뷰어: " + pr_reviewer + "\n • 리뷰 확인하기 >> <" + pr_url + "|Click>"
                }
            },
        ]
    }
]


# Slack으로 메시지 보내기
try:
    ssl_context = ssl.create_default_context(cafile=certifi.where())
    slack_token = os.environ.get('assign_slack_token')
    client = WebClient(token=slack_token, ssl=ssl_context)
    slack_id = author_array[pr_author]
    client.chat_postMessage(
        channel=slack_id,
        blocks=blocks,
        attachments=attachments
    )
except SlackApiError as e:
    assert e.response["error"]
