"""
Email Notification System for CryptoQR
Sends QR code and JSON data to submitter's email using SendGrid
WITH PROFESSIONAL THUMBNAIL BANNER
"""

import os
import base64
import json
from datetime import datetime
from typing import Optional, Dict

# Try to import SendGrid
try:
    from sendgrid import SendGridAPIClient
    from sendgrid.helpers.mail import Mail, Attachment, FileContent, FileName, FileType, Disposition
    SENDGRID_AVAILABLE = True
except ImportError:
    SENDGRID_AVAILABLE = False
    print("⚠️  SendGrid not installed. Run: pip install sendgrid")


class EmailSender:
    """
    Handles sending submission confirmation emails with QR codes using SendGrid.
    
    SendGrid is more reliable than SMTP and works great with Render's free tier.
    """
    
    def __init__(self):
        # SendGrid configuration
        self.api_key = os.getenv("SENDGRID_API_KEY")
        self.sender_email = os.getenv("SENDER_EMAIL", "rishavjha8515@gmail.com")
        
        # Check if email is configured
        self.is_configured = bool(self.api_key and SENDGRID_AVAILABLE)
        
        if not self.api_key:
            print("⚠️  Email notifications disabled: SENDGRID_API_KEY not set")
        elif not SENDGRID_AVAILABLE:
            print("⚠️  Email notifications disabled: SendGrid not installed")
        else:
            print(f"✅ SendGrid email configured with sender: {self.sender_email}")
    
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
            # Create HTML body
            html_body = self._create_email_html(submission_data)
            
            # Create email message
            message = Mail(
                from_email=self.sender_email,
                to_emails=recipient_email,
                subject=f"🔒 CryptoQR Submission Confirmation - {submission_data['submission_id']}",
                html_content=html_body
            )
            
            # Attach QR code image
            qr_attachment = Attachment(
                FileContent(qr_image_base64),
                FileName(f"cryptoqr-{submission_data['submission_id']}.png"),
                FileType("image/png"),
                Disposition("attachment")
            )
            message.attachment = qr_attachment
            
            # Attach JSON data
            json_data = json.dumps(submission_data['qr_data'], indent=2)
            json_base64 = base64.b64encode(json_data.encode()).decode()
            
            json_attachment = Attachment(
                FileContent(json_base64),
                FileName(f"cryptoqr-data-{submission_data['submission_id']}.json"),
                FileType("application/json"),
                Disposition("attachment")
            )
            message.add_attachment(json_attachment)
            
            # Send email via SendGrid
            sg = SendGridAPIClient(self.api_key)
            response = sg.send(message)
            
            if response.status_code in [200, 201, 202]:
                print(f"✅ Email sent to {recipient_email} (Status: {response.status_code})")
                return True
            else:
                print(f"⚠️  Unexpected response from SendGrid: {response.status_code}")
                print(f"   Body: {response.body}")
                return False
            
        except Exception as e:
            print(f"❌ Failed to send email via SendGrid: {e}")
            import traceback
            print(f"   Traceback: {traceback.format_exc()}")
            return False
    
    def _create_email_html(self, submission_data: Dict) -> str:
        """Create beautiful HTML email body with professional thumbnail banner"""
        return f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 600px;
            margin: 0 auto;
            padding: 0;
            background: #f7fafc;
        }}
        
        .email-container {{
            background: white;
            border-radius: 16px;
            overflow: hidden;
            box-shadow: 0 4px 16px rgba(0,0,0,0.1);
            margin: 20px;
        }}
        
        .thumbnail-banner {{
            width: 100%;
            height: auto;
            display: block;
            background: linear-gradient(135deg, #1a202c 0%, #2d3748 100%);
        }}
        
        .thumbnail-banner img {{
            width: 100%;
            height: auto;
            max-height: 200px;
            object-fit: cover;
            display: block;
        }}
        
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}
        
        .logo {{
            font-size: 48px;
            margin-bottom: 10px;
        }}
        
        .header h1 {{
            margin: 0 0 10px 0;
            font-size: 28px;
        }}
        
        .header p {{
            margin: 0;
            opacity: 0.95;
        }}
        
        .content {{
            padding: 30px;
        }}
        
        .section {{
            background: #f7fafc;
            padding: 20px;
            border-radius: 12px;
            margin-bottom: 20px;
        }}
        
        .section h2 {{
            color: #2d3748;
            font-size: 18px;
            margin: 0 0 16px 0;
            font-weight: 700;
        }}
        
        .info-row {{
            display: flex;
            justify-content: space-between;
            padding: 12px 0;
            border-bottom: 1px solid #e2e8f0;
        }}
        
        .info-row:last-child {{
            border-bottom: none;
        }}
        
        .info-label {{
            color: #718096;
            font-weight: 600;
            font-size: 14px;
        }}
        
        .info-value {{
            color: #2d3748;
            font-family: 'Courier New', monospace;
            font-weight: 600;
            font-size: 14px;
            text-align: right;
            word-break: break-all;
        }}
        
        .qr-section {{
            text-align: center;
            background: white;
            padding: 24px;
            border-radius: 12px;
            border: 2px solid #e2e8f0;
            margin: 20px 0;
        }}
        
        .qr-section h3 {{
            color: #2d3748;
            font-size: 18px;
            margin: 0 0 12px 0;
        }}
        
        .attachments {{
            background: #ebf8ff;
            padding: 16px;
            border-radius: 8px;
            border-left: 4px solid #4299e1;
        }}
        
        .attachments ul {{
            margin: 8px 0 0 0;
            padding-left: 20px;
        }}
        
        .attachments li {{
            margin: 6px 0;
            color: #2c5282;
            font-size: 14px;
        }}
        
        .warning {{
            background: #fff5f5;
            border-left: 4px solid #f56565;
            padding: 16px;
            margin: 20px 0;
            border-radius: 4px;
        }}
        
        .warning strong {{
            color: #742a2a;
            display: block;
            margin-bottom: 8px;
        }}
        
        .warning ul {{
            margin: 8px 0 0 0;
            padding-left: 20px;
            color: #742a2a;
        }}
        
        .warning li {{
            margin: 4px 0;
        }}
        
        .button {{
            display: inline-block;
            padding: 14px 28px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            text-decoration: none;
            border-radius: 8px;
            font-weight: 600;
            font-size: 15px;
            margin: 10px 0;
        }}
        
        .cta-section {{
            text-align: center;
            padding: 24px;
        }}
        
        .footer {{
            text-align: center;
            color: #718096;
            font-size: 12px;
            padding: 24px;
            border-top: 1px solid #e2e8f0;
            background: #f7fafc;
        }}
        
        .footer p {{
            margin: 8px 0;
        }}
        
        .footer strong {{
            color: #2d3748;
        }}
        
        .footer a {{
            color: #667eea;
            text-decoration: none;
        }}
        
        @media only screen and (max-width: 600px) {{
            .email-container {{
                margin: 0;
                border-radius: 0;
            }}
            
            .content {{
                padding: 20px;
            }}
            
            .info-row {{
                flex-direction: column;
                gap: 4px;
            }}
            
            .info-value {{
                text-align: left;
                font-size: 13px;
            }}
        }}
    </style>
</head>
<body>
    <div class="email-container">
        <div class="thumbnail-banner">
            <img src="https://raw.githubusercontent.com/rishavjha8515-hub/cryptoqr/main/assets/cryptoqr-thumbnail.png.jpeg" 
                 alt="CryptoQR - Cryptographic proof-of-effort verification"
                 onerror="this.style.display='none'">
        </div>
        
        <div class="header">
            <div class="logo">🔒</div>
            <h1>Submission Confirmed</h1>
            <p>Your cryptographically signed submission is ready</p>
        </div>
        
        <div class="content">
            <div class="section">
                <h2>📋 Submission Details</h2>
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
                <h3>🔐 Your Cryptographic QR Code</h3>
                <p style="color: #718096; font-size: 14px; margin: 8px 0;">
                    This QR code contains your cryptographic signature and cannot be forged.
                </p>
                
                <div class="attachments">
                    <strong style="color: #2c5282;">📥 Attached Files:</strong>
                    <ul>
                        <li>🖼️ <code>cryptoqr-{submission_data['submission_id']}.png</code> - QR Code Image</li>
                        <li>📄 <code>cryptoqr-data-{submission_data['submission_id']}.json</code> - Signature Data</li>
                    </ul>
                </div>
            </div>
            
            <div class="warning">
                <strong>⚠️ Important Security Information:</strong>
                <ul>
                    <li>Keep both files safe - you'll need them for verification</li>
                    <li>Do not modify the files or they will become invalid</li>
                    <li>The QR code is cryptographically bound to your original file</li>
                    <li>Any tampering will be detected during verification</li>
                </ul>
            </div>
            
            <div class="cta-section">
                <a href="https://cryptoqr-pi.vercel.app/verify.html" class="button">
                    🔍 Verify Your Submission
                </a>
                <p style="color: #718096; font-size: 13px; margin-top: 12px;">
                    Judges can verify your submission at any time
                </p>
            </div>
        </div>
        
        <div class="footer">
            <p><strong>How to Use Your QR Code:</strong></p>
            <p>
                1. Download the attached QR code image and JSON file<br>
                2. Submit your project with the QR code attached<br>
                3. Judges can verify authenticity using the verification portal
            </p>
            
            <p style="margin-top: 20px; padding-top: 16px; border-top: 1px solid #e2e8f0;">
                <strong>CryptoQR</strong> - Cryptographic proof for the age of AI<br>
                Built at AlamedaHacks 2026 by Rishav Anand Kumar Jha<br>
                <a href="https://cryptoqr-pi.vercel.app/">cryptoqr-pi.vercel.app</a>
            </p>
            
            <p style="margin-top: 12px; font-size: 11px; color: #a0aec0;">
                Ed25519 signatures • SHA-256 hashing • Zero-trust verification
            </p>
        </div>
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
    print("Testing SendGrid email system...")
    
    test_data = {
        'submission_id': 'TEST123',
        'timestamp': '2026-01-05T12:34:56Z',
        'content_hash': 'a3f5d8c9e2b7f1a4d6c8e0f2a1b3c5d7',
        'qr_data': {'test': 'data'}
    }
    
    # Small test QR image (1x1 pixel PNG)
    test_qr = 'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=='
    
    if email_sender.is_configured:
        print("\n🧪 Sending test email...")
        result = email_sender.send_submission_email(
            "rishavjha8515@gmail.com",
            test_data,
            test_qr
        )
        print(f"\nTest email result: {'✅ Success' if result else '❌ Failed'}")
    else:
        print("\n⚠️  Configure SENDGRID_API_KEY env var to test")
        print("Get your API key from: https://app.sendgrid.com/settings/api_keys")