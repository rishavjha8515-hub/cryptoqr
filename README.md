## 🌐 Live Demo

**🚀 Try it now:**
- **Frontend:** https://your-vercel-url.vercel.app
- **Backend API:** https://cryptoqr-api-awkm.onrender.com

*Note: Backend may take 30 seconds to wake up on first request (free tier)*
# 🔐 CryptoQR

**Cryptographic proof-of-work verification for digital submissions**

> Making honest effort verifiable in an AI-saturated world

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Built at AlamedaHacks](https://img.shields.io/badge/Built%20at-AlamedaHacks%202026-purple)](https://alamedahacks.com)

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

## 📊 Project Status

**Version:** 1.0.0-alpha  
**Development:** Active (AlamedaHacks 2026, Jan 1-11)  
**Stage:** Production-ready MVP  
**License:** MIT  

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

---

## 📧 Contact

- **GitHub:** [@rishavjha8515-hub](https://github.com/rishavjha8515-hub)
- **Email:** rishavjha8515@gmail.com
- **Project:** [github.com/rishavjha8515-hub/cryptoqr](https://github.com/rishavjha8515-hub/cryptoqr)

---

## 📜 License

MIT License - see [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

Built during AlamedaHacks 2026 - a global virtual hackathon for high school and college students.

Special thanks to the organizers and mentors who made this possible.

---

<div align="center">

**CryptoQR** • *Cryptographic proof for the age of AI*

[Demo]  • [Report Issue](https://github.com/rishavjha8515-hub/cryptoqr/issues)

</div>
