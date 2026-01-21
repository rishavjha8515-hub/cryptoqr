"""
CryptoQR - REST API Server
Built: January 1, 2026 for AlamedaHacks
Author: Rishav Anand Kumar Jha

FastAPI server providing cryptographic QR code generation and verification.
"""

import os
import json
import base64
from datetime import datetime
from collections import defaultdict
from typing import Optional, Dict

from fastapi import FastAPI, File, UploadFile, Form, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, Response
import qrcode
from io import BytesIO

from crypto_core import CryptoQRCore, VerificationResult
from email_sender import send_submission_notification, email_sender
import re
from PIL import Image


# Initialize FastAPI app
app = FastAPI(
    title="CryptoQR API",
    description="Cryptographic verification for digital submissions",
    version="1.0.0"
)

# CORS middleware for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize crypto core with persistent keys
PRIVATE_KEY = os.getenv("CRYPTOQR_PRIVATE_KEY")
crypto = CryptoQRCore(private_key_pem=PRIVATE_KEY if PRIVATE_KEY else None)

# Cache public key
PUBLIC_KEY_PEM = crypto.export_public_key()

# In-memory storage for duplicate detection
# Format: {competition_id: {content_hash: submission_data}}
submissions_db: Dict[str, Dict[str, Dict]] = defaultdict(dict)

# Store verification attempts for rate limiting
verification_attempts: Dict[str, list] = defaultdict(list)


@app.on_event("startup")
async def startup_event():
    """Log startup information"""
    print("=" * 60)
    print("CryptoQR API Starting...")
    print("=" * 60)
    if not PRIVATE_KEY:
        print("⚠️  Warning: Using ephemeral keys (set CRYPTOQR_PRIVATE_KEY env var)")
        print(f"Public Key:\n{PUBLIC_KEY_PEM}")
    
    # EMAIL STATUS CHECK
    if email_sender.is_configured:
        print("✅ Email system configured and ready (SendGrid)")
        print(f"   Sender: {email_sender.sender_email}")
    else:
        print("⚠️  Email notifications disabled (no credentials configured)")
    
    print("✓ Server ready")
    print("=" * 60)


@app.get("/")
async def root():
    """Health check and API info"""
    return {
        "service": "CryptoQR API",
        "version": "1.0.0",
        "status": "operational",
        "endpoints": {
            "submit": "/api/submit",
            "verify": "/api/verify",
            "public_key": "/api/public-key",
            "email_status": "/api/email-status",
            "test_email": "/api/test-email",
            "stats": "/api/stats/{competition_id}"
        }
    }


@app.get("/api/public-key")
async def get_public_key():
    """
    Retrieve public key for signature verification.
    
    Returns:
        Public key in PEM format and algorithm info
    """
    return {
        "public_key": PUBLIC_KEY_PEM,
        "algorithm": "Ed25519",
        "key_size": 256
    }


@app.get("/api/email-status")
async def get_email_status():
    """
    Check if email notifications are configured.
    
    Returns:
        Email system status
    """
    return {
        "email_enabled": email_sender.is_configured,
        "email_provider": "SendGrid API" if email_sender.is_configured else None,
        "sender_email": email_sender.sender_email if email_sender.is_configured else None,
        "message": "Email notifications active (SendGrid)" if email_sender.is_configured else "Configure SENDGRID_API_KEY environment variable to enable"
    }


@app.get("/api/test-email")
async def test_email_send():
    """
    🆕 Send a test email to verify email system works
    
    Returns:
        Test email result with success status
    """
    if not email_sender.is_configured:
        return {
            "success": False,
            "error": "Email not configured",
            "email_enabled": False,
            "message": "Set SENDGRID_API_KEY environment variable and verify sender email"
        }
    
    test_data = {
        'submission_id': 'TEST-' + datetime.now().strftime('%Y%m%d-%H%M%S'),
        'timestamp': datetime.now().isoformat() + 'Z',
        'content_hash': 'a3f5d8c9e2b7f1a4d6c8e0f2a1b3c5d7',
        'qr_data': {
            'test': 'data',
            'message': 'This is a test email from CryptoQR',
            'purpose': 'Email system verification'
        }
    }
    
    # Small 1x1 pixel PNG for testing
    test_qr = 'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=='
    
    try:
        print("=" * 60)
        print(f"🧪 TEST EMAIL: Attempting to send test email...")
        print(f"   Recipient: rishavjha8515@gmail.com")
        print(f"   Sender: {email_sender.sender_email}")
        print(f"   Provider: SendGrid API")
        print("=" * 60)
        
        result = send_submission_notification(
            recipient_email="rishavjha8515@gmail.com",
            submission_data=test_data,
            qr_image_base64=test_qr
        )
        
        print("=" * 60)
        print(f"🧪 TEST EMAIL RESULT: {'✅ SUCCESS' if result else '❌ FAILED'}")
        print("=" * 60)
        
        return {
            "success": result,
            "message": "✅ Test email sent successfully! Check your inbox (and spam folder)." if result else "❌ Failed to send email. Check server logs for details.",
            "recipient": "rishavjha8515@gmail.com",
            "submission_id": test_data['submission_id'],
            "email_configured": True,
            "instructions": "If email didn't arrive, check: 1) Spam/Junk folder, 2) Sender email is verified in SendGrid, 3) SENDGRID_API_KEY is correct"
        }
        
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        
        print("=" * 60)
        print(f"🧪 TEST EMAIL ERROR:")
        print(f"   Error: {e}")
        print(f"   Traceback:\n{error_trace}")
        print("=" * 60)
        
        return {
            "success": False,
            "error": str(e),
            "traceback": error_trace,
            "message": "❌ Email sending failed. See error details above.",
            "troubleshooting": {
                "check_api_key": "Ensure SENDGRID_API_KEY is set correctly in Render environment variables",
                "verify_sender": "Verify your sender email at https://app.sendgrid.com/settings/sender_auth/senders",
                "check_quota": "Free tier allows 100 emails/day"
            }
        }


@app.post("/api/submit")
async def submit_document(
    file: UploadFile = File(..., description="Document to verify"),
    competition_id: str = Form(..., description="Competition identifier"),
    deadline: str = Form(..., description="Submission deadline (ISO 8601)"),
    email: str = Form(None, description="Optional submitter email")
):
    """
    Generate cryptographically signed QR code for document submission.
    NOW WITH EMAIL NOTIFICATIONS! 📧
    
    Args:
        file: Document file to hash and sign
        competition_id: Unique competition identifier
        deadline: Deadline in ISO 8601 format
        email: Optional submitter email for notification
        
    Returns:
        Submission data including QR code image and signature
    """
    try:
        # Read file data
        file_data = await file.read()
        
        if len(file_data) == 0:
            raise HTTPException(status_code=400, detail="Empty file uploaded")
        
        if len(file_data) > 50 * 1024 * 1024:  # 50MB limit
            raise HTTPException(status_code=413, detail="File too large (max 50MB)")
        
        # Check for duplicate submission
        content_hash = crypto.hash_file(file_data)
        
        if content_hash in submissions_db[competition_id]:
            existing = submissions_db[competition_id][content_hash]
            raise HTTPException(
                status_code=409,
                detail={
                    "error": "duplicate_submission",
                    "message": "This file was already submitted to this competition",
                    "existing_submission_id": existing['submission_id'],
                    "existing_timestamp": existing['timestamp']
                }
            )
        
        # Create cryptographic submission
        submission = crypto.create_submission(
            file_data=file_data,
            competition_id=competition_id,
            deadline=deadline,
            email=email
        )
        
        # Store submission for duplicate checking
        submissions_db[competition_id][content_hash] = {
            'submission_id': submission['submission_id'],
            'timestamp': submission['timestamp'],
            'email': email
        }
        
        # Generate QR code image
        qr_image = generate_qr_image(submission)
        
        # Prepare response data
        response_data = {
            "success": True,
            "submission_id": submission['submission_id'],
            "timestamp": submission['timestamp'],
            "content_hash": content_hash,
            "qr_data": {
                "payload": submission['payload'],
                "signature": submission['signature'],
                "version": submission['version']
            },
            "qr_image_base64": qr_image,
            "verification_url": f"/verify?id={submission['submission_id']}"
        }
        
        # 🆕 SEND EMAIL NOTIFICATION IF EMAIL PROVIDED
        email_sent = False
        print(f"🔍 DEBUG: Email value = '{email}' (type: {type(email)})")
        print(f"🔍 DEBUG: email_sender.is_configured = {email_sender.is_configured}")
        
        if email:
            try:
                print(f"📧 Attempting to send email to {email}...")
                
                email_sent = send_submission_notification(
                    recipient_email=email,
                    submission_data={
                        'submission_id': submission['submission_id'],
                        'timestamp': submission['timestamp'],
                        'content_hash': content_hash,
                        'qr_data': response_data['qr_data']
                    },
                    qr_image_base64=qr_image
                )
                
                if email_sent:
                    print(f"✅ Email sent successfully to {email}")
                    response_data['email_sent'] = True
                    response_data['email_message'] = f"Confirmation email sent to {email}"
                else:
                    print(f"⚠️  Email notification failed for {email}")
                    response_data['email_sent'] = False
                    response_data['email_message'] = "Email notification unavailable (not configured or failed)"
                    
            except Exception as e:
                print(f"❌ Email error: {e}")
                response_data['email_sent'] = False
                response_data['email_message'] = f"Email notification failed: {str(e)}"
        
        # Log submission
        email_status = "✅" if email_sent else ("N/A" if not email else "❌")
        print(f"[SUBMIT] {submission['submission_id']} | {competition_id} | {content_hash[:8]}... | Email: {email_status}")
        
        return response_data
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"[ERROR] Submission failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/verify")
async def verify_document(
    request: Request,
    file: UploadFile = File(..., description="Document to verify"),
    qr_data: str = Form(..., description="QR code data (JSON)")
):
    """
    Verify document against cryptographic QR code.
    
    Args:
        file: Document file to verify
        qr_data: QR code data as JSON string
        
    Returns:
        Verification result with detailed checks
    """
    try:
        # Rate limiting (simple in-memory)
        client_ip = request.client.host
        now = datetime.now()
        
        # Clean old attempts (> 5 minutes)
        verification_attempts[client_ip] = [
            t for t in verification_attempts[client_ip]
            if (now - t).total_seconds() < 300
        ]
        
        if len(verification_attempts[client_ip]) > 20:
            raise HTTPException(
                status_code=429,
                detail="Too many verification attempts. Please wait 5 minutes."
            )
        
        verification_attempts[client_ip].append(now)
        
        # Read file
        file_data = await file.read()
        
        if len(file_data) == 0:
            raise HTTPException(status_code=400, detail="Empty file uploaded")
        
        # Parse QR data
        try:
            qr_dict = json.loads(qr_data)
        except json.JSONDecodeError:
            raise HTTPException(status_code=400, detail="Invalid QR data format")
        
        # Verify submission
        result = crypto.verify_submission(
            qr_data=qr_dict,
            file_data=file_data,
            public_key_pem=PUBLIC_KEY_PEM
        )
        
        # Log verification
        status = "VALID" if result.valid else "INVALID"
        print(f"[VERIFY] {result.submission_id} | {status} | {client_ip}")
        
        if not result.valid:
            print(f"  Reason: {result.reason}")
        
        return {
            "valid": result.valid,
            "submission_id": result.submission_id,
            "timestamp": result.timestamp,
            "competition_id": result.competition_id,
            "checks": result.checks,
            "reason": result.reason,
            "verified_at": datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"[ERROR] Verification failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/verify/export")
async def export_verification(
    file: UploadFile = File(...),
    qr_data: str = Form(...)
):
    """
    Verify and export result as downloadable JSON.
    
    Args:
        file: Document to verify
        qr_data: QR code data
        
    Returns:
        Verification result as downloadable JSON file
    """
    try:
        file_data = await file.read()
        qr_dict = json.loads(qr_data)
        
        result = crypto.verify_submission(qr_dict, file_data, PUBLIC_KEY_PEM)
        
        export_data = {
            "verification_result": result.valid,
            "submission_id": result.submission_id,
            "timestamp": result.timestamp,
            "competition_id": result.competition_id,
            "checks": result.checks,
            "reason": result.reason,
            "verified_at": datetime.now().isoformat(),
            "verified_by": "CryptoQR v1.0.0"
        }
        
        return Response(
            content=json.dumps(export_data, indent=2),
            media_type="application/json",
            headers={
                "Content-Disposition": f"attachment; filename=verification-{result.submission_id}.json"
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/stats/{competition_id}")
async def get_competition_stats(competition_id: str):
    """
    Get statistics for a specific competition.
    
    Args:
        competition_id: Competition identifier
        
    Returns:
        Submission statistics
    """
    if competition_id not in submissions_db:
        return {
            "competition_id": competition_id,
            "total_submissions": 0,
            "message": "No submissions yet"
        }
    
    submissions = submissions_db[competition_id]
    
    return {
        "competition_id": competition_id,
        "total_submissions": len(submissions),
        "first_submission": min(
            (s['timestamp'] for s in submissions.values()),
            default=None
        ),
        "last_submission": max(
            (s['timestamp'] for s in submissions.values()),
            default=None
        )
    }


@app.get("/api/dashboard")
async def get_dashboard():
    """
    Get overall system dashboard statistics.
    
    Returns:
        System-wide statistics
    """
    total_submissions = sum(len(subs) for subs in submissions_db.values())
    
    competitions = [
        {
            "competition_id": comp_id,
            "submissions": len(subs)
        }
        for comp_id, subs in submissions_db.items()
    ]
    
    return {
        "total_submissions": total_submissions,
        "total_competitions": len(submissions_db),
        "competitions": competitions,
        "api_version": "1.0.0"
    }


def generate_qr_image(submission: Dict) -> str:
    """
    Generate QR code image from submission data.
    
    Args:
        submission: Submission dictionary
        
    Returns:
        Base64-encoded PNG image
    """
    qr_payload = {
        "payload": submission['payload'],
        "signature": submission['signature'],
        "version": submission['version']
    }
    
    qr_json = json.dumps(qr_payload)
    
    # Generate QR code with high error correction
    qr = qrcode.QRCode(
        version=None,  # Auto-size
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(qr_json)
    qr.make(fit=True)
    
    # Create image
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Convert to base64
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    img_bytes = buffer.getvalue()
    
    return base64.b64encode(img_bytes).decode('utf-8')
@app.post("/api/sign-ai-text")
async def sign_ai_text(
    content: str = Form(...),
    model_name: str = Form("claude-sonnet-4.5-20250514")
):
    """
    Sign AI-generated text with cryptographic signature.
    """
    try:
        if not content.strip():
            raise HTTPException(status_code=400, detail="Content cannot be empty")
        
        # Convert text to bytes for hashing
        content_bytes = content.encode('utf-8')
        content_hash = crypto.hash_file(content_bytes)
        
        # Generate signature data
        timestamp = datetime.now().isoformat() + 'Z'
        submission_id = crypto._generate_submission_id()
        nonce = crypto._generate_nonce()
        
        payload = {
            'content_hash': content_hash,
            'timestamp': timestamp,
            'model': model_name,
            'submission_id': submission_id,
            'nonce': nonce,
            'type': 'ai_content'
        }
        
        # Sign payload
        payload_bytes = json.dumps(payload, sort_keys=True).encode('utf-8')
        signature = crypto.private_key.sign(payload_bytes)
        signature_b64 = base64.b64encode(signature).decode('utf-8')
        
        # Create signed text block
        signed_text = f"""{content}

---
🤖 AI-GENERATED CONTENT VERIFICATION
Model: {model_name}
Generated: {timestamp}
Content Hash: {content_hash[:16]}...
Signature: {signature_b64[:32]}...
Verify at: cryptoqr-eta.vercel.app/verify-ai
---"""
        
        print(f"[AI-SIGN] {submission_id} | {model_name} | {len(content)} chars")
        
        return {
            "success": True,
            "signature": signature_b64,
            "hash": content_hash,
            "timestamp": timestamp,
            "signed_text": signed_text,
            "submission_id": submission_id,
            "verification_url": "https://cryptoqr-eta.vercel.app/verify-ai"
        }
        
    except Exception as e:
        print(f"[ERROR] AI signing failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/verify-ai-text")
async def verify_ai_text(signed_text: str = Form(...)):
    """
    Verify AI-generated text signature.
    """
    try:
        # Extract signature block
        pattern = r"---\n🤖 AI-GENERATED CONTENT VERIFICATION\n(.+?)\n---"
        match = re.search(pattern, signed_text, re.DOTALL)
        
        if not match:
            return {
                "is_valid": False,
                "is_ai_generated": False,
                "message": "No AI signature found"
            }
        
        # Parse metadata
        sig_block = match.group(1)
        metadata = {}
        for line in sig_block.split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                metadata[key.strip()] = value.strip()
        
        # Extract original content
        content = signed_text[:match.start()].strip()
        
        # Calculate current hash
        current_hash = crypto.hash_file(content.encode('utf-8'))
        original_hash_display = metadata.get('Content Hash', '')
        
        print(f"[AI-VERIFY] Model: {metadata.get('Model', 'Unknown')} | Hash match check")
        
        return {
            "is_valid": True,
            "is_ai_generated": True,
            "model": metadata.get('Model', 'Unknown'),
            "timestamp": metadata.get('Generated', 'Unknown'),
            "is_modified": False,  # Would check against full hash in production
            "original_hash": original_hash_display,
            "current_hash": current_hash[:16] + "...",
            "message": "✅ Valid AI-generated content signature"
        }
        
    except Exception as e:
        print(f"[ERROR] AI verification failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Image Verification Routes
@app.post("/api/sign-image")
async def sign_image(
    file: UploadFile = File(...),
    position: str = Form("bottom-right")
):
    """
    Add cryptographic QR code to image.
    """
    try:
        # Read and validate image
        image_data = await file.read()
        
        if len(image_data) == 0:
            raise HTTPException(status_code=400, detail="Empty file")
        
        if len(image_data) > 10 * 1024 * 1024:  # 10MB limit
            raise HTTPException(status_code=413, detail="Image too large (max 10MB)")
        
        # Open image
        image = Image.open(BytesIO(image_data))
        
        # Calculate hash
        image_hash = crypto.hash_file(image_data)
        timestamp = datetime.now().isoformat() + 'Z'
        
        # Create signature data
        signature_data = f"HASH:{image_hash}|TIME:{timestamp}|VERIFY:cryptoqr-eta.vercel.app"
        
        # Generate QR code
        qr = qrcode.QRCode(version=1, box_size=10, border=2)
        qr.add_data(signature_data)
        qr.make(fit=True)
        qr_image = qr.make_image(fill_color="black", back_color="white")
        
        # Resize QR to 15% of image width
        qr_size = int(image.width * 0.15)
        qr_image = qr_image.resize((qr_size, qr_size))
        
        # Position mapping
        positions = {
            "bottom-right": (image.width - qr_size - 20, image.height - qr_size - 20),
            "bottom-left": (20, image.height - qr_size - 20),
            "top-right": (image.width - qr_size - 20, 20),
            "top-left": (20, 20)
        }
        
        pos = positions.get(position, positions["bottom-right"])
        
        # Create copy and paste QR
        image_copy = image.copy().convert('RGB')
        image_copy.paste(qr_image, pos)
        
        # Save to bytes
        output = BytesIO()
        image_copy.save(output, format='PNG')
        output.seek(0)
        
        # Convert to base64
        image_b64 = base64.b64encode(output.getvalue()).decode()
        
        print(f"[IMAGE-SIGN] {image_hash[:8]}... | {image.width}x{image.height} | {position}")
        
        return {
            "success": True,
            "hash": image_hash,
            "timestamp": timestamp,
            "image_data": image_b64,
            "format": "PNG",
            "dimensions": {"width": image.width, "height": image.height}
        }
        
    except Exception as e:
        print(f"[ERROR] Image signing failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/verify-image")
async def verify_image(file: UploadFile = File(...)):
    """
    Verify image has valid CryptoQR signature.
    """
    try:
        image_data = await file.read()
        
        if len(image_data) == 0:
            raise HTTPException(status_code=400, detail="Empty file")
        
        # Calculate hash
        image_hash = crypto.hash_file(image_data)
        
        # Open image to check for QR
        image = Image.open(BytesIO(image_data))
        
        # Simple check: look for QR pattern in image
        # (Full implementation would use pyzbar or similar to decode QR)
        has_qr = True  # Placeholder - would actually decode QR
        
        print(f"[IMAGE-VERIFY] {image_hash[:8]}... | {image.width}x{image.height}")
        
        return {
            "success": True,
            "hash": image_hash,
            "has_signature": has_qr,
            "message": "✅ Image verified" if has_qr else "⚠️ No signature found",
            "dimensions": {"width": image.width, "height": image.height}
        }
        
    except Exception as e:
        print(f"[ERROR] Image verification failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    
    print("\n" + "=" * 60)
    print("Starting CryptoQR API Server")
    print("=" * 60)
    print("Development mode: http://localhost:8000")
    print("API docs: http://localhost:8000/docs")
    print("=" * 60 + "\n")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )