# Bulk Email Credential Sender

Send personalized login credentials to multiple participants via email. Built with clean architecture and proper separation of concerns.

## What It Does

Automates sending username and password credentials to recording platform participants through professional HTML emails. Includes batch processing, rate limiting, logging, and security best practices.

## Quick Start

```bash
# Clone and setup
git clone git@github.com:jvcByte/send_bulk_email.git
cd send_bulk_email
python3 -m venv venv
source venv/bin/activate

# Configure
cp config.example.py config.py
# Edit config.py with your SMTP credentials and platform details

# Add participants
cp participants.example.csv participants.csv
# Add your participants (email, username, password)

# Test
python run.py --test

# Send
python run.py
```

## Commands

```bash
python run.py              # Send to all (requires confirmation)
python run.py --test       # Test email to yourself
python run.py --dry-run    # Preview without sending
```

## Project Structure

```
.
├── run.py                 # Entry point
├── config.py              # Configuration (not in git)
├── participants.csv       # Participant data (not in git)
│
└── src/
    ├── services/          # Business logic
    │   ├── email_service.py
    │   ├── participant_service.py
    │   ├── template_service.py
    │   └── bulk_email_service.py
    ├── utils/             # Utilities
    │   ├── logger.py
    │   └── config_loader.py
    └── cli/               # Commands
        └── commands.py
```

## Configuration

Edit `config.py`:

```python
# SMTP
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465
USE_SSL = True

# Credentials
SENDER_EMAIL = "your-email@gmail.com"
SENDER_PASSWORD = "your-app-password"  # Get from Google Account settings

# Platform
PLATFORM_NAME = "Your Platform"
PLATFORM_URL = "https://your-platform.com"

# Optional
CC_RECIPIENTS = ["mentor@example.com"]
EMAIL_DELAY = 1.0        # Seconds between emails
BATCH_SIZE = 50          # Emails per batch
BATCH_DELAY = 10         # Seconds between batches
```

## Gmail Setup

1. Enable 2-factor authentication
2. Generate app password: https://support.google.com/accounts/answer/185833
3. Use app password in `config.py`

## Features

- Personalized emails with participant usernames
- Professional HTML templates
- Batch processing with rate limiting
- Progress tracking and logging
- Test and dry-run modes
- CC support for administrators
- Secure (sensitive data never committed)

## Security

- `config.py` and `participants.csv` are in `.gitignore`
- Use app-specific passwords, not main passwords
- All activity logged to `email_log.txt`

## License

MIT License - See [LICENSE](LICENSE) file for details.
