# 🔐 CryptoQR

**Cryptographic proof-of-work verification for digital submissions**

> Making honest effort verifiable in an AI-saturated world

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)

---

## 🎯 The Problem

In 2025, AI can generate polished projects in minutes. Science fairs, hackathons, and research competitions face an authenticity crisis: **How do you prove when work was actually created?**

Traditional verification relies on trust. CryptoQR relies on cryptography.

---

## 💡 The Solution

CryptoQR generates unforgeable, tamper-evident QR codes that cryptographically bind documents to specific timestamps. When students submit work, they receive a QR code containing:

- **SHA-256 content hash** (proves document integrity)
- **Ed25519 signature** (proves authenticity)
- **ISO 8601 timestamp** (proves when)
- **Competition binding** (prevents reuse)

Judges scan the QR code to instantly verify: Is this the original work? Was it submitted on time? Has it been modified?

---

## 🚀 Quick Start

### For Students (Submitters)

1. Visit [link]
2. Upload your project file
3. Enter competition details
4. Download your cryptographic QR code
5. Attach it to your submission

### For Judges (Verifiers)

1. Visit [link]/verify
2. Upload the submission file + QR code
3. Get instant verification: ✅ Valid or ❌ Invalid

---

## 🏗️ Architecture

**Backend:** Python 3.11 + FastAPI  
**Cryptography:** Ed25519 (signatures) + SHA-256 (hashing)  
**Frontend:** Vanilla JavaScript + Modern CSS  
**Deployment:** Serverless (Render + Vercel)  
**Cost:** $0 to run

---

## 🔒 Security Features

- ✅ **Tamper Detection**: Any file modification breaks verification
- ✅ **Timestamp Integrity**: Backdating is cryptographically impossible
- ✅ **Replay Prevention**: QR codes can't be reused across competitions
- ✅ **Duplicate Prevention**: Same file can't be submitted twice
- ✅ **Zero Trust**: Verification works offline without server

---

## 📈 Use Cases

- 🏆 Hackathons & coding competitions
- 🔬 Science fairs & research submissions
- 🎓 Scholarship applications
- 📚 Academic portfolios
- 💼 Freelance work verification

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| Backend API | FastAPI |
| Cryptography | `cryptography` (Python) |
| QR Generation | `qrcode` + `Pillow` |
| Frontend | HTML5 + CSS3 + JavaScript (ES6+) |
| Deployment | Render (backend) + Vercel (frontend) |

---

## 📊 Status

**Current Version:** 1.0.0-alpha  
**Development Stage:** Active (AlamedaHacks 2026)  
**License:** MIT  

---

## 🤝 Contributing

Built by Rishav Anand Kumar Jha, 16-year-old computational physics researcher.

- 📄 Published: [Quantum Decoherence Visualization](https://zenodo.org/records/17781173)
- 🏆 IRIS National Fair 2025 Finalist

---

## 📧 Contact

- Email: [your email]
- GitHub: [@rishavjha8515-hub](https://github.com/rishavjha8515-hub)
- Project:

---

## 📜 License

MIT License - see [LICENSE](LICENSE) for details

---

**CryptoQR** • *Cryptographic proof for the age of AI*