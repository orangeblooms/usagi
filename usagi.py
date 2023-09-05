# Author: Orange Blooms
# Date: September 2023

from flask import Flask, request, Response
from slackeventsapi import SlackEventAdapter
from threading import Thread
from slack import WebClient
import json
from display_handler import *
from list_handler import *
import os

app = Flask(__name__)

greetings = ["hi", "hello", "hello there", "hey"]
SLACK_SIGNING_SECRET = '139acd7bf8b16607c2471bf44e29079e'
# SLACK_SIGNING_SECRET = os.environ['SLACK_SIGNING_SECRET']
SLACK_BOT_TOKEN = 'xoxb-5841318108658-5865052016704-PgeNpMzKqWd3peMifXBabm0V'
# SLACK_BOT_TOKEN = os.environ['SLACK_BOT_TOKEN']

# instantiating Slack client
slack_client = WebClient(SLACK_BOT_TOKEN)


# Used for Slack URL verification
@app.route("/")
def event_hook(request):
    json_dict = json.loads(request.body.decode("utf-8"))

    if "type" in json_dict:
        if json_dict["type"] == "url_verification":
            response_dict = {"challenge": json_dict["challenge"]}
            return response_dict
    return {"status": 500}


slack_events_adapter = SlackEventAdapter(
    SLACK_SIGNING_SECRET, "/slack/events", app
)


@slack_events_adapter.on("app_mention")
def handle_message(event_data):
    def send_reply(value):
        event_data = value
        message = event_data["event"]
        if message.get("subtype") is None:
            command = message.get("text")
            channel_id = message["channel"]
            if any(item in command.lower() for item in greetings):
                message = (
                        "Hello <@%s>! :rabbit2:"
                        % message["user"]  # noqa
                )
                slack_client.chat_postMessage(channel=channel_id, text=message)

    thread = Thread(target=send_reply, kwargs={"value": event_data})
    thread.start()
    return Response(status=200)

@app.route('/display', methods=['POST'])
def process_display_command():
    # Extract the text from the command payload
    command_text = request.form['text']

    # Remove leading and trailing asterisks
    command_text = command_text.strip('*')

    # Debug print to see the cleaned command text
    print(f"Cleaned command text: {command_text}")

    # Split the text into individual parameters
    params = command_text.split()

    # Debug print to see the split parameters
    print(f"Split parameters: {params}")

    # Ensure there is at least 1 parameter (command)
    if len(params) < 1:
        error_message = 'Invalid command. Please use: /display poem <ID> [weekly <0-4>] [file <file_name>] or /display file <file_name>'
        slack_client.chat_postMessage(channel=request.form['channel_id'], text=error_message)
        return Response(status=200)

    # Extract the command
    command = params[0].lower()  # Convert to lowercase for case-insensitive comparison

    # Initialize content_id, weekly, and file_name
    content_id = None
    weekly = None
    file_name = None

    # Check the command and process parameters accordingly
    if command == 'poem':
        # Process the parameters for the poem command
        i = 1
        while i < len(params):
            if params[i] == 'weekly':
                if i + 1 < len(params) and params[i + 1].isdigit():
                    weekly = params[i + 1]
                i += 2  # Skip both "weekly" and its value
            elif params[i] == 'file':
                if i + 1 < len(params):
                    file_name = params[i + 1]
                i += 2  # Skip both "file" and its value
            else:
                # Assume it's the content_id
                content_id = params[i]
                i += 1
    elif command == 'file':
        # Process the parameters for the file command
        if len(params) >= 2:
            file_name = params[1]
    else:
        # Invalid command
        error_message = 'Invalid command. Please use: /display poem <ID> [weekly <0-4>] [file <file_name>] or /display file <file_name>'
        slack_client.chat_postMessage(channel=request.form['channel_id'], text=error_message)
        return Response(status=200)

    # Debug prints for extracted parameters
    print(f"Command: {command}, Content ID: {content_id}, Weekly: {weekly}, File Name: {file_name}")

    # Call the display_content function to generate the message
    message = display_content(command, content_id, weekly, file_name, request.form['channel_id'])
    print(message)

    # Send the response message to the specified channel
    slack_client.chat_postMessage(channel=request.form['channel_id'], text=message)

    return Response(status=200)


@app.route('/list', methods=['POST'])
def list_weekly_poems_route():
    # Read the existing poem schedule
    poem_schedule = read_poem_schedule()  # Assuming you have a function to read the poem schedule JSON

    # Call the list_weekly_poems function to get a list of weekly poems
    weekly_poems = list_weekly_poems(poem_schedule)

    if weekly_poems:
        # Create a message with the list of weekly poems
        message = "\n".join(weekly_poems)
    else:
        message = "No poems on a weekly schedule found."

    # Send the response message to the specified channel
    slack_client.chat_postMessage(channel=request.form['channel_id'], text=message)

    return Response(status=200)


# Start the server on port 3000
if __name__ == "__main__":
    app.run(port=3000)
