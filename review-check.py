from github import Github
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import ssl
import certifi
import os
import json
import dotenv

dotenv.load_dotenv()

author_array = {
    'eeeasycode': 'U069RPHRU95'
}

g = Github(os.environ.get('Git_Token'))
repo = g.get_user().get_repo(os.environ.get('Git_Repo_Name'))
event_payload_path = os.getenv('GITHUB_EVENT_PATH')

with open(event_payload_path, 'r') as f:
    event_payload = json.load(f)

pr_number = event_payload['pull_request']['number']
pr = repo.get_pull(pr_number)
pr_author = pr.user.login

# Slack 메시지 작성
message = f"안녕하세요, {pr_author}님! 풀 리퀘스트가 리뷰되었습니다."

# Slack으로 메시지 보내기
try:
    ssl_context = ssl.create_default_context(cafile=certifi.where())
    slack_token = os.environ.get('assign_slack_token')
    client = WebClient(token=slack_token, ssl=ssl_context)
    slack_id = author_array[pr_author]
    client.chat_postMessage(
        channel=slack_id,
        text=message,
    )
    print("Slack 메시지가 성공적으로 전송되었습니다.")
except SlackApiError as e:
    print(f"Slack 메시지 전송 중 오류 발생: {e.response['error']}")
