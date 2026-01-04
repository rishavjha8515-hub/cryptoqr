"""
Email Notification System for CryptoQR
Sends QR code and JSON data to submitter's email
"""

import os
import smtplib
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication
from datetime import datetime
from typing import Optional, Dict
import json


class EmailSender:
    """
    Handles sending submission confirmation emails with QR codes.
    
    Uses Gmail SMTP (free tier) or can be configured for other providers.
    """
    
    def __init__(self):
        # Email configuration from environment variables
        self.smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.sender_email = os.getenv("SENDER_EMAIL")
        self.sender_password = os.getenv("SENDER_PASSWORD")
        
        # Check if email is configured
        self.is_configured = bool(self.sender_email and self.sender_password)
        
        if not self.is_configured:
            print("⚠️  Email notifications disabled (no credentials configured)")
    
    def send_submission_email(
        self,
        recipient_email: str,
        submission_data: Dict,
        qr_image_base64: str
    ) -> bool:
        """
        Send submission confirmation email with QR code and JSON data.
        
        Args:
            recipient_email: Recipient's email address
            submission_data: Submission metadata (ID, timestamp, etc.)
            qr_image_base64: Base64-encoded QR code image
            
        Returns:
            True if email sent successfully, False otherwise
        """
        if not self.is_configured:
            print("❌ Email not configured - skipping email notification")
            return False
        
        try:
            # Create message
            msg = MIMEMultipart('related')
            msg['From'] = self.sender_email
            msg['To'] = recipient_email
            msg['Subject'] = f"🔐 CryptoQR Submission Confirmation - {submission_data['submission_id']}"
            
            # Create HTML body
            html_body = self._create_email_html(submission_data)
            msg.attach(MIMEText(html_body, 'html'))
            
            # Attach QR code image
            qr_image_bytes = base64.b64decode(qr_image_base64)
            qr_image = MIMEImage(qr_image_bytes, name=f"cryptoqr-{submission_data['submission_id']}.png")
            qr_image.add_header('Content-ID', '<qr_image>')
            qr_image.add_header('Content-Disposition', 'attachment', 
                              filename=f"cryptoqr-{submission_data['submission_id']}.png")
            msg.attach(qr_image)
            
            # Attach JSON data
            json_data = json.dumps(submission_data['qr_data'], indent=2)
            json_attachment = MIMEApplication(json_data, Name=f"cryptoqr-data-{submission_data['submission_id']}.json")
            json_attachment['Content-Disposition'] = f'attachment; filename="cryptoqr-data-{submission_data["submission_id"]}.json"'
            msg.attach(json_attachment)
            
            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)
            
            print(f"✅ Email sent to {recipient_email}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to send email: {e}")
            return False
    
    def _create_email_html(self, submission_data: Dict) -> str:
        """Create beautiful HTML email body"""
        return f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 12px;
            text-align: center;
            margin-bottom: 30px;
        }}
        .logo {{
            font-size: 48px;
            margin-bottom: 10px;
        }}
        .content {{
            background: #f7fafc;
            padding: 30px;
            border-radius: 12px;
            margin-bottom: 20px;
        }}
        .info-row {{
            display: flex;
            justify-content: space-between;
            padding: 12px 0;
            border-bottom: 1px solid #e2e8f0;
        }}
        .info-label {{
            color: #718096;
            font-weight: 600;
        }}
        .info-value {{
            color: #2d3748;
            font-family: 'Courier New', monospace;
            font-weight: 600;
        }}
        .qr-section {{
            text-align: center;
            padding: 20px;
            background: white;
            border-radius: 12px;
            margin: 20px 0;
        }}
        .qr-image {{
            max-width: 300px;
            border: 2px solid #667eea;
            border-radius: 8px;
            margin: 20px auto;
        }}
        .warning {{
            background: #fff5f5;
            border-left: 4px solid #f56565;
            padding: 15px;
            margin: 20px 0;
            border-radius: 4px;
        }}
        .footer {{
            text-align: center;
            color: #718096;
            font-size: 12px;
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid #e2e8f0;
        }}
        .button {{
            display: inline-block;
            padding: 12px 24px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            text-decoration: none;
            border-radius: 8px;
            font-weight: 600;
            margin: 10px 0;
        }}
    </style>
</head>
<body>
    <div class="header">
        <div class="logo">🔐</div>
        <h1>CryptoQR Submission Confirmed</h1>
        <p>Your cryptographically signed submission is ready</p>
    </div>
    
    <div class="content">
        <h2>Submission Details</h2>
        <div class="info-row">
            <span class="info-label">Submission ID:</span>
            <span class="info-value">{submission_data['submission_id']}</span>
        </div>
        <div class="info-row">
            <span class="info-label">Timestamp:</span>
            <span class="info-value">{datetime.fromisoformat(submission_data['timestamp'].replace('Z', '+00:00')).strftime('%B %d, %Y at %I:%M %p UTC')}</span>
        </div>
        <div class="info-row">
            <span class="info-label">Content Hash:</span>
            <span class="info-value">{submission_data['content_hash'][:16]}...</span>
        </div>
    </div>
    
    <div class="qr-section">
        <h2>Your Cryptographic QR Code</h2>
        <p>This QR code contains your cryptographic signature and cannot be forged.</p>
        <img src="cid:qr_image" class="qr-image" alt="QR Code">
        <p><strong>Attached Files:</strong></p>
        <ul style="text-align: left; display: inline-block;">
            <li>📥 <code>cryptoqr-{submission_data['submission_id']}.png</code> - QR Code Image</li>
            <li>📄 <code>cryptoqr-data-{submission_data['submission_id']}.json</code> - Signature Data</li>
        </ul>
    </div>
    
    <div class="warning">
        <strong>⚠️ Important:</strong>
        <ul>
            <li>Keep both files safe - you'll need them for verification</li>
            <li>Do not modify the files or they will become invalid</li>
            <li>The QR code is cryptographically bound to your original file</li>
        </ul>
    </div>
    
    <div style="text-align: center; margin: 30px 0;">
        <a href="https://cryptoqr-eta.vercel.app/verify.html" class="button">
            Verify Your Submission
        </a>
    </div>
    
    <div class="footer">
        <p><strong>How to Use:</strong></p>
        <p>1. Download the attached QR code image and JSON file<br>
        2. Submit your project with the QR code attached<br>
        3. Judges can verify authenticity using the verification portal</p>
        
        <p style="margin-top: 20px;">
            <strong>CryptoQR</strong> - Cryptographic proof for the age of AI<br>
            Built at AlamedaHacks 2026<br>
            <a href="https://cryptoqr-eta.vercel.app">cryptoqr-eta.vercel.app</a>
        </p>
    </div>
</body>
</html>
        """


# Global email sender instance
email_sender = EmailSender()


def send_submission_notification(
    recipient_email: str,
    submission_data: Dict,
    qr_image_base64: str
) -> bool:
    """
    Convenience function to send submission email.
    
    Args:
        recipient_email: Recipient's email
        submission_data: Submission metadata
        qr_image_base64: Base64 QR code image
        
    Returns:
        True if sent successfully
    """
    if not recipient_email:
        return False
    
    return email_sender.send_submission_email(
        recipient_email,
        submission_data,
        qr_image_base64
    )


if __name__ == "__main__":
    # Test email system
    print("Testing email system...")
    
    test_data = {
        'submission_id': 'TEST123',
        'timestamp': '2026-01-05T12:34:56Z',
        'content_hash': 'a3f5d8c9e2b7f1a4d6c8e0f2a1b3c5d7',
        'qr_data': {'test': 'data'}
    }
    
    # Small test QR image (1x1 pixel PNG)
    test_qr = 'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=='
    
    if email_sender.is_configured:
        result = email_sender.send_submission_email(
            "test@example.com",
            test_data,
            test_qr
        )
        print(f"Test email result: {'✅ Success' if result else '❌ Failed'}")
    else:
        print("⚠️  Configure SENDER_EMAIL and SENDER_PASSWORD env vars to test")