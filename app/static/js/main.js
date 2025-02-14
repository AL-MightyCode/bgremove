document.addEventListener('DOMContentLoaded', function() {
    const imageInput = document.getElementById('imageInput');
    const uploadBtn = document.getElementById('uploadBtn');
    const removeBackgroundBtn = document.getElementById('removeBackgroundBtn');
    const originalImage = document.getElementById('originalImage');
    const processedImage = document.getElementById('processedImage');
    const bgColorInput = document.getElementById('bgColor');
    const downloadBtn = document.getElementById('downloadBtn');
    const originalPreview = document.getElementById('originalPreview');
    const processedPreview = document.getElementById('processedPreview');

    // Handle file input through button
    uploadBtn.addEventListener('click', () => {
        imageInput.click();
    });

    // Preview uploaded image
    imageInput.addEventListener('change', function(e) {
        if (this.files && this.files[0]) {
            const reader = new FileReader();
            reader.onload = function(e) {
                originalImage.src = e.target.result;
                originalPreview.style.display = 'flex';
                processedPreview.style.display = 'none';
            };
            reader.readAsDataURL(this.files[0]);
        }
    });

    // Remove background
    removeBackgroundBtn.addEventListener('click', async () => {
        const formData = new FormData();
        formData.append('image', imageInput.files[0]);

        try {
            removeBackgroundBtn.disabled = true;
            removeBackgroundBtn.textContent = 'Processing...';

            const response = await fetch('/remove-background', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (data.status === 'success') {
                processedImage.src = `data:image/png;base64,${data.image}`;
                processedPreview.style.display = 'flex';
                updateBackgroundColor();
            } else {
                alert('Error processing image');
            }
        } catch (error) {
            console.error('Error:', error);
            alert('Error processing image');
        } finally {
            removeBackgroundBtn.disabled = false;
            removeBackgroundBtn.textContent = 'Remove Background';
        }
    });

    // Update background color
    bgColorInput.addEventListener('change', function() {
        if (this.value) {
            processedImage.style.backgroundColor = this.value;
        }
    });

    function updateBackgroundColor() {
        processedImage.style.backgroundColor = bgColorInput.value;
    }

    // Download processed image
    downloadBtn.addEventListener('click', () => {
        const canvas = document.createElement('canvas');
        const ctx = canvas.getContext('2d');
        const img = new Image();
        
        img.onload = function() {
            canvas.width = img.width;
            canvas.height = img.height;
            
            // Draw background color
            ctx.fillStyle = bgColorInput.value;
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            
            // Draw image
            ctx.drawImage(img, 0, 0);
            
            // Create download link
            const link = document.createElement('a');
            link.download = 'processed-image.png';
            link.href = canvas.toDataURL('image/png');
            link.click();
        };
        
        img.src = processedImage.src;
    });
}); 