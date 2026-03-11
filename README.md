# CryptoQR

**Cryptographic document verification — because honest work deserves proof.**

---

## Where this came from

I was looking at a QR code on a perfume bottle and started wondering — how many unique QR codes can actually exist? I took it to my faculty as a permutations and combinations problem. That conversation led me down a rabbit hole: binary states, exponential possibility spaces, and eventually to Ramanujan's work and how it connects to modern encryption.

That's when it clicked. A QR code isn't just a link. It can be a proof.

In a world where AI can generate a polished research paper or a convincing deepfake in minutes, how does a student prove their work is actually theirs? How does a judge know a submission wasn't backdated? I wanted to build something that makes honest effort verifiable — not through trust, but through math.

CryptoQR is that tool. It's not finished. But the core idea works.

---

## What it does

You upload a document. CryptoQR generates a QR code that cryptographically binds that file to a specific timestamp and competition. Any judge can scan it to verify:

- Is this the original file? (SHA-256 hash — any single bit change breaks it)
- Was it actually signed by the submitter? (Ed25519 digital signature)
- When was it submitted? (ISO 8601 timestamp)
- Was it submitted for this specific competition? (competition binding prevents reuse)

The math behind it: SHA-256 produces a 256-bit fingerprint — that's 2^256 possible values, roughly the number of atoms in the observable universe. Finding two files with the same hash by brute force is computationally impossible. Ed25519 gives ~128 bits of security (2^128 operations to break) with smaller, faster keys than RSA.

---

## What's working

The full cryptographic pipeline works end-to-end:

- Document upload → SHA-256 hash → Ed25519 signature → QR code generation
- Judge verification: upload file + QR → instant valid/invalid result
- Deployed: frontend on Vercel, backend API on Render

Try it: [cryptoqr-pi.vercel.app](https://cryptoqr-pi.vercel.app)

*Note: Backend is on Render free tier — first request may take ~30 seconds to wake up.*

---

## What's not finished

**Email notifications:** Integrated Gmail first (didn't send), then switched to SendGrid. Emails send but land in spam due to shared IP reputation on free tier — this requires a dedicated IP or custom domain DNS configuration to fully resolve. I understand why it's broken; I just don't have the infrastructure budget to fix it yet.

**AI detection layer:** The original goal was to add deepfake and AI-generated content detection on top of the cryptographic verification. That system is not built yet. CryptoQR currently proves *when* and *by whom* — not *how* content was created. That's the next problem.

---

## Stack

| Component | Technology |
|-----------|------------|
| Backend | Python 3.11 + FastAPI |
| Cryptography | Ed25519 (signatures) + SHA-256 (hashing) |
| QR Generation | qrcode + Pillow |
| Frontend | HTML5 / CSS3 / JavaScript |
| Deployment | Render + Vercel |

---

## Built at

AlamedaHacks 2026 — a 10-day global hackathon with 938 participants and 34 industry judges from Google, Meta, Amazon, and Anthropic. Won Judge's Pick.

---

## About

Built by **Rishav Anand Kumar Jha** — 16-year-old independent researcher from Mumbai, working on quantum decoherence visualization and apparently also cryptographic verification systems that started from a perfume bottle.

- Research: [zenodo.org/records/17781173](https://zenodo.org/records/17781173)
- Email: rishavjha8515@gmail.com

---

*MIT License — see LICENSE file.*
