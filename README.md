# 🔐 CryptoQR

**Cryptographic proof-of-work verification for digital submissions**

> Making honest effort verifiable in an AI-saturated world

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Built at AlamedaHacks](https://img.shields.io/badge/Built%20at-AlamedaHacks%202026-purple)](https://alamedahacks.com)

---

## 🌐 Live Demo

**🚀 Try it now:**

- **Frontend:** https://cryptoqr-pi.vercel.app/
- **Backend API:** https://cryptoqr-api-awkm.onrender.com

*Note: Backend may take 30 seconds to wake up on first request (free tier)*

---

## 📋 Table of Contents

- [The Problem](#-the-problem)
- [The Solution](#-the-solution)
- [Quick Start](#-quick-start)
- [Technical Architecture](#-technical-architecture)
- [Security Features](#-security-features)
- [Use Cases](#-use-cases)
- [Technology Stack](#-technology-stack)
- [Project Status](#-project-status)
- [Built By](#-built-by)
- [Contributing](#-contributing)
- [Contact](#-contact)
- [License](#-license)
- [Acknowledgments](#-acknowledgments)

---

## 🎯 The Problem

In 2025, AI can generate polished projects in minutes. Science fairs, hackathons, and research competitions face an authenticity crisis:

**How do you prove when work was actually created?**

Traditional verification relies on trust. CryptoQR relies on cryptography.

---

## 💡 The Solution

CryptoQR generates **unforgeable, tamper-evident QR codes** that cryptographically bind documents to specific timestamps.

When students submit work, they receive a QR code containing:

- 🔒 **SHA-256 content hash** (proves document integrity)
- ✍️ **Ed25519 signature** (proves authenticity)
- ⏰ **ISO 8601 timestamp** (proves when)
- 🎯 **Competition binding** (prevents reuse)

Judges scan the QR code to instantly verify: Is this the original work? Was it submitted on time? Has it been modified?

---

## ⚡ Key Features

### 🔐 Cryptographic Security
- **Ed25519 Digital Signatures** - Military-grade authentication
- **SHA-256 Hashing** - Tamper detection at bit-level precision
- **Zero-Trust Architecture** - Verification works independently
- **Replay Attack Prevention** - QR codes can't be reused

### 🎨 User Experience
- **One-Click Submission** - Upload file, get QR code instantly
- **Email Delivery** - Automatic certificate with QR code attached
- **Beautiful Certificates** - Print-ready submission proof
- **Mobile-Friendly** - Works on any device

### 🚀 Performance
- **Serverless Deployment** - Infinite scalability
- **$0 Operating Cost** - No server maintenance
- **Instant Verification** - Results in milliseconds
- **Offline Capable** - QR codes work without internet

### 🛡️ Enterprise Features
- **Duplicate Detection** - Same file can't be submitted twice
- **Competition Isolation** - Prevents submission reuse
- **Audit Trail** - Complete verification history
- **JSON Export** - Full cryptographic metadata

---

## 🚀 Quick Start

### For Students (Submitters)

1. Visit the submission portal
2. Upload your project file
3. Enter competition details
4. Download your cryptographic QR code
5. Attach it to your submission

### For Judges (Verifiers)

1. Visit the verification portal
2. Upload the submission file + QR code
3. Get instant verification: ✅ Valid or ❌ Invalid

---

## 🔬 How It Works

### Submission Process

```
Student File → SHA-256 Hash → Ed25519 Signature → QR Code
     ↓              ↓               ↓                 ↓
   Upload      Fingerprint     Sign + Timestamp   Visual Proof
```

### Verification Process

```
Judge Upload → Extract Hash → Verify Signature → Compare Timestamp
      ↓             ↓              ↓                    ↓
  Student File  Recalculate   Check Authenticity   Validate Deadline
```

### Cryptographic Flow

1. **Hash Generation**: File content → SHA-256 → 64-character hex string
2. **Signature Creation**: Hash + Timestamp + Competition ID → Ed25519 private key → Digital signature
3. **QR Encoding**: All metadata → JSON → QR code image
4. **Verification**: Uploaded file → Recalculate hash → Verify signature with public key → Success/Failure

---

## 🏗️ Technical Architecture

**Backend:** Python 3.11 + FastAPI  
**Cryptography:** Ed25519 (digital signatures) + SHA-256 (hashing)  
**Frontend:** Modern vanilla JavaScript + CSS3  
**Deployment:** Serverless architecture (Render + Vercel)  
**Cost:** $0 to run at scale

---

## 🔒 Security Features

- ✅ **Tamper Detection**: Any file modification breaks verification
- ✅ **Timestamp Integrity**: Backdating is cryptographically impossible
- ✅ **Replay Prevention**: QR codes can't be reused across competitions
- ✅ **Duplicate Detection**: Same file can't be submitted twice
- ✅ **Zero Trust Architecture**: Verification works independently

---

## 📈 Use Cases

- 🏆 Hackathons & coding competitions
- 🔬 Science fairs & research submissions
- 🎓 Scholarship applications
- 📚 Academic portfolios
- 💼 Freelance work verification
- 📝 Content authenticity proof

---

## 🛠️ Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Backend API | FastAPI | REST endpoints |
| Cryptography | `cryptography` lib | Ed25519 + SHA-256 |
| QR Generation | `qrcode` + `Pillow` | Image creation |
| Frontend | HTML5/CSS3/JS | User interface |
| Deployment | Render + Vercel | Production hosting |

---

## 👨‍💻 Built By

**Rishav Anand Kumar Jha** | 16-year-old computational physics researcher

- 📄 Published: [Quantum Decoherence Visualization](https://zenodo.org/records/17781173) (400+ views)
- 🏆 IRIS National Fair 2025 Finalist (Physics & Astronomy)
- 🔬 Research: Information theory, cryptographic verification systems

This project applies research-grade cryptography to solve real-world verification challenges in student competitions.

---

## 🤝 Contributing

This project is currently in active development for AlamedaHacks 2026.

Contributions, issues, and feature requests are welcome after initial release.

## 📧 Contact

- **GitHub:** [@rishavjha8515-hub](https://github.com/rishavjha8515-hub)
- **Email:** rishavjha8515@gmail.com
- **Project:** [github.com/rishavjha8515-hub/cryptoqr](https://github.com/rishavjha8515-hub/cryptoqr)

---

## 🙏 Acknowledgments

Built during **AlamedaHacks 2026** - a global virtual hackathon for high school and college students.

Special thanks to:
- 🎉 **AlamedaHacks organizers** for hosting this incredible event
- 👥 **Mentors and judges** for guidance and feedback
- 🌟 **Open-source community** for cryptographic libraries
- 💡 **Students worldwide** facing authenticity challenges in the AI era

---

## 📊 Project Status

**Version:** 1.0.0-alpha  
**Development:** Active (AlamedaHacks 2026, Jan 1-11)  
**Stage:** Production-ready MVP  
**License:** MIT

---

<div align="center">

**CryptoQR** • *Cryptographic proof for the age of AI*

[🚀 Try Demo](https://cryptoqr-pi.vercel.app/) • [📖 Read Docs](#-quick-start) • [🐛 Report Issue](https://github.com/rishavjha8515-hub/cryptoqr/issues) • [⭐ Star Project](https://github.com/rishavjha8515-hub/cryptoqr)

Made with ❤️ and cryptography by Rishav Jha

</div>