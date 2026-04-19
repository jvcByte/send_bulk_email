"""
Bulk email service - orchestrates bulk email sending.
Responsibility: Coordinate email sending to multiple recipients with rate limiting
"""
import time
from typing import List, Dict, Optional, Callable
from .email_service import EmailService
from .template_service import TemplateService


class BulkEmailResult:
    """Result of bulk email operation."""
    
    def __init__(self):
        self.total = 0
        self.sent = 0
        self.failed = 0
        self.results = []
    
    def add_success(self, email: str):
        """Record successful send."""
        self.total += 1
        self.sent += 1
        self.results.append({'email': email, 'status': 'sent'})
    
    def add_failure(self, email: str, error: str):
        """Record failed send."""
        self.total += 1
        self.failed += 1
        self.results.append({'email': email, 'status': 'failed', 'error': error})


class BulkEmailService:
    """Service for sending bulk emails with rate limiting."""
    
    def __init__(self, email_service: EmailService, template_service: TemplateService):
        """
        Initialize bulk email service.
        
        Args:
            email_service: Email service instance
            template_service: Template service instance
        """
        self.email_service = email_service
        self.template_service = template_service
    
    def send_bulk(
        self,
        recipients: List[Dict[str, str]],
        subject: str,
        template: str,
        cc: Optional[List[str]] = None,
        delay: float = 1.0,
        batch_size: int = 50,
        batch_delay: float = 10.0,
        progress_callback: Optional[Callable[[int, int, str], None]] = None
    ) -> BulkEmailResult:
        """
        Send personalized emails to multiple recipients.
        
        Args:
            recipients: List of recipient data dictionaries
            subject: Email subject
            template: Email template with {placeholders}
            cc: Optional CC recipients
            delay: Seconds between emails
            batch_size: Emails per batch before longer pause
            batch_delay: Seconds between batches
            progress_callback: Optional callback(current, total, email)
            
        Returns:
            BulkEmailResult with statistics
        """
        result = BulkEmailResult()
        total = len(recipients)
        
        for index, recipient in enumerate(recipients, 1):
            email = recipient.get('email', 'unknown')
            
            try:
                # Personalize template
                personalized_body = self.template_service.personalize(template, recipient)
                
                # Send email
                self.email_service.send_email(
                    to=email,
                    subject=subject,
                    body=personalized_body,
                    cc=cc,
                    html=True
                )
                
                result.add_success(email)
                
                # Progress callback
                if progress_callback:
                    progress_callback(index, total, email)
                
                # Rate limiting
                if index % batch_size == 0 and index < total:
                    time.sleep(batch_delay)
                else:
                    time.sleep(delay)
                    
            except Exception as e:
                result.add_failure(email, str(e))
                
                if progress_callback:
                    progress_callback(index, total, email)
        
        return result
