import os
from slack_sdk import WebClient
import ssl
import certifi
import dotenv

dotenv.load_dotenv()

def send_slack_message(message):
    ssl_context = ssl.create_default_context(cafile=certifi.where())
    slack_token = os.environ.get('assign_slack_token')
    client = WebClient(token=slack_token, ssl=ssl_context)
    channel = 'U069RPHRU95'
    client.chat_postMessage(channel=channel, text=message)

try:
    # 이벤트 정보를 사용하여 메시지를 작성
    pull_request_url = os.getenv('GITHUB_SERVER_URL') + '/' + os.getenv('GITHUB_REPOSITORY') + '/pull/' + os.getenv(
        'PULL_REQUEST_NUMBER')
    sender_username = os.getenv('GITHUB_ACTOR')
    message = f"Pull request에 리뷰가 제출되었습니다. 리뷰어: {sender_username}, Pull Request: {pull_request_url}"

    # Slack으로 메시지 전송
    send_slack_message(message)

except Exception as e:
    print('예외가 발생했습니다.', e)