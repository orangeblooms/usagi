# Author: Orange Blooms
# Date: September 2023

from display_handler import *


def configure_channel_for_poem(action, channel_id=None, content_id=None, custom_weekly_schedule=None):
    """
    Configure a Slack channel for poem scheduling by adding or removing a poem from its schedule.

    Parameters:
        - action (str): The action to perform, either 'add' to add a poem to the schedule or 'remove' to remove a poem.
        - channel_id (str): The ID of the Slack channel to configure.
        - content_id (str): The ID of the poem or content to schedule or remove.
        - custom_weekly_schedule (int, optional): The custom weekly schedule (0-4) for the poem.

    Returns:
        - str: A confirmation or error message describing the result of the configuration.
    """
    # Load the poem schedule JSON
    poem_schedule = read_poem_schedule()

    if action == 'add':
        # Check if the content ID is already scheduled in any channel
        if content_id in poem_schedule:
            return f"The poem with ID {content_id} is already scheduled for one or more channels."

        # Create a new entry for the content ID and its schedule
        poem_schedule[content_id] = {channel_id: custom_weekly_schedule}

        # Save the updated poem schedule
        save_poem_schedule(poem_schedule)

        return f"The poem with ID {content_id} has been scheduled for channel."

    elif action == 'remove':
        # Check if the content ID is scheduled and remove it
        if content_id in poem_schedule:
            if channel_id in poem_schedule[content_id]:
                del poem_schedule[content_id][channel_id]
                # If the content ID no longer has any channels, remove it
                if not poem_schedule[content_id]:
                    del poem_schedule[content_id]
                # Save the updated poem schedule
                save_poem_schedule(poem_schedule)
                return f"The poem with ID {content_id} has been removed from channel."

        # If the content ID or channel wasn't found in the schedule
        return f"The poem with ID {content_id} is not scheduled for channel."

    else:
        return "Invalid action. Please use 'add' or 'remove'."

