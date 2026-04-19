"""
Configuration file for bulk email system.
Copy this file to config.py and update with your actual credentials.

IMPORTANT: Never commit config.py to git!
"""

# SMTP Configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465  # SSL port
USE_SSL = True

# Email Credentials
SENDER_EMAIL = "your-email@gmail.com"  # UPDATE THIS
SENDER_PASSWORD = "your-app-password"  # UPDATE THIS - Use app-specific password

# Platform Details
PLATFORM_NAME = "Your Platform Name"  # UPDATE THIS
PLATFORM_URL = "https://your-platform.com"  # UPDATE THIS

# CC Recipients (optional)
# Add email addresses that should receive a copy of every email sent
CC_RECIPIENTS = []
# Example: CC_RECIPIENTS = ["mentor1@example.com", "mentor2@example.com"]

# Email Settings
EMAIL_DELAY = 1.0  # Seconds to wait between emails (avoid rate limits)
BATCH_SIZE = 50    # Number of emails to send before taking a longer break
BATCH_DELAY = 10   # Seconds to wait after each batch

# File Paths
PARTICIPANTS_FILE = "participants.csv"
LOG_FILE = "email_log.txt"
