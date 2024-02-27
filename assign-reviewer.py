from github import Github
import ssl
import certifi
from slack_sdk import WebClient
import os
import random
import dotenv
import json

dotenv.load_dotenv()

# Reviewer githubName, slackUserId로 관리됨

member_list_path = "member_list.json"
with open(member_list_path, 'r') as file:
    member_list = json.load(file)


# 랜덤하게 리뷰어 선택
def select_random_reviewer(pull_user):
    selected_reviewer = random.choice(member_list)

    # 선택된 리뷰어가 pr을 올린 유저와 같을 경우에 다시 뽑기
    while pull_user == selected_reviewer['githubName']:
        selected_reviewer = random.choice(member_list)

    return selected_reviewer


try:
    # using an access token
    g = Github(os.environ.get('Git_Token'))
    repo = g.get_user().get_repo(os.environ.get('Git_Repo_Name'))
    ssl_context = ssl.create_default_context(cafile=certifi.where())
    slack_token = os.environ.get('assign_slack_token')
    client = WebClient(token=slack_token, ssl=ssl_context)
    for pull in repo.get_pulls(
            state="open",
            sort="updated",
    ):
        print("hi")
        if not pull.requested_reviewers:
            reviewer = select_random_reviewer(pull.user.login)
            github_id, slack_id = reviewer['githubName'], reviewer['slackUserId']
            # 리뷰어 할당
            pull.create_review_request([github_id])
            repo_name = repo.full_name
            pr_title = pull.title
            pr_user = pull.user.login
            pr_url = pull.html_url

            # Slack 알림 전송
            blocks = [{
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": " *[" + os.environ.get('Git_Repo_Name') + "]* \n PR 리뷰어로 할당되었습니다! 빠른 리뷰 부탁드립니다. 🙏"
                }
            }]
            attachments = [
                {
                    "blocks": [
                        {
                            "type": "section",
                            "text": {
                                "type": "mrkdwn",
                                "text": "• PR 제목: " + pr_title + "\n • 담당자: " + pr_user + "\n • 리뷰하러 가기 >> <" + pr_url + "|Click>"
                            }
                        },
                    ]
                }
            ]
            client.chat_postMessage(
                channel=slack_id,
                blocks=blocks,
                attachments=attachments
            )

except Exception as e:
    print('예외가 발생했습니다.', e)
