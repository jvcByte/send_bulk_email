"""
Template service - handles email template operations.
Responsibility: Generate and personalize email templates
"""
from typing import Dict


class TemplateService:
    """Service for managing email templates."""
    
    @staticmethod
    def personalize(template: str, data: Dict[str, str]) -> str:
        """
        Replace placeholders in template with actual data.
        
        Args:
            template: Template string with {placeholders}
            data: Dictionary of placeholder values
            
        Returns:
            Personalized string
        """
        result = template
        for key, value in data.items():
            placeholder = f"{{{key}}}"
            result = result.replace(placeholder, value)
        return result
    
    @staticmethod
    def get_credentials_template(platform_name: str, platform_url: str) -> Dict[str, str]:
        """
        Get the credentials email template.
        
        Args:
            platform_name: Name of the platform
            platform_url: URL of the platform
            
        Returns:
            Dictionary with 'subject' and 'body' keys
        """
        subject = "Your Recording Platform Access Credentials"
        
        body = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.8;
            color: #2c3e50;
            max-width: 650px;
            margin: 0 auto;
            padding: 0;
            background-color: #f4f4f4;
        }}
        .email-wrapper {{
            background-color: #ffffff;
            margin: 20px;
            border-radius: 2px;
            overflow: hidden;
            box-shadow: 0 0 20px rgba(0,0,0,0.08);
        }}
        .header {{
            background-color: #1a1a2e;
            color: #ffffff;
            padding: 40px 30px;
            text-align: center;
        }}
        .header h1 {{
            margin: 0;
            font-size: 26px;
            font-weight: 600;
            letter-spacing: 0.5px;
        }}
        .content {{
            padding: 40px 30px;
        }}
        .greeting {{
            font-size: 16px;
            margin-bottom: 20px;
        }}
        .credentials-box {{
            background-color: #f8f9fa;
            border: 1px solid #e1e4e8;
            border-radius: 4px;
            padding: 25px;
            margin: 30px 0;
        }}
        .credentials-title {{
            font-size: 18px;
            font-weight: 600;
            color: #1a1a2e;
            margin: 0 0 20px 0;
            padding-bottom: 15px;
            border-bottom: 2px solid #1a1a2e;
        }}
        .credential-row {{
            display: table;
            width: 100%;
            margin: 15px 0;
        }}
        .credential-label {{
            font-weight: 600;
            color: #5a6c7d;
            font-size: 14px;
            margin-bottom: 5px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        .credential-value {{
            color: #1a1a2e;
            font-family: 'Courier New', Courier, monospace;
            font-size: 15px;
            background-color: #ffffff;
            padding: 12px 15px;
            border: 1px solid #d1d5db;
            border-radius: 3px;
            margin-top: 5px;
            word-break: break-all;
        }}
        .notice {{
            background-color: #fffbeb;
            border-left: 4px solid #f59e0b;
            padding: 18px 20px;
            margin: 25px 0;
            border-radius: 3px;
        }}
        .notice-title {{
            font-weight: 600;
            color: #92400e;
            margin: 0 0 8px 0;
            font-size: 15px;
        }}
        .notice-text {{
            color: #78350f;
            margin: 0;
            font-size: 14px;
        }}
        .footer {{
            background-color: #f8f9fa;
            padding: 30px;
            text-align: center;
            border-top: 1px solid #e1e4e8;
        }}
        .footer-text {{
            color: #6c757d;
            font-size: 14px;
            margin: 5px 0;
        }}
        .signature {{
            font-weight: 600;
            color: #1a1a2e;
            margin-top: 15px;
        }}
    </style>
</head>
<body>
    <div class="email-wrapper">
        <div class="header">
            <h1>{platform_name}</h1>
        </div>
        
        <div class="content">
            <div class="greeting">
                <p>Dear Participant,</p>
            </div>
            
            <p>Your account has been successfully created. Please find your login credentials below to access the recording platform.</p>
            
            <div class="credentials-box">
                <div class="credentials-title">Account Credentials</div>
                
                <div class="credential-row">
                    <div class="credential-label">Platform URL</div>
                    <div class="credential-value">{platform_url}</div>
                </div>
                
                <div class="credential-row">
                    <div class="credential-label">Username</div>
                    <div class="credential-value">{{username}}</div>
                </div>
                
                <div class="credential-row">
                    <div class="credential-label">Password</div>
                    <div class="credential-value">{{password}}</div>
                </div>
            </div>
            
            <div class="notice">
                <div class="notice-title">Security Notice</div>
                <p class="notice-text">For your security, please change your password immediately after your first login. Keep your credentials confidential and do not share them with anyone.</p>
            </div>
            
            <p>If you encounter any issues accessing the platform or have questions, please contact the coding mentors for assistance.</p>
        </div>
        
        <div class="footer">
            <p class="footer-text">Best regards,</p>
            <p class="signature">DBI Coding Mentors</p>
            <p class="footer-text" style="margin-top: 20px; font-size: 12px;">This is an automated message. Please do not reply to this email.</p>
        </div>
    </div>
</body>
</html>
"""
        
        return {
            'subject': subject,
            'body': body
        }
