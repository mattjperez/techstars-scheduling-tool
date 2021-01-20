import slack
import os
from pathlib import Path
from dotenv import load_dotenv # loads .env 
from flask import Flask
from slackeventsapi import SlackEventAdapter
import requests
from pipeline import process_file # output_file = process_data(csv_file)
import io

# Load Environment Variables
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

# Set Server, default port 5000
app = Flask(__name__)

# Set Env to slackapi interfaces
slack_event_adapter = SlackEventAdapter(os.environ['SIGNING_SECRET'],'/slack/events',app)
client = slack.WebClient(token=os.environ['SLACK_TOKEN'])
client.chat_postMessage(channel='#matchmaker-bot', text="Hello world!")
BOT_ID = client.api_call("auth.test")['user_id']


## Receive Message
@slack_event_adapter.on('message')
def message(payload):
    print("Message received")
    event = payload.get('event', {})
    channel_id = event.get('channel')
    user_id = event.get('user')
    text = event.get('text')
    print()

    try:
        file = event.get('files', {})
    except:
        print("No file attached!")

    if user_id != None and BOT_ID != user_id and file:
        print(f'File: {file[0]}')
        file_info = file[0]
        if file_info['filetype'] == 'csv':
            download_url = file_info['url_private']
            raw = get_file(download_url)
            processed = process_file(raw)
            print()
            print("Processed File")
            print()
            try:
                if processed:
                    post_file(str(channel_id))
                    client.chat_postMessage(channel=channel_id, text = "Here're your matches!")
                    print("File sent")
            except:
                print("Failed to send file")
                client.chat_postMessage(channel=channel_id, text = "Error sending output file")
        else:
            client.chat_postMessage(channel=channel_id, text = "Please send a CSV file")
    elif user_id != None and BOT_ID != user_id:
        client.chat_postMessage(channel=channel_id, text = "Beep-Boop")


def get_file(private_url):
    token = os.environ['SLACK_TOKEN']
    bearer = f'Bearer {token}'
    resp = requests.get(private_url, headers={'Authorization': bearer})
    try:
        data = resp.content.decode('utf8')
        return io.StringIO(data)
    except:
        print("Error downloading/StringIO'ing data")



def post_file(channels):
    try:
        with open('./matches.csv', 'rb') as f:
            token = os.environ['SLACK_TOKEN']
            resp = client.files_upload(
                token=token,
                channels=channels,
                filename='matches.csv',
                title='matches',
                file=io.BytesIO(f.read()))
        return resp
    except:
        print("Failed to post_file")
        return "Failed to post file"


if __name__=="__main__":
    app.run(debug=True)

