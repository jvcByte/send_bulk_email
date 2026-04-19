# Recording Platform Credential Mailer

Professional bulk email system with proper separation of concerns.

## Architecture

```
.
├── run.py                          # Entry point
├── config.py                       # Configuration (not in git)
├── config.example.py               # Configuration template
├── participants.csv                # Data (not in git)
├── participants.example.csv        # Data template
│
├── src/
│   ├── services/                   # Business logic layer
│   │   ├── email_service.py        # SMTP email sending
│   │   ├── participant_service.py  # Participant data management
│   │   ├── template_service.py     # Email template handling
│   │   └── bulk_email_service.py   # Bulk sending orchestration
│   │
│   ├── utils/                      # Utility layer
│   │   ├── logger.py               # Logging functionality
│   │   └── config_loader.py        # Configuration loading
│   │
│   └── cli/                        # Presentation layer
│       └── commands.py             # CLI command handlers
│
└── email_log.txt                   # Generated logs (not in git)
```

## Setup

### 1. Clone Repository

```bash
git clone git@github.com:jvcByte/send_bulk_email.git
cd send_bulk_email
```

### 2. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Configure

```bash
# Copy example config
cp config.example.py config.py

# Edit config.py with your credentials
nano config.py  # or use your preferred editor
```

Update these values in `config.py`:
- `SENDER_EMAIL` - Your email address
- `SENDER_PASSWORD` - Your app password
- `PLATFORM_NAME` - Your platform name
- `PLATFORM_URL` - Your platform URL
- `CC_RECIPIENTS` - Optional CC emails

### 4. Add Participants

```bash
# Copy example participants file
cp participants.example.csv participants.csv

# Add your participants
nano participants.csv
```

CSV format:
```csv
email,username,password
user@example.com,username1,Pass123!
```

## Usage

### Test Configuration

```bash
python run.py --test
```

Sends a test email to your own address to verify everything works.

### Preview (Dry Run)

```bash
python run.py --dry-run
```

Shows what will be sent without actually sending emails.

### Send to All Participants

```bash
python run.py
```

Sends emails to all participants (requires confirmation).

## Commands

| Command | Description |
|---------|-------------|
| `python run.py` | Send to all participants (requires confirmation) |
| `python run.py --test` | Send test email to your address |
| `python run.py --dry-run` | Preview configuration without sending |

## Separation of Concerns

### Services Layer (`src/services/`)
- `EmailService`: Handles SMTP connection and email sending
- `ParticipantService`: Manages participant data loading and validation
- `TemplateService`: Generates and personalizes email templates
- `BulkEmailService`: Orchestrates bulk sending with rate limiting

### Utils Layer (`src/utils/`)
- `Logger`: Handles logging to console and file
- `ConfigLoader`: Loads and validates configuration

### CLI Layer (`src/cli/`)
- `Commands`: Handles user commands (test, dry-run, send)

### Configuration (`config.py`)
- All settings in one place
- Easy to modify without touching code

## Benefits of This Architecture

1. **Single Responsibility**: Each class has one clear purpose
2. **Testability**: Services can be tested independently
3. **Maintainability**: Easy to find and modify specific functionality
4. **Extensibility**: Easy to add new features (e.g., new email templates)
5. **Reusability**: Services can be used in different contexts
6. **Dependency Injection**: Services are injected, not hardcoded

## Configuration Options

In `config.py`:

### SMTP Settings
- `SMTP_SERVER` - SMTP server address (default: smtp.gmail.com)
- `SMTP_PORT` - SMTP port (default: 465 for SSL)
- `USE_SSL` - Use SSL connection (default: True)

### Credentials
- `SENDER_EMAIL` - Your email address
- `SENDER_PASSWORD` - Your app-specific password

### Platform Details
- `PLATFORM_NAME` - Name of your platform
- `PLATFORM_URL` - URL of your platform

### Email Settings
- `EMAIL_DELAY` - Seconds between emails (default: 1.0)
- `BATCH_SIZE` - Emails per batch (default: 50)
- `BATCH_DELAY` - Seconds between batches (default: 10)
- `CC_RECIPIENTS` - List of CC email addresses (default: [])

### File Paths
- `PARTICIPANTS_FILE` - Path to participants CSV (default: participants.csv)
- `LOG_FILE` - Path to log file (default: email_log.txt)

## Gmail Setup

1. Enable 2-factor authentication on your Google account
2. Generate app password: https://support.google.com/accounts/answer/185833
3. Use the app password in `config.py` (not your regular password)

## SMTP Settings for Other Providers

### Gmail
```python
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465
USE_SSL = True
```

### Outlook
```python
SMTP_SERVER = "smtp-mail.outlook.com"
SMTP_PORT = 587
USE_SSL = False  # Uses STARTTLS
```

### Yahoo
```python
SMTP_SERVER = "smtp.mail.yahoo.com"
SMTP_PORT = 587
USE_SSL = False  # Uses STARTTLS
```

## Security

- `config.py` is in `.gitignore` - never committed to git
- `participants.csv` is in `.gitignore` - never committed to git
- Use app-specific passwords, not your main password
- Review `email_log.txt` before sharing (may contain sensitive info)

## Logs

All activity is logged to `email_log.txt` with timestamps:
- Successful sends
- Failed sends with error messages
- Summary statistics

## Troubleshooting

### "Network is unreachable"
- Check your internet connection
- Try port 587 instead of 465
- Check if your firewall blocks SMTP ports

### "Authentication failed"
- Make sure you're using an app-specific password
- Verify email and password are correct
- Check if 2FA is enabled (required for app passwords)

### "Connection refused"
- Verify SMTP server and port are correct
- Try toggling `USE_SSL` setting

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

[MIT](./LICENSE) License
