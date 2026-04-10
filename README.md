# Contact Manager Bot

A Telegram bot that lets you create custom contact fields and instantly find any person by name.

## Product context

End users: Anyone who manages many contacts (freelancers, students, managers, regular users).

Problem: Contacts are scattered across different apps. Fixed fields (phone/email only) don't fit everyone's needs. Friends need birthdays, colleagues need company names.

Solution: A Telegram bot where you create your own custom fields (like "birthday", "company") and find all data about a person instantly by name.

## Features

Implemented (Version 2):
- /addfield <name> - Create a new custom field
- /fields - Show all existing fields
- /add <person> <field> <value> - Add data about a person
- /find <person> - Show all fields and values for that person
- /findby <field> <value> - Find people by a specific field value
- /edit <person> <field> <new_value> - Edit existing data
- /list - Show all saved people
- /delete <person> - Delete a person and all their data
- /export - Export all contacts to a JSON file
- /aisearch <query> - AI-powered smart search using Qwen

Not yet implemented:
- Auto-suggest fields when adding a person
- Stale contact reminders
- Predefined templates for work/friend/family

## Usage

| Command | Example | Description |
|---------|---------|-------------|
| /addfield | /addfield birthday | Create new field |
| /add | /add Anna birthday 15.05 | Add data |
| /find | /find Anna | Find person |
| /findby | /findby birthday 15.05 | Search by value |
| /edit | /edit Anna birthday 20.05 | Edit data |
| /list | /list | Show all people |
| /delete | /delete Anna | Delete person |
| /export | /export | Export to JSON |
| /aisearch | /aisearch Anna from Google | AI-powered search |

## Deployment

VM OS: Ubuntu 24.04

What to install:
- Docker
- Git

Step-by-step instructions:

1. Clone the repository
   git clone https://github.com/vovger/se-toolkit-hackathon
   cd se-toolkit-hackathon

2. Create .env file with your bot token
   echo "BOT_TOKEN=your_telegram_bot_token_here" > .env

3. Build Docker image
   docker build -t contact-bot .

4. Run the container
   docker run -d --restart always --name contact-bot --env-file .env contact-bot

5. Check logs
   docker logs contact-bot

## Links

GitHub: https://github.com/vovger/se-toolkit-hackathon
Telegram bot: https://t.me/@ContactPeoplebot 
