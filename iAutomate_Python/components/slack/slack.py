from slack import WebClient
from slack.errors import SlackApiError

'''

Pre requisite:
Install Python slackclient library (requires Python 3.6 and above)
Install command: pip install slackclient

:parameter
slack_token - Access token for the Slack workspace with minimum permissions
    Permissions: channels:write, channels:read, chat:write, groups:write, mpim:write, im:write
channel_name - Name of the channel to which messages will be sent. 
    Value passed for name contained unallowed special characters or upper case characters.

'''
class SlackIntegration:

    '''
    Workspace Credentials
    Workspace URL: https://xoriant-crew.slack.com
    Workspace Name: Xoriant
    '''

    slack_token = "xoxp-1128422662707-1121481081878-1136320168965-de9e4af5019732b074cc14fcaf6956ab"
    channel_name = "ax360_results"

    '''
    This method sends a message to a slack channel.
    :parameter
    message - This argument takes the value of message which is to be sent to the slack channel
    
    :returns
    Boolean value
    True - If message was sent successfully
    False - If there was any failure
    '''
    def send_message_to_channel(self, message):
        try:
            client = WebClient(token=self.slack_token)
            response = client.conversations_list()
            channel_list = []

            for element in response["channels"]:
                channel_list.append(element["name"])

            if self.channel_name not in channel_list:
                response = client.conversations_create(name=self.channel_name)

            response = client.chat_postMessage(channel=self.channel_name, text=message)
        except SlackApiError as e:
            print(e.response["error"])
            return False

        return True


'''
slack_object = SlackIntegration()
if(slack_object.send_message_to_channel("Demo Message to slack channel ax360_results !!!")):
    print("Message sent successfully")
else:
    print("There was failure")
'''

