// AWS API Gateway endpoint - Replace with your actual endpoint
const API_ENDPOINT = 'https://YOUR-API-ID.execute-api.us-east-1.amazonaws.com/prod/convert';

let selectedFile = null;

document.getElementById('fileInput').addEventListener('change', function(e) {
    selectedFile = e.target.files[0];
    if (selectedFile) {
        if (selectedFile.size > 10 * 1024 * 1024) { // 10MB limit
            alert('File size should be less than 10MB');
            return;
        }
        document.getElementById('fileName').textContent = `Selected: ${selectedFile.name}`;
        document.getElementById('convertBtn').disabled = false;
    }
});

document.getElementById('convertBtn').addEventListener('click', async function() {
    if (!selectedFile) return;

    const statusDiv = document.getElementById('status');
    const downloadSection = document.getElementById('downloadSection');
    
    statusDiv.className = 'status processing';
    statusDiv.textContent = '⏳ Converting your PDF... This may take a minute.';
    downloadSection.style.display = 'none';
    this.disabled = true;

    try {
        // Read file as base64
        const reader = new FileReader();
        reader.onload = async function(e) {
            const base64File = e.target.result.split(',')[1];
            
            const response = await fetch(API_ENDPOINT, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    file: base64File,
                    filename: selectedFile.name
                })
            });

            const result = await response.json();

            if (result.success) {
                const downloadLink = document.getElementById('downloadLink');
                downloadLink.href = result.download_url;
                downloadLink.download = selectedFile.name.replace('.pdf', '.docx');
                
                statusDiv.className = 'status success';
                statusDiv.textContent = '✅ Conversion successful! Click below to download.';
                downloadSection.style.display = 'block';
            } else {
                throw new Error(result.error || 'Conversion failed');
            }
        };
        
        reader.readAsDataURL(selectedFile);

    } catch (error) {
        statusDiv.className = 'status error';
        statusDiv.textContent = '❌ Conversion failed. Please try again or use a different file.';
        console.error('Error:', error);
    } finally {
        document.getElementById('convertBtn').disabled = false;
    }
});
