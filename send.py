import slack
import os
import time
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask, request, Response
from slackeventsapi import SlackEventAdapter
from redis import Redis
from Email import send


app = Flask(__name__)

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)
redis = Redis(host='127.0.0.1', port=6379)
adapter = SlackEventAdapter(os.environ['SIGNING_TICKET1'], '/slack/events', app)

USER_DICT = {}
cache = {}
client = slack.WebClient(token=os.environ['SLACK_TOKEN1'])
BOT_ID = client.api_call('auth.test')['user_id']
USER_LIST = client.api_call('users.list')['members']
for user in USER_LIST:
    if(user['deleted']==False and user['is_bot']==False):
        temp = {user['id']:
                    [{'name': user['name']}, {'real_name': user['profile']['real_name']}]
                }
        USER_DICT.update(temp)
    if(user['deleted']==False and user['is_bot']==False):
        temp = {user['id']: 0}
        cache.update(temp)
for key in USER_DICT.keys():
    redis.hset(key, USER_DICT[key][0]['name'], USER_DICT[key][1]['real_name'])


def convert(timeStamp):
    # 使用time
    timeArray = time.localtime(float(timeStamp))
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    return str(otherStyleTime)

@adapter.on('message')
def message(payload):
    event = payload.get('event',{})
    channel = event.get("channel")
    user = event.get("user")
    text = event.get("text")
    aka = USER_DICT.get(user)[0].get('name')
    if BOT_ID != user:
        print(text)
        with open("test.txt", "a") as f:
            f.write("-"+user+f"({aka})"+" "+convert(event['ts'])+"\n")
            f.write(text+"\n")

@app.route('/send_email', methods = ['GET','POST'])
def message_count():
    send("test.txt")
    return Response(), 200

if __name__ == "__main__":
    app.run(debug=True)