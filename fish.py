import slack
import time
import os
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask, request, Response
from slackeventsapi import SlackEventAdapter
from redis import Redis


app = Flask(__name__)

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)
redis = Redis(host='127.0.0.1', port=6379, db=1)
adapter = SlackEventAdapter(os.environ['SIGNING_TICKET'], '/slack/events', app)

USER_DICT = {}
cache = {}
client = slack.WebClient(token=os.environ['SLACK_TOKEN'])
BOT_ID = client.api_call('auth.test')['user_id']
USER_LIST = client.api_call('users.list')['members']
for user in USER_LIST:
    if(user['deleted']==False):
        temp = {user['id']:
                    [{'name': user['name']}, {'real_name': user['profile']['real_name']}]
                }
        USER_DICT.update(temp)
    if(user['deleted']==False):
        temp = {user['id']: 0}
        cache.update(temp)
for key in USER_DICT.keys():
    redis.hset(key, USER_DICT[key][0]['name'], USER_DICT[key][1]['real_name'])

def convert(timeStamp):
    # 使用time
    timeArray = time.localtime(timeStamp)
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    return otherStyleTime

@adapter.on('message')
def message(payload):
    event = payload.get('event',{})
    channel = event.get("channel")
    user = event.get("user")
    text = event.get("text")
    if BOT_ID != user:
        print(user)
        print(text)
        redis.hset(user, convert(float(event['ts'])), text)

@app.route('/message-count', methods = ['GET','POST'])
def message_count():
    data = request.form
    user = data.get('user _id')
    channel = data.get('channel_id')
    return Response(), 200

if __name__ == "__main__":
    app.run(debug=True)