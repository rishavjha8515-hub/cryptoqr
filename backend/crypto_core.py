"""
CryptoQR - Cryptographic Core Module
Built: January 1, 2026 for AlamedaHacks
Author: Rishav Anand Kumar Jha

Implements Ed25519 digital signatures and SHA-256 hashing
for tamper-evident document verification.
"""

import hashlib
import secrets
import json
import base64
from datetime import datetime, timezone
from typing import Dict, Optional, Tuple
from dataclasses import dataclass, asdict

from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import serialization
from cryptography.exceptions import InvalidSignature


@dataclass
class SubmissionPayload:
    """Structured submission data"""
    content_hash: str
    timestamp: str
    competition_id: str
    deadline: str
    submission_id: str
    nonce: str
    email: Optional[str] = None


@dataclass
class VerificationResult:
    """Structured verification result"""
    valid: bool
    submission_id: str
    timestamp: str
    competition_id: str
    checks: Dict[str, bool]
    reason: Optional[str] = None


class CryptoQRCore:
    """
    Core cryptographic operations for CryptoQR system.
    
    Handles:
    - Ed25519 key generation and management
    - SHA-256 file hashing
    - Digital signature creation and verification
    - Payload serialization and deserialization
    """
    
    def __init__(self, private_key_pem: Optional[str] = None):
        """
        Initialize crypto core with key pair.
        
        Args:
            private_key_pem: Optional PEM-encoded private key.
                           If None, generates new key pair.
        """
        if private_key_pem:
            self._load_private_key(private_key_pem)
        else:
            self._generate_key_pair()
    
    def _generate_key_pair(self) -> None:
        """Generate new Ed25519 key pair"""
        self.private_key = ed25519.Ed25519PrivateKey.generate()
        self.public_key = self.private_key.public_key()
    
    def _load_private_key(self, pem: str) -> None:
        """Load existing private key from PEM format"""
        try:
            self.private_key = serialization.load_pem_private_key(
                pem.encode('utf-8'),
                password=None
            )
            self.public_key = self.private_key.public_key()
        except Exception as e:
            raise ValueError(f"Failed to load private key: {e}")
    
    def export_public_key(self) -> str:
        """Export public key in PEM format"""
        return self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ).decode('utf-8')
    
    def export_private_key(self) -> str:
        """Export private key in PEM format (use with caution)"""
        return self.private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ).decode('utf-8')
    
    @staticmethod
    def hash_file(file_data: bytes) -> str:
        """
        Compute SHA-256 hash of file content.
        
        Args:
            file_data: Raw file bytes
            
        Returns:
            Hex-encoded SHA-256 hash
        """
        return hashlib.sha256(file_data).hexdigest()
    
    @staticmethod
    def _serialize_payload(payload: SubmissionPayload) -> bytes:
        """Canonically serialize payload for signing"""
        payload_dict = asdict(payload)
        # Remove None values
        payload_dict = {k: v for k, v in payload_dict.items() if v is not None}
        # Sort keys for deterministic serialization
        return json.dumps(payload_dict, sort_keys=True).encode('utf-8')
    
    def create_submission(
        self,
        file_data: bytes,
        competition_id: str,
        deadline: str,
        email: Optional[str] = None
    ) -> Dict:
        """
        Create cryptographically signed submission.
        
        Args:
            file_data: Raw file bytes to verify
            competition_id: Unique competition identifier
            deadline: ISO 8601 deadline timestamp
            email: Optional submitter email
            
        Returns:
            Dict containing submission_id, payload, signature, and metadata
        """
        # Generate unique identifiers
        submission_id = self._generate_submission_id()
        nonce = self._generate_nonce()
        
        # Compute content hash
        content_hash = self.hash_file(file_data)
        
        # Create timestamp
        timestamp = datetime.now(timezone.utc).isoformat()
        
        # Build payload
        payload = SubmissionPayload(
            content_hash=content_hash,
            timestamp=timestamp,
            competition_id=competition_id,
            deadline=deadline,
            submission_id=submission_id,
            nonce=nonce,
            email=email
        )
        
        # Sign payload
        signature = self._sign_payload(payload)
        
        return {
            'submission_id': submission_id,
            'timestamp': timestamp,
            'content_hash': content_hash,
            'payload': asdict(payload),
            'signature': base64.b64encode(signature).decode('utf-8'),
            'version': '1.0.0'
        }
    
    def _sign_payload(self, payload: SubmissionPayload) -> bytes:
        """Generate Ed25519 signature for payload"""
        serialized = self._serialize_payload(payload)
        return self.private_key.sign(serialized)
    
    def verify_submission(
        self,
        qr_data: Dict,
        file_data: bytes,
        public_key_pem: Optional[str] = None
    ) -> VerificationResult:
        """
        Verify submission against QR code data.
        
        Args:
            qr_data: Decoded QR code data
            file_data: Actual file bytes to verify
            public_key_pem: Optional public key (uses instance key if None)
            
        Returns:
            VerificationResult with validation status and details
        """
        try:
            # Extract components
            payload_dict = qr_data.get('payload', {})
            signature_b64 = qr_data.get('signature', '')
            
            # Reconstruct payload
            payload = SubmissionPayload(**payload_dict)
            signature = base64.b64decode(signature_b64)
            
            # Select public key
            pub_key = self._get_public_key(public_key_pem)
            
            # Perform checks
            checks = {
                'signature_valid': self._verify_signature(payload, signature, pub_key),
                'content_match': self._verify_content(payload, file_data),
                'before_deadline': self._verify_deadline(payload),
                'timestamp_valid': self._verify_timestamp(payload)
            }
            
            all_valid = all(checks.values())
            
            result = VerificationResult(
                valid=all_valid,
                submission_id=payload.submission_id,
                timestamp=payload.timestamp,
                competition_id=payload.competition_id,
                checks=checks,
                reason=self._generate_failure_reason(checks) if not all_valid else None
            )
            
            return result
            
        except Exception as e:
            return VerificationResult(
                valid=False,
                submission_id='unknown',
                timestamp='unknown',
                competition_id='unknown',
                checks={},
                reason=f"Verification error: {str(e)}"
            )
    
    def _get_public_key(self, pem: Optional[str]) -> ed25519.Ed25519PublicKey:
        """Get public key from PEM or use instance key"""
        if pem:
            return serialization.load_pem_public_key(pem.encode('utf-8'))
        return self.public_key
    
    def _verify_signature(
        self,
        payload: SubmissionPayload,
        signature: bytes,
        public_key: ed25519.Ed25519PublicKey
    ) -> bool:
        """Verify Ed25519 signature"""
        try:
            serialized = self._serialize_payload(payload)
            public_key.verify(signature, serialized)
            return True
        except InvalidSignature:
            return False
        except Exception:
            return False
    
    def _verify_content(self, payload: SubmissionPayload, file_data: bytes) -> bool:
        """Verify file content matches hash in payload"""
        computed_hash = self.hash_file(file_data)
        return computed_hash == payload.content_hash
    
    def _verify_deadline(self, payload: SubmissionPayload) -> bool:
        """Verify submission was before deadline"""
        try:
            submission_time = datetime.fromisoformat(
                payload.timestamp.replace('Z', '+00:00')
            )
            deadline_time = datetime.fromisoformat(
                payload.deadline.replace('Z', '+00:00')
            )
            return submission_time <= deadline_time
        except Exception:
            return False
    
    def _verify_timestamp(self, payload: SubmissionPayload) -> bool:
        """Verify timestamp is valid and reasonable"""
        try:
            ts = datetime.fromisoformat(payload.timestamp.replace('Z', '+00:00'))
            now = datetime.now(timezone.utc)
            # Timestamp shouldn't be in the future (with 5 min tolerance)
            return ts <= now
        except Exception:
            return False
    
    @staticmethod
    def _generate_failure_reason(checks: Dict[str, bool]) -> str:
        """Generate human-readable failure reason"""
        failures = [k for k, v in checks.items() if not v]
        if not failures:
            return None
        
        messages = {
            'signature_valid': 'Invalid cryptographic signature',
            'content_match': 'File content does not match QR code',
            'before_deadline': 'Submission was after deadline',
            'timestamp_valid': 'Invalid or suspicious timestamp'
        }
        
        return '; '.join(messages.get(f, f) for f in failures)
    
    @staticmethod
    def _generate_submission_id() -> str:
        """Generate unique submission identifier"""
        return base64.urlsafe_b64encode(secrets.token_bytes(16)).decode('utf-8').rstrip('=')
    
    @staticmethod
    def _generate_nonce() -> str:
        """Generate cryptographic nonce"""
        return base64.urlsafe_b64encode(secrets.token_bytes(16)).decode('utf-8').rstrip('=')


# Convenience functions for simple usage
def generate_qr_submission(
    file_data: bytes,
    competition_id: str,
    deadline: str,
    email: Optional[str] = None
) -> Dict:
    """
    Convenience function to generate submission without managing keys.
    
    Note: Generates ephemeral keys. For production, maintain persistent keys.
    """
    crypto = CryptoQRCore()
    return crypto.create_submission(file_data, competition_id, deadline, email)


def verify_qr_submission(
    qr_data: Dict,
    file_data: bytes,
    public_key_pem: str
) -> VerificationResult:
    """
    Convenience function to verify submission.
    """
    crypto = CryptoQRCore()
    return crypto.verify_submission(qr_data, file_data, public_key_pem)


if __name__ == '__main__':
    # Self-test
    print("CryptoQR Core - Self Test")
    print("=" * 50)
    
    # Initialize
    crypto = CryptoQRCore()
    print("✓ Generated key pair")
    
    # Create test submission
    test_file = b"This is a test submission for AlamedaHacks 2026"
    submission = crypto.create_submission(
        file_data=test_file,
        competition_id="alamedahacks-2026",
        deadline="2026-01-11T09:00:00Z",
        email="test@example.com"
    )
    print(f"✓ Created submission: {submission['submission_id']}")
    
    # Verify submission
    qr_data = {
        'payload': submission['payload'],
        'signature': submission['signature'],
        'version': submission['version']
    }
    
    result = crypto.verify_submission(qr_data, test_file)
    print(f"✓ Verification: {'VALID' if result.valid else 'INVALID'}")
    print(f"  Checks: {result.checks}")
    
    # Test tampering
    tampered_file = b"This is DIFFERENT content"
    result2 = crypto.verify_submission(qr_data, tampered_file)
    print(f"✓ Tamper test: {'VALID' if result2.valid else 'INVALID'} (should be INVALID)")
    print(f"  Reason: {result2.reason}")
    
    print("\n" + "=" * 50)
    print("Self-test complete!")