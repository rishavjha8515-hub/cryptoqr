// PDF Export for CryptoQR Verification Reports
// Uses jsPDF library (CDN: https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js)

class CryptoQRPDFExporter {
    constructor() {
        this.loadJsPDF();
    }

    loadJsPDF() {
        if (typeof window.jspdf === 'undefined') {
            const script = document.createElement('script');
            script.src = 'https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js';
            script.onload = () => {
                console.log('jsPDF loaded successfully');
            };
            document.head.appendChild(script);
        }
    }

    async exportVerificationReport(verificationData, qrImageBase64) {
        // Wait for jsPDF to load
        await this.waitForJsPDF();

        const { jsPDF } = window.jspdf;
        const doc = new jsPDF();

        // Colors
        const primaryColor = [102, 126, 234]; // #667eea
        const successColor = [72, 187, 120];  // #48bb78
        const errorColor = [245, 101, 101];   // #f56565
        const textColor = [45, 55, 72];       // #2d3748
        const grayColor = [113, 128, 150];    // #718096

        const pageWidth = doc.internal.pageSize.getWidth();
        const pageHeight = doc.internal.pageSize.getHeight();

        // Header
        doc.setFillColor(...primaryColor);
        doc.rect(0, 0, pageWidth, 40, 'F');

        doc.setTextColor(255, 255, 255);
        doc.setFontSize(24);
        doc.setFont(undefined, 'bold');
        doc.text('🔐 CryptoQR', 20, 20);

        doc.setFontSize(12);
        doc.setFont(undefined, 'normal');
        doc.text('Cryptographic Verification Report', 20, 30);

        // Status Badge
        const isValid = verificationData.valid;
        const statusY = 55;

        if (isValid) {
            doc.setFillColor(...successColor);
            doc.roundedRect(20, statusY, 60, 12, 3, 3, 'F');
            doc.setTextColor(255, 255, 255);
            doc.setFontSize(10);
            doc.setFont(undefined, 'bold');
            doc.text('✓ VALID', 30, statusY + 8);
        } else {
            doc.setFillColor(...errorColor);
            doc.roundedRect(20, statusY, 60, 12, 3, 3, 'F');
            doc.setTextColor(255, 255, 255);
            doc.setFontSize(10);
            doc.setFont(undefined, 'bold');
            doc.text('✗ INVALID', 28, statusY + 8);
        }

        // Verification Details
        let yPos = 80;

        doc.setTextColor(...textColor);
        doc.setFontSize(14);
        doc.setFont(undefined, 'bold');
        doc.text('Verification Details', 20, yPos);

        yPos += 10;
        doc.setFontSize(10);
        doc.setFont(undefined, 'normal');

        const details = [
            ['Submission ID', verificationData.submission_id],
            ['Timestamp', new Date(verificationData.timestamp).toLocaleString()],
            ['Competition', verificationData.competition_id],
            ['Verified At', new Date(verificationData.verified_at).toLocaleString()]
        ];

        details.forEach(([label, value]) => {
            doc.setTextColor(...grayColor);
            doc.text(label + ':', 20, yPos);
            doc.setTextColor(...textColor);
            doc.setFont(undefined, 'bold');
            doc.text(String(value), 70, yPos);
            doc.setFont(undefined, 'normal');
            yPos += 7;
        });

        // Security Checks
        yPos += 10;
        doc.setFontSize(14);
        doc.setFont(undefined, 'bold');
        doc.setTextColor(...textColor);
        doc.text('Security Checks', 20, yPos);

        yPos += 10;
        doc.setFontSize(10);
        doc.setFont(undefined, 'normal');

        if (verificationData.checks) {
            Object.entries(verificationData.checks).forEach(([key, passed]) => {
                const checkLabel = this.formatCheckLabel(key);
                
                doc.setTextColor(...textColor);
                doc.text(checkLabel, 25, yPos);

                if (passed) {
                    doc.setTextColor(...successColor);
                    doc.text('✓ Pass', 120, yPos);
                } else {
                    doc.setTextColor(...errorColor);
                    doc.text('✗ Fail', 120, yPos);
                }

                yPos += 7;
            });
        }

        // Failure Reason
        if (!isValid && verificationData.reason) {
            yPos += 10;
            doc.setFillColor(255, 245, 245);
            doc.rect(20, yPos - 5, pageWidth - 40, 20, 'F');
            
            doc.setTextColor(...errorColor);
            doc.setFontSize(10);
            doc.setFont(undefined, 'bold');
            doc.text('Failure Reason:', 25, yPos);
            
            doc.setFont(undefined, 'normal');
            const reasonLines = doc.splitTextToSize(verificationData.reason, pageWidth - 50);
            doc.text(reasonLines, 25, yPos + 7);
            
            yPos += 25;
        }

        // QR Code Image
        if (qrImageBase64) {
            yPos += 10;
            doc.setFontSize(14);
            doc.setFont(undefined, 'bold');
            doc.setTextColor(...textColor);
            doc.text('Cryptographic QR Code', 20, yPos);

            yPos += 10;
            try {
                const qrSize = 60;
                const qrX = (pageWidth - qrSize) / 2;
                doc.addImage(`data:image/png;base64,${qrImageBase64}`, 'PNG', qrX, yPos, qrSize, qrSize);
                yPos += qrSize + 10;
            } catch (error) {
                console.error('Error adding QR image to PDF:', error);
            }
        }

        // Footer
        const footerY = pageHeight - 20;
        doc.setDrawColor(...grayColor);
        doc.line(20, footerY - 5, pageWidth - 20, footerY - 5);

        doc.setFontSize(8);
        doc.setTextColor(...grayColor);
        doc.setFont(undefined, 'normal');
        doc.text('Generated by CryptoQR v1.0.0', 20, footerY);
        doc.text(`Report Date: ${new Date().toLocaleString()}`, 20, footerY + 5);
        doc.text('Cryptographically verified using Ed25519 digital signatures', pageWidth - 20, footerY, { align: 'right' });

        // Watermark
        doc.setFontSize(60);
        doc.setTextColor(240, 240, 240);
        doc.text(isValid ? 'VALID' : 'INVALID', pageWidth / 2, pageHeight / 2, {
            align: 'center',
            angle: 45
        });

        // Save PDF
        const filename = `cryptoqr-verification-${verificationData.submission_id}.pdf`;
        doc.save(filename);
    }

    async exportSubmissionCertificate(submissionData, qrImageBase64) {
        await this.waitForJsPDF();

        const { jsPDF } = window.jspdf;
        const doc = new jsPDF();

        const primaryColor = [102, 126, 234];
        const pageWidth = doc.internal.pageSize.getWidth();
        const pageHeight = doc.internal.pageSize.getHeight();

        // Decorative border
        doc.setDrawColor(...primaryColor);
        doc.setLineWidth(2);
        doc.rect(10, 10, pageWidth - 20, pageHeight - 20);

        // Header
        doc.setFontSize(32);
        doc.setTextColor(...primaryColor);
        doc.setFont(undefined, 'bold');
        doc.text('Certificate of Submission', pageWidth / 2, 40, { align: 'center' });

        // Subtitle
        doc.setFontSize(14);
        doc.setTextColor(100, 100, 100);
        doc.setFont(undefined, 'normal');
        doc.text('Cryptographically Verified', pageWidth / 2, 50, { align: 'center' });

        // QR Code (large, centered)
        if (qrImageBase64) {
            const qrSize = 80;
            const qrX = (pageWidth - qrSize) / 2;
            doc.addImage(`data:image/png;base64,${qrImageBase64}`, 'PNG', qrX, 70, qrSize, qrSize);
        }

        // Submission Details
        let yPos = 170;
        doc.setFontSize(12);
        doc.setTextColor(0, 0, 0);

        const details = [
            ['Submission ID', submissionData.submission_id],
            ['Timestamp', new Date(submissionData.timestamp).toLocaleString()],
            ['Content Hash', submissionData.content_hash.substring(0, 16) + '...']
        ];

        details.forEach(([label, value]) => {
            doc.setFont(undefined, 'bold');
            doc.text(label + ':', 40, yPos);
            doc.setFont(undefined, 'normal');
            doc.text(String(value), 100, yPos);
            yPos += 10;
        });

        // Footer
        doc.setFontSize(10);
        doc.setTextColor(150, 150, 150);
        doc.text('This document is cryptographically secured', pageWidth / 2, pageHeight - 30, { align: 'center' });
        doc.text('Verified using Ed25519 digital signatures', pageWidth / 2, pageHeight - 20, { align: 'center' });

        const filename = `cryptoqr-certificate-${submissionData.submission_id}.pdf`;
        doc.save(filename);
    }

    formatCheckLabel(key) {
        const labels = {
            'signature_valid': 'Cryptographic Signature',
            'content_match': 'Content Hash Match',
            'before_deadline': 'Submitted Before Deadline',
            'timestamp_valid': 'Timestamp Validity'
        };
        return labels[key] || key;
    }

    async waitForJsPDF() {
        let attempts = 0;
        while (typeof window.jspdf === 'undefined' && attempts < 50) {
            await new Promise(resolve => setTimeout(resolve, 100));
            attempts++;
        }
        if (typeof window.jspdf === 'undefined') {
            throw new Error('jsPDF library failed to load');
        }
    }
}

// Global instance
const pdfExporter = new CryptoQRPDFExporter();

// Export functions for easy use
window.exportVerificationPDF = (verificationData, qrImageBase64) => {
    return pdfExporter.exportVerificationReport(verificationData, qrImageBase64);
};

window.exportSubmissionCertificate = (submissionData, qrImageBase64) => {
    return pdfExporter.exportSubmissionCertificate(submissionData, qrImageBase64);
};