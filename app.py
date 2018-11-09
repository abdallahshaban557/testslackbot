#slack needed libraries
from slackeventsapi import SlackEventAdapter
from slackclient import SlackClient
import os
#needed to get the environment variables
from dotenv import load_dotenv
from os.path import join, dirname
#Snowflake connecter
import json
import snowflake.connector
#excel library
from openpyxl import Workbook
#Function file
from functions import BOPUS_METRICS
import io

#needed to get the environment variables
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# Our app's Slack Event Adapter for receiving actions via the Events API
slack_signing_secret = os.environ.get('SLACK_SIGNING_SECRET')
slack_events_adapter = SlackEventAdapter(slack_signing_secret, "/slack/events")

# Create a SlackClient for your bot to use for Web API requests
slack_bot_token = os.environ.get('SLACK_BOT_TOKEN')
slack_client = SlackClient(slack_bot_token)


#snowflake
ctx = snowflake.connector.connect(
    user = os.environ.get('snowflake_username'),
    password=os.environ.get('snowflake_password'),
    account='petco.us-east-1'
        )
cs = ctx.cursor()
try:
    cs.execute("SELECT current_version()")
    one_row = cs.fetchone()
    print(one_row[0])
finally:
    cs.close()
#ctx.close()





# Example responder to greetings
@slack_events_adapter.on("message")
def handle_message(event_data):
    message = event_data["event"]
    # If the incoming message contains "hi", then respond with a "Hello" message
    if message.get("subtype") is None and "hi" in message.get('text'):
        channel = message["channel"]
        message = "Hello <@%s>! :tada:" % message["user"]
        slack_client.api_call("chat.postMessage", channel=channel, text=message)


# Example reaction emoji echo
@slack_events_adapter.on("reaction_added")
def reaction_added(event_data):
    event = event_data["event"]
    emoji = event["reaction"]
    channel = event["item"]["channel"]
    text = ":%s:" % emoji
    slack_client.api_call("chat.postMessage", channel=channel, text=text)



# Example reaction emoji echo
@slack_events_adapter.on("app_mention")
def app_mention(event_data):
    event = event_data["event"]
    #emoji = event["reaction"]
    channel = event["channel"]
    message=event["text"]
    command = message.split(' ')

    if command[1] == 'snowflake':
        BOPUS_METRICS()
        with open('query_results\BOPUS_Metrics.xlsx', 'rb') as f:
            slack_client.api_call(
                "files.upload",
                channels=channel,
                filename='BOPUS_Metrics.xlsx',
                title='sampletitle',
                initial_comment='sampletext',
                file=io.BytesIO(f.read())
            )
        slack_client.api_call("chat.postMessage", channel=channel, text="Just finished your snowflake file!")
        #slack_client.api_call("chat.postMessage", channel=channel, text=one_row[1][0])
    else:
        #Default message
        slack_client.api_call("chat.postMessage", channel=channel, text="Maybe try to ask bot for snowflake? ")


# Error events
@slack_events_adapter.on("error")
def error_handler(err):
    print("ERrrrROR: " + str(err))

# Once we have our event listeners configured, we can start the
# Flask server with the default `/events` endpoint on port 3000
slack_events_adapter.start(port=3000 , debug=False)