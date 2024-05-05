# mulearn-task-bot

This Discord bot is built using the discord.py library and mysql. It performs various tasks on a Discord server, including sending welcome messages, tracking word usage, and allowing users to select roles via a select menu.

## Features
### Welcome Messages
When a new user joins the server, the bot sends a welcome message both to the user directly and to a designated welcome channel. Server administrators can configure the welcome channel using commands.

### Word Counting
The bot tracks the words sent by users in the server and stores the data in a database. Users can use commands to view the top 10 most frequently used words overall or by a specific user.

### Role Selection
Users can select their role using a convenient select menu provided by the bot. 

## Commands
### General Commands
 - `/help` : Displays the list of available commands and their descriptions.

### Welcome 
 - `/set_welcome_channel [channel]` : Sets the specified channel as the welcome channel, where welcome messages will be sent.
 - `/remove_welcome_channel` : Removes the welcome channel.

### Word Counting
 - `/word_status` : Shows the top 10 most frequently used words in the server.
 - `/user_status [user]`: Shows the top 10 most frequently used words by the specified user.

### Roles
 - `/select_role` -  Initiates a select menu where users can choose a role from the available options


## Installation
### 1. Installing required packages
Ensure you have Python installed on your system. Then, install the required Python packages using pip:

```
pip install -r requirements.txt
```

### 2. Environment variable
Create a copy of `.env.sample` and rename it to `.env`. Fill in the required variables such as Discord bot token and database credentials in the `.env` file.

### 3. Running the bot
Run the bot using the following command:
```
python bot.py
```