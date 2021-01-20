import slack
import os
from pathlib import Path
from dotenv import load_dotenv # loads .env 
from flask import Flask
from slackeventsapi import SlackEventAdapter
import json
import requests
import csv
from pipeline import process_file # output_file = process_data(csv_file)

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

app = Flask(__name__)
slack_event_adapter = SlackEventAdapter(os.environ['SIGNING_SECRET'],'/slack/events',app)

client = slack.WebClient(token=os.environ['SLACK_TOKEN'])
BOT_ID = client.api_call("auth.test")['user_id']

## Receive Message
@slack_event_adapter.on('message')
def message(payload):

    event = payload.get('event', {})
    channel_id = event.get('channel')
    user_id = event.get('user')
    text = event.get('text')

    client.chat_postMessage(channel=channel_id, text = text)
    #if user_id != None and BOT_ID != user_id and 'files' in event:
        # check if csv, check_csv()
        # get private url, get_download_url()
        # download file, get_file()
        # use csv library to convert to dictionary, csv_to_dict()
        # create tuples based on (name-company) pairs, pevents double mentor-mentee pairing, tupled-pairs dictionary, pairify()
        # use backtraking algorithm to make schedule, results = backtrack(tupled_pair)
        # produce dictionary of final results
        # convert to master-json, jsonify()
        # use master-json as base for exporting (csv, pdf, json, sheets), export(type=csv)


def get_file(private_url):
    auth = os.environ['SLACK_TOKEN']
    bearer = f'Bearer {auth}'
    with requests.Session() as s:
        download = s.get(private_url, headers={'Authorization': bearer})
        decoded_content = download.content.decode('utf-8')
        
        cr = csv.reader(decoded_content.split)

    decoded_content = download.content.deco


attachment = json.dumps( [ {
    "fallback": "Matched Mentors",
    "author_name": "MatchMaker",
}])

file_object = {
    "name": "matches.csv",
    "title": "matches.csv",
    "filetype": "csv",
    "username": "matchmaker-bot",
    "has_rich_preview": 'false'
}

if __name__=="__main__":
    app.run(debug=True)

