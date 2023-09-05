# Author: Orange Blooms
# Date: September 2023
# Description: Displays content, either a poem, the contents of a file, or save a poem to a file

import os
import datetime
import json

# Define the path to the JSON file
schedule_file_path = 'poem_schedule.json'


# Function to read the poem schedule from the JSON file
def read_poem_schedule():
    if os.path.exists(schedule_file_path):
        with open(schedule_file_path, 'r') as file:
            return json.load(file)
    return {}


# Function to save the poem schedule to the JSON file
def save_poem_schedule(schedule):
    with open(schedule_file_path, 'w') as file:
        json.dump(schedule, file)


def display_content(command, content_id, weekly=None, file_name=None, channel_id=None):
    """
    Display content, which can be a poem, the contents of a file, or save a poem to a file.

    Parameters:
        - command (str): The type of command, either 'poem' or 'file'.
        - content_id (str): The identifier for the content (e.g., poem ID).
        - weekly (str): The weekly schedule for displaying the content (optional).
        - file_name (str, optional): The name of the file to save or read from (optional).
        - channel_id (str, optional): The ID of the channel where the command was invoked (optional).

    Returns:
        - If displaying content: The content to be displayed.
        - If saving to file: Confirmation message.
        - If invalid command: An error message.
    """

    poem_schedule = read_poem_schedule()

    if command == 'poem':
        # Define two example poems based on content_id
        example_poems = {
            '12345': "静夜思 (Thoughts in the Silent Night)\n\n床前明月光，疑是地上霜。\n举头望明月，低头思故乡。\n\nTranslation:\n\nBeneath the bed, the bright moonlight is like frost on the ground.\nI raise my head to gaze at the bright moon, and lower it to think of my hometown.",
            '67890': "The moon in the sky,\nShines so bright and high,\nA world full of dreams,\nIn its silver beams."
        }

        # Check if the provided content_id matches an example poem
        if content_id in example_poems:
            content = example_poems[content_id]
        else:
            content = "Poem not found. Please provide a valid content ID."

        # Include the Poem ID at the beginning of the content
        content_with_id = f'Poem ID: {content_id}\n\n{content}'

        # Check if it's the correct day to display the poem
        if is_weekly_day(content_id, channel_id, poem_schedule):
            # Load and return the poem for the current day
            return content_with_id

        # Check if the weekly parameter is provided and if it's a valid value (0-4)
        if weekly is not None:
            try:
                weekly_int = int(weekly)
                # Save the weekly value for this poem ID and channel ID in the schedule
                if content_id not in poem_schedule:
                    poem_schedule[content_id] = {}
                poem_schedule[content_id][channel_id] = weekly_int
                save_poem_schedule(poem_schedule)

                if weekly_int < 0 or weekly_int > 6 or weekly_int != datetime.datetime.now().weekday():
                    return "Invalid weekly value. Please use a number between 0 (Monday) and 6 (Sunday)."
            except ValueError:
                return "Invalid weekly value. Please use a number between 0 (Monday) and 6 (Sunday)."

        # Check if a file_name is provided and save the poem to a file if requested
        if file_name is not None:
            # Save the poem content with the Poem ID to the specified file
            with open(file_name, 'w', encoding='utf-8') as file:
                file.write(content_with_id)
            return f'Poem with ID {content_id} has been saved to the file {file_name}.\n\n{content_with_id}'

        # Return the poem content if no file_name is provided
        return content_with_id

    elif command == 'file':
        # Check if file_name is provided
        if file_name is None:
            return "File name is missing. Please provide a file name."

        # Check if the specified file exists and read its contents
        if os.path.exists(file_name):
            with open(file_name, 'r', encoding='utf-8') as file:
                return file.read()
        else:
            return f"File not found. The specified file '{file_name}' does not exist."

    else:
        return "Invalid command. Please use: /display poem <ID> [weekly <0-4>] [file <file_name>] or /display file <file_name>"


def is_weekly_day(content_id, channel_id, poem_schedule):
    # Get the current day of the week (0 = Monday, 6 = Sunday)
    current_day = datetime.datetime.now().weekday()

    # Check if the content_id and channel_id exist in the schedule
    if content_id in poem_schedule and channel_id in poem_schedule[content_id]:
        # Get the scheduled day for the content_id and channel_id
        scheduled_day = poem_schedule[content_id][channel_id]

        # Check if the current day matches the scheduled day
        return current_day == scheduled_day

    # If content_id or channel_id is not in the schedule, return False
    return False