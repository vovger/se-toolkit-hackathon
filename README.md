# Contact Manager Bot

Telegram bot that allows you to create custom contact fields and store any information about a person.

## Product context

**End users:** Anyone who manages many contacts — freelancers, students, managers, or regular users.

**Problem:** Contacts are scattered across different apps, and fixed fields (phone/email only) don't fit everyone's needs.

**Solution:** A Telegram bot where you create your own custom fields and find all data about a person instantly by name.

## Commands

| Command | Example | Description |
|---------|---------|-------------|
| /addfield | /addfield birthday | Create new field |
| /fields | /fields | List all fields |
| /add | /add Anna birthday 15.05 | Add data |
| /find | /find Anna | Find person |
| /findby | /findby birthday 15.05 | Search by value |
| /edit | /edit Anna birthday 20.05 | Edit data |
| /list | /list | Show all people |
| /delete | /delete Anna | Delete person |
| /export | /export | Export to JSON |


## Deployment

### Step 1: Clone repository
git clone https://github.com/vovger/se-toolkit-hackathon
cd se-toolkit-hackathon

### Step 2: Build Docker image
docker build -t contact-bot .

### Step 3: Run container
docker run -d --restart always --name contact-bot -e BOT_TOKEN="your_token" contact-bot

### Step 4: Check logs
docker logs contact-bot

## License

MIT License

## Author

Name: Vladimir Germanov
Email: v.germanov@innopolis.university
Group: DSAI-02
