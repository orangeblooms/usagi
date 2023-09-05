# Usagi 

Author: Orange Blooms

## Overview

Usagi is designed to respond to messages in your Slack workspace, specifically handling mentions and a custom command for displaying content, such as poems or files. It leverages the Slack API, Flask, and the slackeventsapi library.

## Features

- Responds to greetings in Slack messages.
- Supports a custom commands to interact with the bot for displaying content.
- Can display poems, the contents of files, or save poems to files.
- Handles different parameters like content ID, weekly scheduling, and file names.

## Installation and Setup

1. Clone the repository to your local machine.

2. Set up the required environment variables:
   - `SLACK_SIGNING_SECRET`: Your Slack app's signing secret.
   - `SLACK_BOT_TOKEN`: Your Slack bot's token.

3. Install the necessary Python packages using pip:

   ```bash
   pip install Flask slackeventsapi slack
   ```

4. Start the Flask server:

   ```bash
   python usagi.py
   ```

5. Make sure to configure your Slack app to point to the appropriate URL where your Flask server is running.

## Usage

### `/configure` Command

The `/configure` command allows you to configure a Slack channel for poem scheduling. You can use the following syntax:
```
/configure add|remove <poem_ID> [weekly <0-4>]
```
- `add|remove`: Use `add` to add a poem to the channel's schedule, or `remove` to remove a poem.
- `<poem_ID>`: Replace with the ID of the poem you want to schedule or remove.
- `[weekly <0-4>]`: Optional. Specify a custom day of the week (0 = Monday, 4 = Friday) for the poem's schedule.

- Examples:
  - `/configure add 12345 weekly 2`

### `/display` Command

The `/display` command is used to display poems, read poem files, and save poems to files. You can use the following syntax:

```
/display poem <ID> [weekly <0-4>] [file <file_name>]
```
- `<ID>`: Replace with the ID of the poem you want to display.
- `[weekly <0-4>]`: Optional. Specify a day of the week (0 = Monday, 4 = Friday) to schedule the poem for weekly display.
- `[file <file_name>]`: Optional. Specify a file name to save the poem content to a file.

- Examples:
  - `/display poem 12345`
  - `/display poem 67890 weekly 2`
  - `/display file my_poem.txt`

### `/list` Command

The `/list` command is used to list poems that are scheduled for weekly display in a specific Slack channel.
