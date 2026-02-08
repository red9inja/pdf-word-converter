let selectedFile = null;

document.getElementById('fileInput').addEventListener('change', function(e) {
    selectedFile = e.target.files[0];
    if (selectedFile) {
        document.getElementById('fileName').textContent = `Selected: ${selectedFile.name}`;
        document.getElementById('convertBtn').disabled = false;
    }
});

document.getElementById('convertBtn').addEventListener('click', async function() {
    if (!selectedFile) return;

    const statusDiv = document.getElementById('status');
    const downloadSection = document.getElementById('downloadSection');
    
    statusDiv.className = 'status processing';
    statusDiv.textContent = '⏳ Converting your PDF...';
    downloadSection.style.display = 'none';

    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
        const response = await fetch('/api/convert', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error('Conversion failed');
        }

        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const downloadLink = document.getElementById('downloadLink');
        
        downloadLink.href = url;
        downloadLink.download = selectedFile.name.replace('.pdf', '.docx');
        
        statusDiv.className = 'status success';
        statusDiv.textContent = '✅ Conversion successful!';
        downloadSection.style.display = 'block';

    } catch (error) {
        statusDiv.className = 'status error';
        statusDiv.textContent = '❌ Conversion failed. Please try again.';
        console.error('Error:', error);
    }
});
