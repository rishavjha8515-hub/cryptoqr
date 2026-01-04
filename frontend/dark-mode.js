// Dark Mode Toggle System for CryptoQR
// Add this to all HTML pages

// CSS Variables for Dark Mode (add to <style> section)
const darkModeStyles = `
:root {
    --bg-gradient-start: #667eea;
    --bg-gradient-end: #764ba2;
    --card-bg: #ffffff;
    --text-primary: #1a202c;
    --text-secondary: #718096;
    --border-color: #e2e8f0;
    --input-bg: #ffffff;
    --input-border: #e2e8f0;
}

[data-theme="dark"] {
    --bg-gradient-start: #1a202c;
    --bg-gradient-end: #2d3748;
    --card-bg: #2d3748;
    --text-primary: #f7fafc;
    --text-secondary: #cbd5e0;
    --border-color: #4a5568;
    --input-bg: #1a202c;
    --input-border: #4a5568;
}

body {
    background: linear-gradient(135deg, var(--bg-gradient-start) 0%, var(--bg-gradient-end) 100%);
    transition: background 0.3s ease;
}

.container {
    background: var(--card-bg);
    transition: background 0.3s ease, box-shadow 0.3s ease;
}

[data-theme="dark"] .container {
    box-shadow: 0 24px 60px rgba(0, 0, 0, 0.5);
}

h1, h2, h3, label, .text-primary {
    color: var(--text-primary);
}

.subtitle, .text-secondary {
    color: var(--text-secondary);
}

input, textarea {
    background: var(--input-bg);
    border-color: var(--input-border);
    color: var(--text-primary);
}

.theme-toggle {
    position: fixed;
    top: 20px;
    right: 20px;
    width: 60px;
    height: 60px;
    background: var(--card-bg);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
    transition: all 0.3s ease;
    z-index: 1000;
    border: 2px solid var(--border-color);
}

.theme-toggle:hover {
    transform: scale(1.1) rotate(180deg);
}

.theme-toggle-icon {
    font-size: 28px;
}

[data-theme="dark"] .file-input-label {
    background: var(--input-bg);
    border-color: var(--border-color);
}

[data-theme="dark"] .file-input-label:hover {
    background: #374151;
}

[data-theme="dark"] .stat-card,
[data-theme="dark"] .competitions-section,
[data-theme="dark"] .chart-container {
    background: var(--card-bg);
    box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
}

[data-theme="dark"] .competition-item {
    background: #1a202c;
    border-color: #4a5568;
}

[data-theme="dark"] .competition-item:hover {
    background: #374151;
    border-color: #667eea;
}

[data-theme="dark"] .result {
    background: var(--card-bg);
}

[data-theme="dark"] .info-item,
[data-theme="dark"] .check-item {
    background: #1a202c;
}
`;

// Theme Toggle Component
class ThemeToggle {
    constructor() {
        this.theme = localStorage.getItem('cryptoqr-theme') || 'light';
        this.init();
    }

    init() {
        // Inject dark mode styles
        this.injectStyles();
        
        // Apply saved theme
        this.applyTheme(this.theme);
        
        // Create toggle button
        this.createToggleButton();
    }

    injectStyles() {
        const styleEl = document.createElement('style');
        styleEl.textContent = darkModeStyles;
        document.head.appendChild(styleEl);
    }

    createToggleButton() {
        const toggle = document.createElement('div');
        toggle.className = 'theme-toggle';
        toggle.innerHTML = `<span class="theme-toggle-icon">${this.theme === 'dark' ? '☀️' : '🌙'}</span>`;
        toggle.onclick = () => this.toggleTheme();
        
        document.body.appendChild(toggle);
        this.toggleButton = toggle;
    }

    toggleTheme() {
        this.theme = this.theme === 'light' ? 'dark' : 'light';
        this.applyTheme(this.theme);
    }

    applyTheme(theme) {
        document.documentElement.setAttribute('data-theme', theme);
        localStorage.setItem('cryptoqr-theme', theme);
        
        if (this.toggleButton) {
            const icon = this.toggleButton.querySelector('.theme-toggle-icon');
            icon.textContent = theme === 'dark' ? '☀️' : '🌙';
        }
    }
}

// Initialize on page load
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        new ThemeToggle();
    });
} else {
    new ThemeToggle();
}

// Export for use in modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = ThemeToggle;
}