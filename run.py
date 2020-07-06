import os
import slack
from flask import Flask, request
from slackeventsapi import SlackEventAdapter
from slackbot.bot import listen_to
from uuid import uuid4

# client_id = os.environ["SLACK_CLIENT_ID"]
# client_secret = os.environ["SLACK_CLIENT_SECRET"]
# signing_secret = os.environ["SLACK_SIGNING_SECRET"]
client_id = "1219252904066.1207036003607"
client_secret = "a558c38d630ccc71f02806904db032c1"
signing_secret = "95a2dd3aa2348a6893ebfd926e9553d6"

state = str(uuid4())
# Scopes needed for this app
oauth_scope = ", ".join(["chat:write", "channels:read", "channels:join", "channels:manage"])

# Create a dictionary to represent a database to store our token
token_database = {}
global_token = ""

app = Flask(__name__)


# Route to kick off Oauth flow
@app.route("/begin_auth", methods=["GET"])
def pre_install():
    return f'<a href="https://slack.com/oauth/v2/authorize?scope={ oauth_scope }&client_id={ client_id }&state={state}"><img alt=""Add to Slack"" height="40" width="139" src="https://platform.slack-edge.com/img/add_to_slack.png" srcset="https://platform.slack-edge.com/img/add_to_slack.png 1x, https://platform.slack-edge.com/img/add_to_slack@2x.png 2x" /></a>'


# Route for Oauth flow to redirect to after user accepts scopes
@app.route("/finish_auth", methods=["GET", "POST"])
def post_install():
    # Retrieve the auth code and state from the request params
    auth_code = request.args["code"]
    received_state = request.args["state"]

    # Token is not required to call the oauth.v2.access method
    client = slack.WebClient()

    # verify state received in params matches state we originally sent in auth request
    if received_state == state:
        # Exchange the authorization code for an access token with Slack
        response = client.oauth_v2_access(
            client_id=client_id,
            client_secret=client_secret,
            code=auth_code
        )
    else:
        return "Invalid State"

    # Save the bot token and teamID to a database
    # In our example, we are saving it to dictionary to represent a DB
    teamID = response["team"]["id"]
    token_database[teamID] = response["access_token"]
    # Also save the bot token in a global variable so we don't have to
    # do a database lookup on each WebClient call
    global global_token
    global_token = response["access_token"]

    # See if "the-welcome-channel" exists. Create it if it doesn't.
    channel_exists()

    # Don't forget to let the user know that auth has succeeded!
    return "Auth complete!"


# verifies if "the-welcome-channel" already exists
def channel_exists():
    client = slack.WebClient(token=global_token)

    # grab a list of all the channels in a workspace
    clist = client.conversations_list()
    exists = False
    for k in clist["channels"]:
        # look for the channel in the list of existing channels
        if k["name"] == "the-created-channel":

            exists = True
            break
    if exists == False:
        # create the channel since it doesn't exist
        create_channel()


# creates a channel named "the-welcome-channel"
def create_channel():
    client = slack.WebClient(token=global_token)
    resp = client.conversations_create(name="the-created-channel")


# Bind the Events API route to your existing Flask app by passing the server
# instance as the last param, or with `server=app`.
slack_events_adapter = SlackEventAdapter(signing_secret, "/slack/events", app)

def init_client(teamID):

    # look up the token in our "database"
    token = token_database[teamID]

    # In case the app doesn't have access to the oAuth Token
    if token is None:
        print("ERROR: Autenticate the App!")
        return
    client = slack.WebClient(token=token)
    return client

# Create an event listener for "member_joined_channel" events
# Sends a DM to the user who joined the channel

@slack_events_adapter.on("member_joined_channel")
def member_joined_channel(event_data):
    user = event_data["event"]["user"]
    channelid = event_data["event"]["channel"]
    teamID = event_data["team_id"]

    client = init_client(teamID)

    # Use conversations.info method to get channel name for DM msg
    info = client.conversations_info(channel=channelid)
    msg = f'Welcome! You have joined: {info["channel"]["name"]}!'
    client.chat_postMessage(channel=channelid, text=msg, icon_emoji=':heart:')

# Create an event listener for "member_left_channel" events
# Sends a DM to the user who left the channel
@slack_events_adapter.on("member_left_channel")
def member_joined_channel(event_data):
    user = event_data["event"]["user"]
    channelid = event_data["event"]["channel"]
    teamID = event_data["team_id"]

    client = init_client(teamID)

    # Use conversations.info method to get channel name for DM msg
    info = client.conversations_info(channel=channelid)
    msg = f'You have left the channel: {info["channel"]["name"]}! '
    client.chat_postMessage(channel=user, text=msg, icon_emoji=':wave:')


# Create an event listener for "app_mention" events
# Sends a DM to the user who mentioned the bot
@slack_events_adapter.on("app_mention")
def app_mention(event_data):
    text = event_data["event"]["text"]
    channelid = event_data["event"]["channel"]
    teamID = event_data["team_id"]
    if "Hello" in text:
        react_greeting(teamID,channelid)

def react_greeting(teamID,channelid):
    client = init_client(teamID)
    msg = f'Hi there!  '
    client.chat_postMessage(channel=channelid, text=msg, icon_emoji=':wave:')
# Create an event listener for "message" events
# Sends a DM to the user who sent the message.

# @slack_events_adapter.on("message")
# def member_joined_channel(event_data):
#     user = event_data["event"]["user"]
#     channelid = event_data["event"]["channel"]
#     teamID = event_data["team_id"]
#
#     client =init_client(teamID)
#
#     # Use conversations.info method to get channel name for DM msg
#     info = client.conversations_info(channel=channelid)
#     msg = f'A message has been sent to :{info["channel"]["name"]}! '
#     client.chat_postMessage(channel=user, text=msg, icon_emoji=":heart:")

