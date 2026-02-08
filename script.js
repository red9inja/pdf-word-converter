// AWS API Gateway endpoint - Auto-updated by GitHub Actions
const API_ENDPOINT = 'https://YOUR-API-ID.execute-api.us-east-1.amazonaws.com/prod';

let selectedFiles = [];
let currentTool = null;

// Tool configurations
const toolConfig = {
    'pdf-to-word': { title: 'PDF to Word', accept: '.pdf', endpoint: '/convert/pdf-to-word' },
    'word-to-pdf': { title: 'Word to PDF', accept: '.doc,.docx', endpoint: '/convert/word-to-pdf' },
    'pdf-to-excel': { title: 'PDF to Excel', accept: '.pdf', endpoint: '/convert/pdf-to-excel' },
    'excel-to-pdf': { title: 'Excel to PDF', accept: '.xls,.xlsx', endpoint: '/convert/excel-to-pdf' },
    'pdf-to-ppt': { title: 'PDF to PowerPoint', accept: '.pdf', endpoint: '/convert/pdf-to-ppt' },
    'ppt-to-pdf': { title: 'PowerPoint to PDF', accept: '.ppt,.pptx', endpoint: '/convert/ppt-to-pdf' },
    'pdf-to-jpg': { title: 'PDF to JPG', accept: '.pdf', endpoint: '/convert/pdf-to-jpg' },
    'jpg-to-pdf': { title: 'JPG to PDF', accept: '.jpg,.jpeg,.png', endpoint: '/convert/jpg-to-pdf' },
    'merge-pdf': { title: 'Merge PDF', accept: '.pdf', multiple: true, endpoint: '/organize/merge' },
    'split-pdf': { title: 'Split PDF', accept: '.pdf', endpoint: '/organize/split', options: 'split' },
    'rotate-pdf': { title: 'Rotate PDF', accept: '.pdf', endpoint: '/organize/rotate', options: 'rotate' },
    'delete-pages': { title: 'Delete Pages', accept: '.pdf', endpoint: '/organize/delete-pages', options: 'pages' },
    'extract-pages': { title: 'Extract Pages', accept: '.pdf', endpoint: '/organize/extract-pages', options: 'pages' },
    'organize-pdf': { title: 'Organize PDF', accept: '.pdf', endpoint: '/organize/reorder', options: 'reorder' },
    'compress-pdf': { title: 'Compress PDF', accept: '.pdf', endpoint: '/optimize/compress', options: 'compress' },
    'repair-pdf': { title: 'Repair PDF', accept: '.pdf', endpoint: '/optimize/repair' },
    'optimize-pdf': { title: 'Optimize PDF', accept: '.pdf', endpoint: '/optimize/optimize' },
    'protect-pdf': { title: 'Protect PDF', accept: '.pdf', endpoint: '/security/protect', options: 'protect' },
    'unlock-pdf': { title: 'Unlock PDF', accept: '.pdf', endpoint: '/security/unlock', options: 'unlock' },
    'sign-pdf': { title: 'Sign PDF', accept: '.pdf', endpoint: '/security/sign', options: 'sign' },
    'watermark-pdf': { title: 'Watermark PDF', accept: '.pdf', endpoint: '/edit/watermark', options: 'watermark' },
    'edit-pdf': { title: 'Edit PDF', accept: '.pdf', endpoint: '/edit/edit' },
    'add-page-numbers': { title: 'Add Page Numbers', accept: '.pdf', endpoint: '/edit/page-numbers', options: 'pageNumbers' },
    'ocr-pdf': { title: 'OCR PDF', accept: '.pdf', endpoint: '/edit/ocr', options: 'ocr' },
    'pdf-reader': { title: 'PDF Reader', accept: '.pdf', endpoint: '/reader' },
    'resume-builder': { title: 'Resume Builder (ATS Optimized)', accept: '', endpoint: '/resume/build', options: 'resumeBuilder' },
    'ats-checker': { title: 'ATS Score Checker', accept: '.pdf,.doc,.docx', endpoint: '/resume/ats-check' },
    'resume-templates': { title: 'Resume Templates', accept: '', endpoint: '/resume/templates', options: 'templates' },
    'cover-letter': { title: 'Cover Letter Generator', accept: '', endpoint: '/resume/cover-letter', options: 'coverLetter' }
};

// Tool option templates
const optionTemplates = {
    split: `
        <div class="option-group">
            <label>Split Mode:</label>
            <select id="splitMode">
                <option value="pages">By Page Range</option>
                <option value="size">By File Size</option>
                <option value="each">Extract Each Page</option>
            </select>
        </div>
        <div class="option-group" id="pageRangeGroup">
            <label>Page Range (e.g., 1-3, 5, 7-10):</label>
            <input type="text" id="pageRange" placeholder="1-3, 5, 7-10">
        </div>
    `,
    rotate: `
        <div class="option-group">
            <label>Rotation Angle:</label>
            <select id="rotateAngle">
                <option value="90">90° Clockwise</option>
                <option value="180">180°</option>
                <option value="270">270° (90° Counter-clockwise)</option>
            </select>
        </div>
    `,
    pages: `
        <div class="option-group">
            <label>Page Numbers (e.g., 1,3,5-7):</label>
            <input type="text" id="pageNumbers" placeholder="1,3,5-7">
        </div>
    `,
    compress: `
        <div class="option-group">
            <label>Compression Level:</label>
            <select id="compressionLevel">
                <option value="low">Low (Best Quality)</option>
                <option value="medium">Medium (Recommended)</option>
                <option value="high">High (Smallest Size)</option>
            </select>
        </div>
    `,
    protect: `
        <div class="option-group">
            <label>Password:</label>
            <input type="password" id="pdfPassword" placeholder="Enter password">
        </div>
        <div class="option-group">
            <label>Permissions:</label>
            <label><input type="checkbox" id="allowPrint"> Allow Printing</label>
            <label><input type="checkbox" id="allowCopy"> Allow Copy</label>
            <label><input type="checkbox" id="allowModify"> Allow Modify</label>
        </div>
    `,
    unlock: `
        <div class="option-group">
            <label>PDF Password:</label>
            <input type="password" id="unlockPassword" placeholder="Enter PDF password">
        </div>
    `,
    watermark: `
        <div class="option-group">
            <label>Watermark Text:</label>
            <input type="text" id="watermarkText" placeholder="Enter watermark text">
        </div>
        <div class="option-group">
            <label>Position:</label>
            <select id="watermarkPosition">
                <option value="center">Center</option>
                <option value="top">Top</option>
                <option value="bottom">Bottom</option>
                <option value="diagonal">Diagonal</option>
            </select>
        </div>
    `,
    pageNumbers: `
        <div class="option-group">
            <label>Position:</label>
            <select id="pageNumPosition">
                <option value="bottom-center">Bottom Center</option>
                <option value="bottom-right">Bottom Right</option>
                <option value="bottom-left">Bottom Left</option>
                <option value="top-center">Top Center</option>
            </select>
        </div>
    `,
    ocr: `
        <div class="option-group">
            <label>Language:</label>
            <select id="ocrLanguage">
                <option value="eng">English</option>
                <option value="spa">Spanish</option>
                <option value="fra">French</option>
                <option value="deu">German</option>
                <option value="hin">Hindi</option>
            </select>
        </div>
    `,
    resumeBuilder: `
        <div class="resume-form">
            <h3>Personal Information</h3>
            <div class="option-group">
                <label>Full Name:</label>
                <input type="text" id="fullName" placeholder="John Doe">
            </div>
            <div class="option-group">
                <label>Email:</label>
                <input type="email" id="email" placeholder="john@example.com">
            </div>
            <div class="option-group">
                <label>Phone:</label>
                <input type="tel" id="phone" placeholder="+1 234 567 8900">
            </div>
            <div class="option-group">
                <label>LinkedIn:</label>
                <input type="url" id="linkedin" placeholder="linkedin.com/in/johndoe">
            </div>
            
            <h3>Professional Summary</h3>
            <div class="option-group">
                <label>Summary (ATS Optimized):</label>
                <textarea id="summary" rows="4" placeholder="Experienced professional with..."></textarea>
            </div>
            
            <h3>Work Experience</h3>
            <div class="option-group">
                <label>Job Title:</label>
                <input type="text" id="jobTitle" placeholder="Senior Developer">
            </div>
            <div class="option-group">
                <label>Company:</label>
                <input type="text" id="company" placeholder="Tech Corp">
            </div>
            <div class="option-group">
                <label>Duration:</label>
                <input type="text" id="duration" placeholder="Jan 2020 - Present">
            </div>
            <div class="option-group">
                <label>Responsibilities (one per line):</label>
                <textarea id="responsibilities" rows="5" placeholder="- Led team of 5 developers&#10;- Increased performance by 40%"></textarea>
            </div>
            
            <h3>Education</h3>
            <div class="option-group">
                <label>Degree:</label>
                <input type="text" id="degree" placeholder="Bachelor of Computer Science">
            </div>
            <div class="option-group">
                <label>University:</label>
                <input type="text" id="university" placeholder="State University">
            </div>
            <div class="option-group">
                <label>Year:</label>
                <input type="text" id="gradYear" placeholder="2019">
            </div>
            
            <h3>Skills (ATS Keywords)</h3>
            <div class="option-group">
                <label>Technical Skills (comma separated):</label>
                <input type="text" id="skills" placeholder="Python, JavaScript, AWS, Docker, React">
            </div>
            
            <h3>Template</h3>
            <div class="option-group">
                <label>Choose Template:</label>
                <select id="resumeTemplate">
                    <option value="modern">Modern (ATS Friendly)</option>
                    <option value="professional">Professional</option>
                    <option value="minimal">Minimal</option>
                    <option value="creative">Creative</option>
                </select>
            </div>
            
            <div class="ats-tips">
                <h4>ATS Optimization Tips:</h4>
                <ul>
                    <li>Use standard section headings</li>
                    <li>Include relevant keywords from job description</li>
                    <li>Use simple formatting (no tables, columns)</li>
                    <li>Save as PDF or DOCX</li>
                    <li>Use standard fonts (Arial, Calibri, Times New Roman)</li>
                </ul>
            </div>
        </div>
    `,
    templates: `
        <div class="template-gallery">
            <h3>Choose a Template</h3>
            <div class="template-grid">
                <div class="template-card" data-template="modern">
                    <div class="template-preview">Modern</div>
                    <p>ATS Friendly - Clean & Professional</p>
                </div>
                <div class="template-card" data-template="professional">
                    <div class="template-preview">Professional</div>
                    <p>Traditional - Corporate Style</p>
                </div>
                <div class="template-card" data-template="minimal">
                    <div class="template-preview">Minimal</div>
                    <p>Simple - Focus on Content</p>
                </div>
                <div class="template-card" data-template="creative">
                    <div class="template-preview">Creative</div>
                    <p>Unique - Stand Out Design</p>
                </div>
            </div>
        </div>
    `,
    coverLetter: `
        <div class="option-group">
            <label>Your Name:</label>
            <input type="text" id="clName" placeholder="John Doe">
        </div>
        <div class="option-group">
            <label>Company Name:</label>
            <input type="text" id="clCompany" placeholder="Tech Corp">
        </div>
        <div class="option-group">
            <label>Position:</label>
            <input type="text" id="clPosition" placeholder="Senior Developer">
        </div>
        <div class="option-group">
            <label>Hiring Manager Name (if known):</label>
            <input type="text" id="clManager" placeholder="Jane Smith">
        </div>
        <div class="option-group">
            <label>Your Key Skills (comma separated):</label>
            <input type="text" id="clSkills" placeholder="Python, Leadership, Problem Solving">
        </div>
        <div class="option-group">
            <label>Why this company?</label>
            <textarea id="clWhy" rows="3" placeholder="I'm excited about your company because..."></textarea>
        </div>
    `
};

// Tool button click handlers
document.querySelectorAll('.tool-btn').forEach(btn => {
    btn.addEventListener('click', function() {
        const tool = this.dataset.tool;
        selectTool(tool);
    });
});

function selectTool(tool) {
    currentTool = tool;
    const config = toolConfig[tool];
    
    // Update UI
    document.querySelectorAll('.tool-btn').forEach(b => b.classList.remove('active'));
    document.querySelector(`[data-tool="${tool}"]`).classList.add('active');
    
    document.getElementById('toolTitle').textContent = config.title;
    document.getElementById('fileInput').accept = config.accept;
    document.getElementById('fileInput').multiple = config.multiple || false;
    
    // Show/hide options
    const optionsDiv = document.getElementById('toolOptions');
    if (config.options && optionTemplates[config.options]) {
        optionsDiv.innerHTML = optionTemplates[config.options];
        optionsDiv.classList.add('active');
    } else {
        optionsDiv.innerHTML = '';
        optionsDiv.classList.remove('active');
    }
    
    // Reset
    selectedFiles = [];
    document.getElementById('fileName').textContent = '';
    document.getElementById('processBtn').disabled = true;
    document.getElementById('status').textContent = '';
    document.getElementById('downloadSection').style.display = 'none';
}

// File input handler
document.getElementById('fileInput').addEventListener('change', function(e) {
    selectedFiles = Array.from(e.target.files);
    if (selectedFiles.length > 0) {
        const fileNames = selectedFiles.map(f => f.name).join(', ');
        document.getElementById('fileName').textContent = `Selected: ${fileNames}`;
        document.getElementById('processBtn').disabled = false;
    }
});

// Process button handler
document.getElementById('processBtn').addEventListener('click', async function() {
    if (selectedFiles.length === 0 || !currentTool) return;

    const statusDiv = document.getElementById('status');
    const downloadSection = document.getElementById('downloadSection');
    const config = toolConfig[currentTool];
    
    statusDiv.className = 'status processing';
    statusDiv.textContent = 'Processing your files... This may take a minute.';
    downloadSection.style.display = 'none';
    this.disabled = true;

    try {
        const formData = new FormData();
        
        // Add files
        selectedFiles.forEach((file, index) => {
            formData.append(`file${index}`, file);
        });
        
        // Add tool-specific options
        if (config.options) {
            const options = getToolOptions(config.options);
            formData.append('options', JSON.stringify(options));
        }

        const response = await fetch(API_ENDPOINT + config.endpoint, {
            method: 'POST',
            body: formData
        });

        const result = await response.json();

        if (result.success) {
            const downloadLink = document.getElementById('downloadLink');
            downloadLink.href = result.download_url;
            downloadLink.download = result.filename || 'result.pdf';
            
            statusDiv.className = 'status success';
            statusDiv.textContent = 'Processing successful! Click below to download.';
            downloadSection.style.display = 'block';
        } else {
            throw new Error(result.error || 'Processing failed');
        }

    } catch (error) {
        statusDiv.className = 'status error';
        statusDiv.textContent = 'Processing failed. Please try again or use different files.';
        console.error('Error:', error);
    } finally {
        this.disabled = false;
    }
});

function getToolOptions(optionType) {
    const options = {};
    
    switch(optionType) {
        case 'split':
            options.mode = document.getElementById('splitMode')?.value;
            options.pageRange = document.getElementById('pageRange')?.value;
            break;
        case 'rotate':
            options.angle = document.getElementById('rotateAngle')?.value;
            break;
        case 'pages':
            options.pages = document.getElementById('pageNumbers')?.value;
            break;
        case 'compress':
            options.level = document.getElementById('compressionLevel')?.value;
            break;
        case 'protect':
            options.password = document.getElementById('pdfPassword')?.value;
            options.allowPrint = document.getElementById('allowPrint')?.checked;
            options.allowCopy = document.getElementById('allowCopy')?.checked;
            options.allowModify = document.getElementById('allowModify')?.checked;
            break;
        case 'unlock':
            options.password = document.getElementById('unlockPassword')?.value;
            break;
        case 'watermark':
            options.text = document.getElementById('watermarkText')?.value;
            options.position = document.getElementById('watermarkPosition')?.value;
            break;
        case 'pageNumbers':
            options.position = document.getElementById('pageNumPosition')?.value;
            break;
        case 'ocr':
            options.language = document.getElementById('ocrLanguage')?.value;
            break;
        case 'resumeBuilder':
            options.personalInfo = {
                fullName: document.getElementById('fullName')?.value,
                email: document.getElementById('email')?.value,
                phone: document.getElementById('phone')?.value,
                linkedin: document.getElementById('linkedin')?.value
            };
            options.summary = document.getElementById('summary')?.value;
            options.experience = {
                jobTitle: document.getElementById('jobTitle')?.value,
                company: document.getElementById('company')?.value,
                duration: document.getElementById('duration')?.value,
                responsibilities: document.getElementById('responsibilities')?.value
            };
            options.education = {
                degree: document.getElementById('degree')?.value,
                university: document.getElementById('university')?.value,
                year: document.getElementById('gradYear')?.value
            };
            options.skills = document.getElementById('skills')?.value;
            options.template = document.getElementById('resumeTemplate')?.value;
            break;
        case 'coverLetter':
            options.name = document.getElementById('clName')?.value;
            options.company = document.getElementById('clCompany')?.value;
            options.position = document.getElementById('clPosition')?.value;
            options.manager = document.getElementById('clManager')?.value;
            options.skills = document.getElementById('clSkills')?.value;
            options.why = document.getElementById('clWhy')?.value;
            break;
    }
    
    return options;
}
