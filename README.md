# Github-Slack-Bot


# PR review bot 

> 지정한 레포지토리의 PR이 남아있는지 확인 후, 평일 지정한 시간에 Slack을 통해 알림을 전송하는 Bot 입니다.
> 
## Tech Environment

- Python v3.12
- actions/checkout@v3
- actions/setup-python@v3

## Code Description

### main.py

- python 코드로 slack, github 연동
- github repository 정보를 가져와 slack 메시지 형태로 가공
- 가공된 메시지를 지정한 slack 채널로 전송

### pr-review-bot.yml
- github action을 활용하여 main.py를 실행
- schedule -> cron 표현식을 통해 지정한 시간마다 동작하도록 스케줄링
- main.py의 의존성을 위해 requirements.txt로 라이브러리 설치
- 이후, github secret을 사용해 env 값 설정
