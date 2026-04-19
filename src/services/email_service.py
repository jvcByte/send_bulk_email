"""
Email service - handles email sending logic.
Responsibility: Send emails via SMTP
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Optional


class EmailService:
    """Service for sending emails via SMTP."""
    
    def __init__(self, smtp_server: str, smtp_port: int, email: str, password: str, use_ssl: bool = False):
        """
        Initialize email service with SMTP credentials.
        
        Args:
            smtp_server: SMTP server address
            smtp_port: SMTP port number
            email: Sender email address
            password: Sender email password
            use_ssl: Whether to use SSL connection
        """
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.email = email
        self.password = password
        self.use_ssl = use_ssl
    
    def connect(self):
        """Establish SMTP connection."""
        if self.use_ssl:
            server = smtplib.SMTP_SSL(self.smtp_server, self.smtp_port)
        else:
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
        server.login(self.email, self.password)
        return server
    
    def send_email(self, to: str, subject: str, body: str, 
                   cc: Optional[List[str]] = None, html: bool = True) -> bool:
        """
        Send a single email.
        
        Args:
            to: Recipient email address
            subject: Email subject
            body: Email body content
            cc: Optional list of CC recipients
            html: Whether body is HTML
            
        Returns:
            True if sent successfully, False otherwise
        """
        try:
            server = self.connect()
            
            msg = MIMEMultipart()
            msg['From'] = self.email
            msg['To'] = to
            msg['Subject'] = subject
            
            if cc:
                msg['Cc'] = ', '.join(cc)
            
            content_type = 'html' if html else 'plain'
            msg.attach(MIMEText(body, content_type))
            
            recipients = [to]
            if cc:
                recipients.extend(cc)
            
            server.send_message(msg)
            server.quit()
            
            return True
            
        except Exception as e:
            raise Exception(f"Failed to send email to {to}: {str(e)}")
