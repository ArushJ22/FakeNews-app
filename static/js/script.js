console.log("JS loaded!");

// UI Elements
const analyzeBtn = document.querySelector("button");
const textarea = document.querySelector("textarea");
const resultSection = document.querySelector(".result-section");
const resultStats = document.querySelector(".result-stats");
const chartContainer = document.querySelector(".chart-container");

// Show loading state
function setLoading(isLoading) {
    analyzeBtn.disabled = isLoading;
    analyzeBtn.innerHTML = isLoading ? 
        '<i class="fas fa-spinner fa-spin"></i> Analyzing...' : 
        '<i class="fas fa-search"></i> Analyze Content';
}

// Enhanced error display
function showError(message) {
    // Remove existing error messages
    const existingError = document.querySelector('.error-message');
    if (existingError) existingError.remove();
    
    // Create new error message
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.innerHTML = `
        <i class="fas fa-exclamation-triangle"></i>
        <span>${message}</span>
        <button onclick="this.parentElement.remove()" class="error-close">
            <i class="fas fa-times"></i>
        </button>
    `;
    
    // Insert before the form
    const card = document.querySelector('.card');
    card.insertBefore(errorDiv, card.firstChild);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (errorDiv.parentElement) errorDiv.remove();
    }, 5000);
}

// Generate unique article ID
function generateId() {
    return 'ART-' + Date.now().toString(36).toUpperCase();
}

// Validate input content
function validateContent(content) {
    if (!content || content.trim().length < 10) {
        throw new Error('Please enter at least 10 characters of article content.');
    }
    if (content.length > 5000) {
        throw new Error('Article content is too long. Please limit to 5000 characters.');
    }
    return true;
}

// Determine status based on probability with uncertainty handling
function determineStatus(probability) {
    if (probability >= 0.65) return { 
        label: 'fake', 
        class: 'fake', 
        icon: 'times-circle',
        confidence: 'High'
    };
    if (probability <= 0.35) return { 
        label: 'real', 
        class: 'real', 
        icon: 'check-circle',
        confidence: 'High'
    };
    return { 
        label: 'uncertain', 
        class: 'warning', 
        icon: 'question-circle',
        confidence: 'Low'
    };
}

// Enhanced pie chart animation with easing
function animatePieChart(targetPercentage) {
    let current = parseInt(getComputedStyle(document.documentElement).getPropertyValue('--fake-percentage')) || 0;
    let startTime = null;
    const duration = 1200; // 1.2 seconds for smoother animation
    
    function animate(timestamp) {
        if (!startTime) startTime = timestamp;
        const elapsed = timestamp - startTime;
        const progress = Math.min(elapsed / duration, 1);
        
        // Easing function for smoother animation
        const easeOutCubic = 1 - Math.pow(1 - progress, 3);
        const value = Math.round(current + (targetPercentage - current) * easeOutCubic);
        
        document.documentElement.style.setProperty('--fake-percentage', `${value}%`);
        
        // Update center label during animation
        const chartLabel = document.querySelector('.chart-label');
        const realPercentage = 100 - value;
        chartLabel.innerHTML = `
            <div class="percentage-main">${value}%</div>
            <div class="percentage-label">Fake</div>
            <div class="percentage-sub">${realPercentage}% Real</div>
        `;
        
        if (progress < 1) {
            requestAnimationFrame(animate);
        }
    }
    
    requestAnimationFrame(animate);
}

// Enhanced result display
function updateResult(result) {
    // Handle both probability and binary results
    const probability = result.probability || result.confidence || (result.label === 'fake' ? 0.7 : 0.3);
    const fakePercentage = Math.round(probability * 100);
    const realPercentage = 100 - fakePercentage;
    
    const status = determineStatus(probability);
    const articleId = result.id || generateId();
    const timestamp = new Date().toLocaleTimeString();
    
    // Calculate confidence percentage based on predicted class
    let confidencePercentage;
    if (status.label === 'fake') {
        confidencePercentage = fakePercentage; // Show fake percentage for fake news
    } else if (status.label === 'real') {
        confidencePercentage = realPercentage; // Show real percentage for real news
    } else {
        // For uncertain, show the higher percentage
        confidencePercentage = Math.max(fakePercentage, realPercentage);
    }
    
    // Animate the pie chart
    animatePieChart(fakePercentage);
    
    // Update result stats with enhanced information
    document.querySelector('.result-stats').innerHTML = `
        <div class="result-item">
            <span>Status:</span>
            <span class="result-value ${status.class}">
                <i class="fas fa-${status.icon}"></i> ${status.label.toUpperCase()}
            </span>
        </div>
        <div class="result-item">
            <span>Confidence:</span>
            <span class="result-value ${status.class}">
                ${confidencePercentage} (${status.confidence})
            </span>
        </div>
        <div class="result-item">
            <span>Article ID:</span>
            <span class="result-value">
                <i class="fas fa-hashtag"></i> ${articleId}
            </span>
        </div>
        <div class="result-item">
            <span>Analysis Time:</span>
            <span class="result-value">
                <i class="fas fa-clock"></i> ${timestamp}
            </span>
        </div>
        ${probability >= 0.35 && probability <= 0.65 ? `
        <div class="result-item uncertainty-warning">
            <span>⚠️ Note:</span>
            <span class="result-value warning">
                Result is uncertain. Manual verification recommended.
            </span>
        </div>
        ` : ''}
    `;

    // Show result section with fade-in effect
    resultSection.style.display = 'block';
    resultSection.style.opacity = '0';
    setTimeout(() => {
        resultSection.style.opacity = '1';
    }, 100);
}

// Enhanced main analysis function
analyzeBtn.addEventListener("click", async () => {
    const content = textarea.value.trim();
    
    try {
        validateContent(content);
        setLoading(true);
        
        // Clear previous errors
        const existingError = document.querySelector('.error-message');
        if (existingError) existingError.remove();
        
        const response = await fetch("/articles/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ 
                content: content,
                timestamp: new Date().toISOString()
            }),
        });

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.message || `Server error: ${response.status}`);
        }

        const result = await response.json();
        updateResult(result);
        
    } catch (error) {
        console.error("Analysis error:", error);
        showError(error.message);
    } finally {
        setLoading(false);
    }
});

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    // Hide result section initially
    resultSection.style.display = 'none';
    
    // Add character counter to textarea
    const charCounter = document.createElement('div');
    charCounter.className = 'char-counter';
    charCounter.innerHTML = '0 / 5000 characters';
    textarea.parentNode.appendChild(charCounter);
    
    textarea.addEventListener('input', () => {
        const length = textarea.value.length;
        charCounter.innerHTML = `${length} / 5000 characters`;
        charCounter.style.color = length > 4500 ? '#e63946' : '#6c757d';
    });
});
