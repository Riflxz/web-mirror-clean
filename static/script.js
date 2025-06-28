// Web Mirror Application JavaScript
document.addEventListener('DOMContentLoaded', function() {
    
    // Theme toggle functionality
    const themeToggle = document.getElementById('themeToggle');
    const themeIcon = document.getElementById('themeIcon');
    const themeText = document.getElementById('themeText');
    const html = document.documentElement;
    
    // Load saved theme or default to light
    const savedTheme = localStorage.getItem('theme') || 'light';
    setTheme(savedTheme);
    
    if (themeToggle) {
        themeToggle.addEventListener('click', function() {
            const currentTheme = html.getAttribute('data-bs-theme');
            const newTheme = currentTheme === 'light' ? 'dark' : 'light';
            setTheme(newTheme);
            localStorage.setItem('theme', newTheme);
        });
    }
    
    function setTheme(theme) {
        html.setAttribute('data-bs-theme', theme);
        if (themeIcon && themeText) {
            if (theme === 'dark') {
                themeIcon.className = 'fas fa-sun';
                themeText.textContent = 'Light';
            } else {
                themeIcon.className = 'fas fa-moon';
                themeText.textContent = 'Dark';
            }
        }
    }
    
    // Form submission with loading state
    const mirrorForm = document.getElementById('mirrorForm');
    const mirrorBtn = document.getElementById('mirrorBtn');
    
    if (mirrorForm && mirrorBtn) {
        mirrorForm.addEventListener('submit', function(e) {
            // Add loading state
            mirrorBtn.classList.add('loading');
            mirrorBtn.disabled = true;
            
            // Validate URL
            const urlInput = document.getElementById('url');
            const url = urlInput.value.trim();
            
            if (!url) {
                e.preventDefault();
                mirrorBtn.classList.remove('loading');
                mirrorBtn.disabled = false;
                urlInput.focus();
                return;
            }
            
            // Add protocol if missing
            if (!url.startsWith('http://') && !url.startsWith('https://')) {
                urlInput.value = 'https://' + url;
            }
        });
    }
    
    // Reading options functionality
    const fontSize = document.getElementById('fontSize');
    const lineHeight = document.getElementById('lineHeight');
    const mirroredContent = document.getElementById('mirroredContent');
    
    if (fontSize && mirroredContent) {
        fontSize.addEventListener('change', function() {
            mirroredContent.style.fontSize = this.value + 'px';
            localStorage.setItem('fontSize', this.value);
        });
        
        // Load saved font size
        const savedFontSize = localStorage.getItem('fontSize');
        if (savedFontSize) {
            fontSize.value = savedFontSize;
            mirroredContent.style.fontSize = savedFontSize + 'px';
        }
    }
    
    if (lineHeight && mirroredContent) {
        lineHeight.addEventListener('change', function() {
            mirroredContent.style.lineHeight = this.value;
            localStorage.setItem('lineHeight', this.value);
        });
        
        // Load saved line height
        const savedLineHeight = localStorage.getItem('lineHeight');
        if (savedLineHeight) {
            lineHeight.value = savedLineHeight;
            mirroredContent.style.lineHeight = savedLineHeight;
        }
    }
    
    // Focus mode functionality
    const focusMode = document.getElementById('focusMode');
    const focusOverlay = document.getElementById('focusOverlay');
    const exitFocusMode = document.getElementById('exitFocusMode');
    const focusContent = document.getElementById('focusContent');
    
    if (focusMode && focusOverlay) {
        focusMode.addEventListener('click', function() {
            if (mirroredContent) {
                focusContent.innerHTML = mirroredContent.innerHTML;
                focusOverlay.classList.remove('d-none');
                document.body.style.overflow = 'hidden';
            }
        });
    }
    
    if (exitFocusMode && focusOverlay) {
        exitFocusMode.addEventListener('click', function() {
            focusOverlay.classList.add('d-none');
            document.body.style.overflow = 'auto';
        });
        
        // Exit focus mode with Escape key
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape' && !focusOverlay.classList.contains('d-none')) {
                exitFocusMode.click();
            }
        });
    }
    
    // Print functionality
    const printBtn = document.getElementById('printBtn');
    if (printBtn) {
        printBtn.addEventListener('click', function() {
            window.print();
        });
    }
    
    // Copy link functionality
    const copyLinkBtn = document.getElementById('copyLinkBtn');
    if (copyLinkBtn) {
        copyLinkBtn.addEventListener('click', function() {
            navigator.clipboard.writeText(window.location.href).then(function() {
                // Show success feedback
                const originalText = copyLinkBtn.innerHTML;
                copyLinkBtn.innerHTML = '<i class="fas fa-check me-1"></i>Copied!';
                copyLinkBtn.classList.add('btn-success');
                copyLinkBtn.classList.remove('btn-outline-secondary');
                
                setTimeout(function() {
                    copyLinkBtn.innerHTML = originalText;
                    copyLinkBtn.classList.remove('btn-success');
                    copyLinkBtn.classList.add('btn-outline-secondary');
                }, 2000);
            }).catch(function() {
                // Fallback for older browsers
                const textArea = document.createElement('textarea');
                textArea.value = window.location.href;
                document.body.appendChild(textArea);
                textArea.focus();
                textArea.select();
                document.execCommand('copy');
                document.body.removeChild(textArea);
                
                // Show success feedback
                const originalText = copyLinkBtn.innerHTML;
                copyLinkBtn.innerHTML = '<i class="fas fa-check me-1"></i>Copied!';
                copyLinkBtn.classList.add('btn-success');
                copyLinkBtn.classList.remove('btn-outline-secondary');
                
                setTimeout(function() {
                    copyLinkBtn.innerHTML = originalText;
                    copyLinkBtn.classList.remove('btn-success');
                    copyLinkBtn.classList.add('btn-outline-secondary');
                }, 2000);
            });
        });
    }
    
    // Auto-dismiss alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            if (alert.parentNode) {
                alert.classList.add('fade');
                setTimeout(function() {
                    if (alert.parentNode) {
                        alert.remove();
                    }
                }, 300);
            }
        }, 5000);
    });
    
    // Smooth scrolling for internal links
    document.addEventListener('click', function(e) {
        if (e.target.tagName === 'A' && e.target.href.startsWith('#')) {
            e.preventDefault();
            const target = document.querySelector(e.target.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        }
    });
    
    // Add fade-in animation to content
    const contentArea = document.getElementById('contentArea');
    if (contentArea) {
        contentArea.classList.add('fade-in');
    }
    
    // Handle external links in mirrored content
    const externalLinks = document.querySelectorAll('#mirroredContent a[href^="http"]');
    externalLinks.forEach(function(link) {
        link.setAttribute('target', '_blank');
        link.setAttribute('rel', 'noopener noreferrer');
        
        // Add external link icon
        if (!link.querySelector('.fa-external-link-alt')) {
            const icon = document.createElement('i');
            icon.className = 'fas fa-external-link-alt ms-1';
            icon.style.fontSize = '0.8em';
            link.appendChild(icon);
        }
    });
    
    // Lazy loading for images in mirrored content
    const images = document.querySelectorAll('#mirroredContent img');
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver(function(entries, observer) {
            entries.forEach(function(entry) {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    if (img.dataset.src) {
                        img.src = img.dataset.src;
                        img.removeAttribute('data-src');
                    }
                    img.classList.remove('lazy');
                    imageObserver.unobserve(img);
                }
            });
        });
        
        images.forEach(function(img) {
            imageObserver.observe(img);
        });
    }
    
    // Add keyboard shortcuts
    document.addEventListener('keydown', function(e) {
        // Ctrl/Cmd + K to focus on URL input
        if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
            e.preventDefault();
            const urlInput = document.getElementById('url');
            if (urlInput) {
                urlInput.focus();
                urlInput.select();
            }
        }
        
        // Ctrl/Cmd + P to print
        if ((e.ctrlKey || e.metaKey) && e.key === 'p') {
            e.preventDefault();
            if (printBtn) {
                printBtn.click();
            }
        }
        
        // F to toggle focus mode
        if (e.key === 'f' && !e.ctrlKey && !e.metaKey && !e.altKey) {
            const activeElement = document.activeElement;
            if (activeElement.tagName !== 'INPUT' && activeElement.tagName !== 'TEXTAREA') {
                e.preventDefault();
                if (focusMode && !focusOverlay.classList.contains('d-none') === false) {
                    focusMode.click();
                }
            }
        }
    });
});
