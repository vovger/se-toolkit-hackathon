# Project Plan: Contact Manager Bot

## Project Idea

**End-user:** Anyone who manages many contacts (freelancers, students, managers, regular users)

**Problem:** Contacts are scattered across different apps. Fixed fields (phone/email only) don't fit everyone's needs. Friends need birthdays, colleagues need company names, freelancers need project notes.

**One-sentence solution:** A Telegram bot where you create your own custom contact fields and find all data about a person instantly by name.

**Core feature:** User-defined custom fields with add/find/delete functionality.

## Components

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Backend | Python + python-telegram-bot | Handles commands, business logic, database operations |
| Database | SQLite | Stores people, custom fields, and contact values |
| Client (frontend) | Telegram bot | End-user interface for sending commands and receiving data |

## Implementation Plan

### Version 1 (Core Features)

**Goal:** Working product with basic CRUD operations.

**Commands:**
- `/addfield <name>` - create custom field
- `/fields` - list all fields
- `/add <person> <field> <value>` - add contact data
- `/find <person>` - find person by name
- `/list` - show all people
- `/delete <person>` - delete contact

### Version 2 (Advanced Features)

**Improvements on V1:**
- `/findby <field> <value>` - search by value
- `/edit <person> <field> <new_value>` - edit data
- `/export` - export all contacts to JSON
- Docker containerization
- Deployment on Ubuntu 24.04 VM

## Technical Stack

| Component | Technology |
|-----------|-----------|
| Language | Python 3.10 |
| Bot Framework | python-telegram-bot v20 |
| Database | SQLite |
| Container | Docker |
| Deployment | Ubuntu 24.04 VM |

## Timeline

| Day | Task |
|-----|------|
| 1 | Bot setup + database + /start + /addfield + /fields |
| 2 | /add + /find + /list + /delete |
| 3 | /edit + /findby + /export |
| 4 | Dockerfile + local testing |
| 5 | Deployment on VM + documentation |

## Deployment Instructions

1. Clone repository
2. Build Docker image: `docker build -t contact-bot .`
3. Run container: `docker run -d -e BOT_TOKEN="token" contact-bot`

## Links

- GitHub: https://github.com/vovger/se-toolkit-hackathon
- Deployed bot: [Telegram link to be added]
