
// UI Feedback and Interactions
document.addEventListener("DOMContentLoaded", function () {
    const uploadInput = document.getElementById('video-upload');
    const uploadBox = document.getElementById('upload-box');
    const fileNameDisplay = document.getElementById('file-name-display');
    const uploadButton = document.getElementById('upload-button');

    // Link button to hidden input
    if (uploadButton && uploadInput) {
        uploadButton.addEventListener('click', () => uploadInput.click());
    }

    // Handle file selection
    if (uploadInput) {
        uploadInput.addEventListener('change', function () {
            if (this.files && this.files[0]) {
                const file = this.files[0];
                fileNameDisplay.textContent = `Selected: ${file.name}`;
                uploadBox.style.borderColor = 'var(--primary-color)';
                uploadBox.style.background = 'rgba(99, 102, 241, 0.1)';
            }
        });
    }

    // Drag and Drop support
    if (uploadBox) {
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            uploadBox.addEventListener(eventName, preventDefaults, false);
        });

        function preventDefaults(e) {
            e.preventDefault();
            e.stopPropagation();
        }

        ['dragenter', 'dragover'].forEach(eventName => {
            uploadBox.addEventListener(eventName, () => {
                uploadBox.style.borderColor = 'var(--primary-color)';
                uploadBox.style.background = 'rgba(99, 102, 241, 0.1)';
            }, false);
        });

        ['dragleave', 'drop'].forEach(eventName => {
            uploadBox.addEventListener(eventName, () => {
                uploadBox.style.borderColor = 'var(--glass-border)';
                uploadBox.style.background = 'var(--card-bg)';
            }, false);
        });

        uploadBox.addEventListener('drop', (e) => {
            const dt = e.dataTransfer;
            const files = dt.files;
            if (uploadInput) {
                uploadInput.files = files;
                if (files[0]) {
                    fileNameDisplay.textContent = `Selected: ${files[0].name}`;
                }
            }
        });
    }

    // Option box click handling
    const optionBoxes = document.querySelectorAll('.option-box');
    optionBoxes.forEach(box => {
        box.addEventListener('click', handleOptionBoxClick);
    });
});

function handleOptionBoxClick(event) {
    const buttonId = event.currentTarget.id;
    const modalContent = document.getElementById('modal-results-content');
    const uploadInput = document.getElementById('video-upload');

    if (!uploadInput || !uploadInput.files || !uploadInput.files[0]) {
        alert("Please upload a video file first!");
        return;
    }

    // Show modal using jQuery/Bootstrap
    $('#resultsModal').modal('show');

    if (modalContent) {
        // Add loading state
        modalContent.innerHTML = '<div style="display: flex; flex-direction: column; justify-content: center; align-items: center; padding: 40px;"><i class="fas fa-circle-notch fa-spin fa-3x" style="color: var(--primary-color); margin-bottom: 20px;"></i><p>Analyzing video using YOLOv8 & EasyOCR...</p></div>';

        const formData = new FormData();
        formData.append('video', uploadInput.files[0]);

        fetch('/process-video/', {
            method: 'POST',
            body: formData
        })
            .then(response => response.json())
            .then(result => {
                if (result.status === 'success') {
                    let html = "<h4><i class='fas fa-chart-bar'></i> Detection Results</h4><ul style='list-style: none; padding: 0;'>";
                    if (result.data && result.data.length > 0) {
                        result.data.forEach((item, index) => {
                            html += `<li style='margin-bottom: 12px; padding: 15px; border-radius: 8px; background: rgba(99, 102, 241, 0.05); border-left: 4px solid var(--primary-color);'>
                            <p style='margin: 0 0 8px 0;'><strong><i class="fas fa-car" style="color: var(--primary-color);"></i> Vehicle Detected</strong></p>
                            <p style='margin: 0 0 5px 0;'><span><i class="fas fa-id-card"></i> Number Plate:</span> <span style='color: #10b981; font-weight: 600; font-size: 1.1em;'>${item.plate || 'Not detected'}</span></p>
                            <p style='margin: 0; font-size: 0.85em; color: var(--text-muted);'><i class="fas fa-film"></i> Found at frame: ${item.frame}</p>
                        </li>`;
                        });
                    } else {
                        html += "<li style='padding: 15px; text-align: center; color: var(--text-muted);'>No vehicles or license plates detected in the sample frames.</li>";
                    }
                    html += "</ul>";
                    modalContent.innerHTML = html;
                } else {
                    modalContent.innerHTML = `<div style="padding: 20px; text-align: center;"><i class="fas fa-exclamation-triangle fa-2x" style="color: #ef4444; margin-bottom: 10px;"></i><p style="color: #ef4444;">Error processing video: <br>${result.message}</p></div>`;
                }
            })
            .catch(err => {
                modalContent.innerHTML = `<div style="padding: 20px; text-align: center;"><i class="fas fa-wifi fa-2x" style="color: #ef4444; margin-bottom: 10px;"></i><p style="color: #ef4444;">Connection error: <br>${err.message}</p></div>`;
            });
    }
}

