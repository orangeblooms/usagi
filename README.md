# Usagi 

Author: Orange Blooms

## Overview

Usagi is designed to respond to messages in your Slack workspace, specifically handling mentions and a custom command for displaying content, such as poems or files. It leverages the Slack API, Flask, and the slackeventsapi library.

## Features

- Responds to greetings in Slack messages.
- Supports a custom `/display` command to interact with the bot for displaying content.
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

- Mention the bot with a greeting to receive a friendly response.

- Use the `/display` command to interact with the bot for displaying content. You can provide various parameters to specify what you want to display or save.

   - Examples:
     - `/display poem 12345`
     - `/display poem 67890 weekly 2`
     - `/display file my_poem.txt`
     - `/display file my_poem.txt weekly 3`