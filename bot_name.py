import os
from slackclient import SlackClient
#Trace library
import pdb

#Static bot name
BOT_NAME = 'abdalls'

#Needed to get Env variable for API token
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))

if __name__ == "__main__":
    
    api_call = slack_client.api_call("users.list")
    if api_call.get('ok'):
        #Retrieve all users
        users = api_call.get('members')
        for user in users:
            if 'name' in user and user.get('name') == BOT_NAME:
                print("Bot ID for " + user['name'] + " is " + user.get('id'))
    else:
        print("not found" + BOT_NAME)

