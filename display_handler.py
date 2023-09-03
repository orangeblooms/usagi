# Author: Orange Blooms
# Date: September 2023
# Description: Displays content, either a poem, the contents of a file, or save a poem to a file

import os
import datetime


def display_content(command, content_id, weekly, file_name=None):
    """
    Display content, which can be a poem, the contents of a file, or save a poem to a file.

    Parameters:
        - command (str): The type of command, either 'poem' or 'file'.
        - content_id (str): The identifier for the content (e.g., poem ID).
        - weekly (str): The weekly schedule for displaying the content (optional).
        - file_name (str, optional): The name of the file to save or read from (optional).

    Returns:
        - If displaying content: The content to be displayed.
        - If saving to file: Confirmation message.
        - If invalid command: An error message.
    """
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

        # Check if the weekly parameter is provided and if it matches the current day of the week
        if weekly is not None:
            try:
                # Get the current day of the week (0 = Monday, 6 = Sunday)
                current_day = datetime.datetime.now().weekday()

                # Convert the provided weekly value to an integer
                weekly_day = int(weekly)

                # Check if the provided weekly day matches the current day
                if weekly_day != current_day:
                    return f"This {command} is scheduled for weekly day {weekly_day}. Today is not the scheduled day."
            except ValueError:
                return "Invalid weekly value. Please use a number between 0 and 6 for the day of the week."

        # Include the Poem ID at the beginning of the content
        content_with_id = f'Poem ID: {content_id}\n\n{content}'

        # Check if a file_name is provided and save the poem to a file if requested
        if file_name is not None:
            # Save the poem content with the Poem ID to the specified file
            with open(file_name, 'w', encoding='utf-8') as file:
                file.write(content_with_id)
            return f'Poem with ID {content_id} has been saved to the file {file_name}.\n\n{content_with_id}'

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
