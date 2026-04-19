"""
CLI commands - handles user commands.
Responsibility: Parse and execute user commands
"""
from typing import Dict, Any
from ..services.email_service import EmailService
from ..services.participant_service import ParticipantService
from ..services.template_service import TemplateService
from ..services.bulk_email_service import BulkEmailService
from ..utils.logger import Logger


class Commands:
    """CLI command handlers."""
    
    def __init__(self, config: Dict[str, Any], logger: Logger):
        """
        Initialize commands with configuration.
        
        Args:
            config: Configuration dictionary
            logger: Logger instance
        """
        self.config = config
        self.logger = logger
        
        # Initialize services
        self.email_service = EmailService(
            smtp_server=config['SMTP_SERVER'],
            smtp_port=config['SMTP_PORT'],
            email=config['SENDER_EMAIL'],
            password=config['SENDER_PASSWORD'],
            use_ssl=config.get('USE_SSL', False)
        )
        
        self.participant_service = ParticipantService()
        self.template_service = TemplateService()
        self.bulk_service = BulkEmailService(self.email_service, self.template_service)
    
    def test(self) -> bool:
        """
        Send test email to sender's own address.
        
        Returns:
            True if successful
        """
        self.logger.separator()
        self.logger.info("TEST MODE - Sending test email")
        self.logger.separator()
        
        test_recipient = {
            'email': self.config['SENDER_EMAIL'],
            'username': 'test_user',
            'password': 'TestPass123!'
        }
        
        template = self.template_service.get_credentials_template(
            self.config['PLATFORM_NAME'],
            self.config['PLATFORM_URL']
        )
        
        personalized = self.template_service.personalize(template['body'], test_recipient)
        
        try:
            self.email_service.send_email(
                to=test_recipient['email'],
                subject="TEST - " + template['subject'],
                body=personalized,
                cc=self.config.get('CC_RECIPIENTS'),
                html=True
            )
            
            self.logger.info(f"✓ Test email sent to {test_recipient['email']}")
            self.logger.info("Check your inbox and verify the email looks correct.")
            return True
            
        except Exception as e:
            self.logger.error(f"✗ Test failed: {str(e)}")
            return False
    
    def dry_run(self) -> bool:
        """
        Preview configuration without sending emails.
        
        Returns:
            True if successful
        """
        self.logger.separator()
        self.logger.info("DRY RUN MODE - Preview only")
        self.logger.separator()
        
        try:
            participants = self.participant_service.load_from_csv(
                self.config['PARTICIPANTS_FILE']
            )
            
            template = self.template_service.get_credentials_template(
                self.config['PLATFORM_NAME'],
                self.config['PLATFORM_URL']
            )
            
            self.logger.info(f"\nConfiguration:")
            self.logger.info(f"  SMTP: {self.config['SMTP_SERVER']}:{self.config['SMTP_PORT']}")
            self.logger.info(f"  From: {self.config['SENDER_EMAIL']}")
            self.logger.info(f"  Platform: {self.config['PLATFORM_NAME']}")
            self.logger.info(f"  URL: {self.config['PLATFORM_URL']}")
            
            cc = self.config.get('CC_RECIPIENTS', [])
            self.logger.info(f"  CC: {', '.join(cc) if cc else 'None'}")
            
            self.logger.info(f"\nParticipants: {len(participants)}")
            self.logger.info(f"Subject: {template['subject']}")
            
            self.logger.info(f"\nFirst 5 recipients:")
            for i, p in enumerate(participants[:5], 1):
                self.logger.info(f"  {i}. {p['email']} (username: {p['username']})")
            
            if len(participants) > 5:
                self.logger.info(f"  ... and {len(participants) - 5} more")
            
            self.logger.info("\nTo send emails, run: python run.py")
            return True
            
        except Exception as e:
            self.logger.error(f"Error: {str(e)}")
            return False
    
    def send(self) -> bool:
        """
        Send emails to all participants.
        
        Returns:
            True if all emails sent successfully
        """
        self.logger.separator()
        self.logger.info("PRODUCTION MODE - Sending emails")
        self.logger.separator()
        
        try:
            # Load participants
            participants = self.participant_service.load_from_csv(
                self.config['PARTICIPANTS_FILE']
            )
            
            self.logger.info(f"Loaded {len(participants)} participants")
            
            if len(participants) == 0:
                self.logger.error("No participants found!")
                return False
            
            # Show configuration
            self.logger.info(f"\nConfiguration:")
            self.logger.info(f"  Platform: {self.config['PLATFORM_NAME']}")
            self.logger.info(f"  URL: {self.config['PLATFORM_URL']}")
            
            cc = self.config.get('CC_RECIPIENTS', [])
            self.logger.info(f"  CC: {', '.join(cc) if cc else 'None'}")
            self.logger.info(f"  Total emails: {len(participants)}")
            
            # Confirm
            response = input(f"\nSend {len(participants)} emails? (yes/no): ")
            if response.lower() != 'yes':
                self.logger.info("Cancelled by user.")
                return False
            
            # Get template
            template = self.template_service.get_credentials_template(
                self.config['PLATFORM_NAME'],
                self.config['PLATFORM_URL']
            )
            
            # Progress callback
            def progress(current, total, email):
                status = "✓" if email else "✗"
                self.logger.info(f"{status} [{current}/{total}] {email}")
            
            # Send emails
            self.logger.info("\nSending emails...\n")
            result = self.bulk_service.send_bulk(
                recipients=participants,
                subject=template['subject'],
                template=template['body'],
                cc=cc if cc else None,
                delay=self.config.get('EMAIL_DELAY', 1.0),
                batch_size=self.config.get('BATCH_SIZE', 50),
                batch_delay=self.config.get('BATCH_DELAY', 10.0),
                progress_callback=progress
            )
            
            # Summary
            self.logger.separator()
            self.logger.info("SUMMARY")
            self.logger.separator()
            self.logger.info(f"Total: {result.total}")
            self.logger.info(f"Sent: {result.sent}")
            self.logger.info(f"Failed: {result.failed}")
            
            if result.failed > 0:
                self.logger.info("\nFailed emails:")
                for r in result.results:
                    if r['status'] == 'failed':
                        self.logger.error(f"  {r['email']}: {r.get('error', 'Unknown')}")
            
            self.logger.separator()
            
            return result.failed == 0
            
        except Exception as e:
            self.logger.error(f"Error: {str(e)}")
            return False
