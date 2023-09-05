# Author: Orange Blooms
# Date: September 2023
# Description: Lists all the poems on a weekly schedule

def list_weekly_poems(schedule_json):
    """
    List poems that are scheduled to be displayed on a weekly basis.

    Parameters:
        - schedule_json (dict): A dictionary containing the poem schedule data.

    Returns:
        - A list of poems scheduled for weekly display.
    """
    weekly_poems = [f":memo: Here is the list of all the scheduled poems in this channel. \n"]

    for content_id, channel_schedule in schedule_json.items():
        for channel_id, weekly_value in channel_schedule.items():
            if weekly_value is not None:
                weekly_poems.append(f"Poem ID: {content_id}, Weekly Schedule: {weekly_value}")

    return weekly_poems
