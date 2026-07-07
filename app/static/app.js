// DOM Elements
const dropZone = document.getElementById('drop-zone');
const fileInput = document.getElementById('file-input');
const jobDescInput = document.getElementById('job-desc');
const analyzeBtn = document.getElementById('analyze-btn');
const fileListContainer = document.getElementById('file-list-container');
const fileList = document.getElementById('file-list');
const fileCountSpan = document.getElementById('file-count');

const emptyState = document.getElementById('empty-state');
const loadingState = document.getElementById('loading-state');
const resultsDashboard = document.getElementById('results-dashboard');
const rankingList = document.getElementById('ranking-list');

const statProcessed = document.getElementById('stat-processed');
const statTopScore = document.getElementById('stat-top-score');
const statAvgScore = document.getElementById('stat-avg-score');
const resultsCountBadge = document.getElementById('results-count-badge');

// Application State
let selectedFiles = [];

// Initialize Lucide icons
document.addEventListener('DOMContentLoaded', () => {
    lucide.createIcons();
    validateForm();
});

// Textarea verification
jobDescInput.addEventListener('input', validateForm);

// Drag and drop events
dropZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropZone.classList.add('dragover');
});

dropZone.addEventListener('dragleave', () => {
    dropZone.classList.remove('dragover');
});

dropZone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropZone.classList.remove('dragover');
    
    if (e.dataTransfer.files) {
        addFiles(e.dataTransfer.files);
    }
});

// Drop zone click triggers file dialog
dropZone.addEventListener('click', (e) => {
    // Avoid double trigger if clicking label/browse-link which defaults to input click
    if (e.target !== fileInput) {
        fileInput.click();
    }
});

fileInput.addEventListener('change', () => {
    if (fileInput.files) {
        addFiles(fileInput.files);
    }
});

// File Management Functions
function addFiles(filesList) {
    for (let file of filesList) {
        // Only accept PDFs
        if (file.type === 'application/pdf' || file.name.endsWith('.pdf')) {
            // Check for duplicates
            if (!selectedFiles.some(f => f.name === file.name && f.size === file.size)) {
                selectedFiles.push(file);
            }
        }
    }
    renderFileList();
    validateForm();
}

function removeFile(index) {
    selectedFiles.splice(index, 1);
    renderFileList();
    validateForm();
}

function renderFileList() {
    if (selectedFiles.length === 0) {
        fileListContainer.style.display = 'none';
        fileList.innerHTML = '';
        return;
    }

    fileListContainer.style.display = 'block';
    fileCountSpan.textContent = selectedFiles.length;
    fileList.innerHTML = selectedFiles.map((file, idx) => `
        <li class="file-item">
            <div class="file-info">
                <i data-lucide="file" class="file-icon"></i>
                <span class="file-name" title="${file.name}">${file.name}</span>
            </div>
            <button class="btn-remove-file" onclick="removeFile(${idx})">
                <i data-lucide="x" style="width: 14px; height: 14px;"></i>
            </button>
        </li>
    `).join('');
    
    lucide.createIcons();
}

function validateForm() {
    const hasJobDesc = jobDescInput.value.trim().length > 10;
    const hasFiles = selectedFiles.length > 0;
    analyzeBtn.disabled = !(hasJobDesc && hasFiles);
}

// API Submission Function
analyzeBtn.addEventListener('click', async () => {
    if (selectedFiles.length === 0 || jobDescInput.value.trim().length < 10) return;

    // Transition state UI
    emptyState.style.display = 'none';
    resultsDashboard.style.display = 'none';
    loadingState.style.display = 'flex';
    analyzeBtn.disabled = true;

    const formData = new FormData();
    formData.append('job_description', jobDescInput.value.trim());
    
    selectedFiles.forEach(file => {
        formData.append('resumes', file);
    });

    try {
        const response = await fetch('/analyze', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            const err = await response.json();
            throw new Error(err.detail || 'Failed to analyze resumes');
        }

        const data = await response.json();
        renderResults(data);
    } catch (error) {
        console.error(error);
        alert(`Error: ${error.message}`);
        // Reset to empty state on failure
        loadingState.style.display = 'none';
        emptyState.style.display = 'flex';
    } finally {
        analyzeBtn.disabled = false;
        validateForm();
    }
});

// Render Results Dashboard
function renderResults(results) {
    loadingState.style.display = 'none';
    resultsDashboard.style.display = 'flex';

    const count = results.length;
    statProcessed.textContent = count;
    resultsCountBadge.textContent = `${count} Candidate${count !== 1 ? 's' : ''}`;

    if (count === 0) {
        statTopScore.textContent = '0%';
        statAvgScore.textContent = '0%';
        rankingList.innerHTML = `<div class="glass-card" style="padding: 2rem; text-align: center; color: var(--text-secondary);">No valid resume profiles parsed.</div>`;
        return;
    }

    const scores = results.map(r => r.score);
    const topScore = Math.max(...scores);
    const avgScore = Math.round(scores.reduce((a, b) => a + b, 0) / count);

    statTopScore.textContent = `${topScore}%`;
    statAvgScore.textContent = `${avgScore}%`;

    // Radial Progress Parameters (r = 30)
    // circumference = 2 * pi * r = 188.49
    const r = 30;
    const c = 2 * Math.PI * r;

    rankingList.innerHTML = results.map((candidate, idx) => {
        const strokeDashoffset = c - (candidate.score / 100) * c;
        const rank = idx + 1;
        
        let rankClass = '';
        if (rank === 1) rankClass = 'rank-top-1';
        else if (rank === 2) rankClass = 'rank-top-2';

        // Split lists into tags
        const matchTags = candidate.matching_skills.map(s => `<span class="tag tag-match">${s}</span>`).join('');
        const otherTags = candidate.extracted_skills
            .filter(s => !candidate.matching_skills.includes(s))
            .map(s => `<span class="tag tag-other">${s}</span>`).join('');

        return `
            <div class="glass-card candidate-card">
                <div class="rank-badge ${rankClass}">#${rank}</div>
                <div class="candidate-summary">
                    <div class="candidate-details">
                        <h3 class="candidate-name">${candidate.filename}</h3>
                        <div class="candidate-meta">
                            <span class="meta-item">
                                <i data-lucide="file-check" class="meta-icon"></i>
                                <span>Parsed PDF</span>
                            </span>
                            <span class="meta-item">
                                <i data-lucide="award" class="meta-icon"></i>
                                <span>${candidate.matching_skills_count} matching skills</span>
                            </span>
                        </div>
                    </div>
                    <div class="score-container">
                        <div class="score-radial">
                            <svg>
                                <circle class="bg" cx="34" cy="34" r="${r}"></circle>
                                <circle class="progress" cx="34" cy="34" r="${r}" 
                                    style="stroke-dasharray: ${c}; stroke-dashoffset: ${strokeDashoffset};">
                                </circle>
                            </svg>
                            <span class="score-text">${candidate.score}%</span>
                        </div>
                    </div>
                </div>
                
                <div class="candidate-skills-section">
                    ${candidate.matching_skills.length > 0 ? `
                        <div class="skills-group">
                            <span class="skills-label">Matching Core Skills</span>
                            <div class="tags-wrapper">
                                ${matchTags}
                            </div>
                        </div>
                    ` : ''}
                    
                    ${candidate.extracted_skills.length > candidate.matching_skills.length ? `
                        <div class="skills-group">
                            <span class="skills-label">Other Extracted Skills</span>
                            <div class="tags-wrapper">
                                ${otherTags}
                            </div>
                        </div>
                    ` : ''}
                    
                    ${candidate.extracted_skills.length === 0 ? `
                        <div class="skills-group">
                            <span class="skills-label">Extracted Skills</span>
                            <span style="font-size: 0.8rem; color: var(--text-muted);">No key skills identified in resume.</span>
                        </div>
                    ` : ''}
                </div>
            </div>
        `;
    }).join('');

    lucide.createIcons();
}
