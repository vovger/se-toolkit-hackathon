# Project Plan: Contact Manager Bot

## Project Idea

End-user: Anyone who manages many contacts (freelancers, students, managers, regular users)

Problem: Contacts are scattered across different apps. Fixed fields (phone/email only) don't fit everyone's needs.

One-sentence solution: A Telegram bot where you create your own custom contact fields and find all data about a person instantly by name.

Core feature: User-defined custom fields with add/find/delete functionality.

## Components

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Backend | Python + python-telegram-bot | Handles commands, business logic, database operations |
| Database | SQLite | Stores people, custom fields, and contact values |
| Client (frontend) | Telegram bot | End-user interface for sending commands and receiving data |

## Version 1 (Core Features)

Goal: Working product with basic CRUD operations.

Commands:
1. /addfield <name> - Create a new custom field type
2. /add <person> <field> <value> - Store data for a person
3. /find <person> - Show all fields and values for that person
4. /list - Show all saved people
5. /fields - Show all created custom fields
6. /delete <person> - Remove a contact

## Version 2 (Advanced Features)

Builds on V1 - adds more functionality.

Commands:
7. /findby <field> <value> - Search for people by field value
8. /edit <person> <field> <new_value> - Update existing data
9. /export - Export all contacts to JSON file
10. /aisearch <query> - AI-powered smart search using Qwen
11. Docker containerization
12. Deployment on Ubuntu 24.04 VM

## Technical Stack

| Component | Technology |
|-----------|-----------|
| Language | Python 3.10 |
| Bot Framework | python-telegram-bot v20 |
| Database | SQLite |
| Container | Docker |
| Deployment | Ubuntu 24.04 VM |

## Timeline

| Day | Task | Version |
|-----|------|---------|
| 1 | Bot setup + database + /addfield + /fields | V1 |
| 2 | /add + /find + /list + /delete | V1 |
| 3 | /edit + /findby + /export | V2 |
| 4 | Dockerfile + local testing | V2 |
| 5 | Deployment on VM + documentation | V2 |

## Links

GitHub: https://github.com/vovger/se-toolkit-hackathon
Telegram bot: https://t.me/@ContactPeoplebot
