
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

    // Show modal using jQuery/Bootstrap
    $('#resultsModal').modal('show');

    if (modalContent) {
        // Add loading state
        modalContent.innerHTML = '<div style="display: flex; justify-content: center; align-items: center; padding: 40px;"><i class="fas fa-circle-notch fa-spin fa-3x" style="color: var(--primary-color);"></i></div>';

        setTimeout(() => {
            let mockData = "";
            switch (buttonId) {
                case 'detect-helmet':
                    mockData = `<p><span><i class="fas fa-head-side-mask"></i> Helmet Status:</span> <span style='color: #ef4444; font-weight: 600;'>No Helmet</span></p>
                                <p><span><i class="fas fa-id-card"></i> Number Plate:</span> <span style='color: #6366f1; font-weight: 600;'>MH 12 AB 1234</span></p>`;
                    break;
                case 'detect-speed':
                    mockData = `<p><span><i class="fas fa-tachometer-alt"></i> Estimated Speed:</span> <span style='color: #f59e0b; font-weight: 600;'>72 km/h</span></p>
                                <p style='color: #ef4444; border: none; font-size: 0.9rem; width: 100%; text-align: center;'><i class="fas fa-exclamation-triangle"></i> Speed violation detected!</p>`;
                    break;
                case 'extract-numberplate':
                    mockData = `<p><span><i class="fas fa-search"></i> OCR Extraction:</span> <span style='color: #10b981; font-weight: 600;'>IND MH12AB1234</span></p>
                                <p><span><i class="fas fa-check-circle"></i> Confidence:</span> 94%</p>`;
                    break;
                default:
                    mockData = "Running detection...";
            }
            modalContent.innerHTML = mockData;
        }, 1200); // Increased delay slightly for better UX feel
    }
}

