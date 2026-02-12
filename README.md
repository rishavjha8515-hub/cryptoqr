
# 🔐 CryptoQR

**Cryptographic proof-of-work verification for digital submissions**

> Making honest effort verifiable in an AI-saturated world

![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)
![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)
![Built at AlamedaHacks](https://img.shields.io/badge/Built%20at-AlamedaHacks%202026-purple)

---

## 🌐 Live Demo

- **Frontend:** https://cryptoqr-pi.vercel.app/
- **Backend API:** https://cryptoqr-api-awkm.onrender.com

> Note: Backend may take ~30 seconds to wake up on first request (free tier deployment).

---

## 🎯 Problem Statement

With the rapid rise of AI-generated content, judges and reviewers in science fairs, hackathons, and competitions face a growing challenge:

**How can authentic effort and original work be verified reliably?**

Traditional review systems rely heavily on trust, manual inspection, or plagiarism checks, which are increasingly insufficient in an AI-assisted environment.

---

## 💡 Solution Overview

CryptoQR provides a **cryptographic verification layer** for digital submissions.

Each submitted file is bound to a **tamper-evident QR code** that proves:

- What file was submitted
- When it was submitted
- That the file has not been modified
- That it is valid only for a specific competition or context

Verification is cryptographic, not opinion-based.

---

## 🔐 Core Cryptographic Design

Each QR code encodes:

- **SHA-256 content hash** — guarantees file integrity
- **Ed25519 digital signature** — guarantees authenticity
- **ISO 8601 timestamp** — proves submission time
- **Competition identifier** — prevents reuse across events

Any modification to the file invalidates verification.

---

## ⚙️ How It Works

### Submission Flow

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

## 🚀 Key Features

### Cryptographic Integrity
- Ed25519 digital signatures
- SHA-256 hashing
- Tamper detection at bit-level precision
- Replay and reuse prevention

### Reviewer & Judge Utility
- Fast verification (milliseconds)
- Clear pass/fail output
- Context-bound submissions
- Audit-friendly metadata

### System Properties
- Zero-trust verification
- Offline-verifiable QR codes
- Serverless deployment
- No user accounts required

---

## 🧪 Design Philosophy

- Cryptography over trust
- Verification over claims
- Transparency over black-box scoring
- Advisory signals, not absolute judgments

CryptoQR is designed to support human review, not replace it.

---

## 🏆 Judges & Evaluation Context

CryptoQR was built and deployed during **AlamedaHacks 2026**, a global hackathon evaluated by industry professionals and engineers.

The project was recognized for:
- Practical application of cryptography
- Clear threat model and assumptions
- Real-world relevance to competitions and academic review systems

CryptoQR placed **Top 4 overall** at AlamedaHacks 2026.

---

## 📌 Project Status

- **Version:** 1.0.0-alpha
- **Stage:** Production-ready MVP
- **Development:** Active
- **License:** MIT

---

## 🔮 Planned Extensions

- AI-assisted content detection (advisory signals only)
- Deepfake and media integrity checks
- Cross-competition reuse detection
- Reviewer analytics dashboard

---

## 👨‍💻 Author

**Rishav Anand Kumar Jha**

Student researcher working on:
- Cryptographic verification systems
- Information integrity
- Quantum information & decoherence

Achievements:
- Top 4 — AlamedaHacks 2026
- IRIS National Science Fair Finalist (Physics & Astronomy)
- Published research on quantum decoherence visualization

---

## 📄 License

This project is licensed under the MIT License.

---

**CryptoQR** — Cryptographic proof for the age of AI