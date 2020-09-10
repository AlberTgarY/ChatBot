
import time
import re
from slackclient import SlackClient
from target import command


class Bot(object):
    def __init__(self):
        # instantiate Slack client
        self.slack_client = SlackClient('xoxb-1219252904066-1331307839251-7m0yc4ZmxrONFtxRwVzmUIjv')
        # starterbot's user ID in Slack: value is assigned after the bot starts up
        self.starterbot_id = None
        self.cmd = command.Command()
        # constants
        self.RTM_READ_DELAY = 1  # 1 second delay between reading from RTM
        self.MENTION_REGEX = "^<@(|[WU].+?)>(.*)"
        self.start()

    def parse_bot_commands(self, slack_events):
        """
            Parses a list of events coming from the Slack RTM API to find bot commands.
            If a bot command is found, this function returns a tuple of command and channel.
            If its not found, then this function returns None, None.
        """
        for event in slack_events:
            if event["type"] == "message" and not "subtype" in event:
                user_id, message = self.parse_direct_mention(event["text"])
                if user_id == self.starterbot_id:
                    print(event['user'])
                    print(message)
                    print(event["channel"])
                    return event['user'], message, event["channel"]
        return None, None, None

    def parse_direct_mention(self,message_text):
        """
            Finds a direct mention (a mention that is at the beginning) in message text
            and returns the user ID which was mentioned. If there is no direct mention, returns None
        """
        matches = re.search(self.MENTION_REGEX, message_text)
        # the first group contains the username, the second group contains the remaining message
        return (matches.group(1), matches.group(2).strip()) if matches else (None, None)

    def handle_command(self,user, command, channel):
        # Default response is help text for the user
        response = self.cmd.handle_command(user, command)

        # Sends the response back to the channel
        self.slack_client.api_call(
            "chat.postMessage",
            channel=channel,
            text=response
        )

    def start(self):
        if self.slack_client.rtm_connect():
            print("Starter Bot connected and running!")
            # Read bot's user ID by calling Web API method `auth.test`
            self.starterbot_id = self.slack_client.api_call("auth.test")["user_id"]
            while True:
                user, command, channel = self.parse_bot_commands(self.slack_client.rtm_read())
                if command:
                    self.handle_command(user, command, channel)
                time.sleep(self.RTM_READ_DELAY)
        else:
            print("Connection failed. Exception traceback printed above.")

bot = Bot()