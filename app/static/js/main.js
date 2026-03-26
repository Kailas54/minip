
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
        modalContent.innerHTML = '<div style="display: flex; flex-direction: column; justify-content: center; align-items: center; padding: 40px;"><i class="fas fa-circle-notch fa-spin fa-3x" style="color: var(--primary-color); margin-bottom: 20px;"></i><p>Analyzing video for violations...</p><p style="margin-top: 10px; font-size: 0.9em; color: var(--text-muted);">Detecting: Speed, Helmets, Number Plates</p></div>';

        const formData = new FormData();
        formData.append('video', uploadInput.files[0]);

        fetch('/process-video/', {
            method: 'POST',
            body: formData
        })
            .then(response => response.json())
            .then(result => {
                if (result.status === 'success') {
                    const violations = result.data.violations || [];
                    const stats = result.data.statistics || {};
                    
                    let html = "<div style='padding: 15px;'>";
                    
                    // Display Statistics Summary
                    if (stats.total_violations !== undefined) {
                        html += `<div style='background: linear-gradient(135deg, rgba(99, 102, 241, 0.1), rgba(168, 85, 247, 0.1)); padding: 20px; border-radius: 12px; margin-bottom: 20px; border-left: 4px solid var(--primary-color);'>
                            <h4 style='margin: 0 0 15px 0; color: var(--text-main);'><i class='fas fa-chart-bar'></i> Analysis Summary</h4>
                            <div style='display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px;'>
                                <div style='text-align: center;'>
                                    <div style='font-size: 2em; font-weight: bold; color: #ef4444;'>${stats.overspeeding_count || 0}</div>
                                    <div style='font-size: 0.85em; color: var(--text-muted);'>Overspeeding</div>
                                </div>
                                <div style='text-align: center;'>
                                    <div style='font-size: 2em; font-weight: bold; color: #f59e0b;'>${stats.no_helmet_count || 0}</div>
                                    <div style='font-size: 0.85em; color: var(--text-muted);'>No Helmet</div>
                                </div>
                                <div style='text-align: center;'>
                                    <div style='font-size: 2em; font-weight: bold; color: #10b981;'>${stats.plates_detected || 0}</div>
                                    <div style='font-size: 0.85em; color: var(--text-muted);'>Plates Detected</div>
                                </div>
                            </div>
                        </div>`;
                    }
                    
                    // Display Violations
                    html += "<h4 style='margin: 0 0 15px 0; color: var(--text-main);'><i class='fas fa-exclamation-triangle'></i> Detailed Violations</h4>";
                    html += "<div style='max-height: 400px; overflow-y: auto;'>";
                    
                    if (violations.length > 0) {
                        violations.forEach((item, index) => {
                            let icon, color, bgColor, borderColor;
                            
                            switch(item.type) {
                                case 'overspeeding':
                                    icon = 'fa-tachometer-alt';
                                    color = '#ef4444';
                                    bgColor = 'rgba(239, 68, 68, 0.05)';
                                    borderColor = '#ef4444';
                                    break;
                                case 'no_helmet':
                                    icon = 'fa-hard-hat';
                                    color = '#f59e0b';
                                    bgColor = 'rgba(245, 158, 11, 0.05)';
                                    borderColor = '#f59e0b';
                                    break;
                                case 'number_plate':
                                    icon = 'fa-id-card';
                                    color = '#10b981';
                                    bgColor = 'rgba(16, 185, 129, 0.05)';
                                    borderColor = '#10b981';
                                    break;
                                case 'summary':
                                    icon = 'fa-info-circle';
                                    color = '#6b7280';
                                    bgColor = 'rgba(107, 114, 128, 0.05)';
                                    borderColor = '#6b7280';
                                    break;
                                default:
                                    icon = 'fa-car';
                                    color = 'var(--primary-color)';
                                    bgColor = 'rgba(99, 102, 241, 0.05)';
                                    borderColor = 'var(--primary-color)';
                            }
                            
                            html += `<div style='margin-bottom: 12px; padding: 15px; border-radius: 8px; background: ${bgColor}; border-left: 4px solid ${borderColor};'>`;
                            
                            if (item.type === 'summary') {
                                html += `<p style='margin: 0; color: var(--text-muted);'><i class="fas ${icon}"></i> ${item.message || 'No violations detected'}</p>`;
                                if (item.duration) {
                                    html += `<p style='margin: 5px 0 0 0; font-size: 0.85em; color: var(--text-muted);'>Duration: ${item.duration}</p>`;
                                }
                            } else {
                                // Header with icon and type
                                let headerText = '';
                                let showPlate = false;
                                                            
                                if (item.type === 'overspeeding') {
                                    headerText = `Overspeeding - ${item.speed}`;
                                    showPlate = true;  // Always show plate for speeders
                                } else if (item.type === 'no_helmet') {
                                    headerText = 'No Helmet Detected';
                                    showPlate = true;  // Always show plate for helmet violators
                                } else if (item.type === 'number_plate') {
                                    headerText = `Vehicle & Plate Detected`;
                                }
                                
                                html += `<p style='margin: 0 0 8px 0; font-weight: 600; color: ${color};'>
                                    <i class="fas ${icon}"></i> ${headerText}
                                </p>`;
                                
                                // Details
                                if (item.vehicle_type) {
                                    html += `<p style='margin: 0 0 5px 0; font-size: 0.9em;'><i class="fas fa-car"></i> Vehicle: ${item.vehicle_type}</p>`;
                                }
                                
                                // Show plate prominently for violators
                                if (showPlate && item.plate) {
                                    html += `<p style='margin: 5px 0 5px 0; font-size: 1.1em; font-weight: bold;'><i class="fas fa-id-card"></i> NUMBER PLATE: <span style='color: ${color}; background: rgba(255,255,255,0.3); padding: 4px 8px; border-radius: 4px;'>${item.plate}</span></p>`;
                                } else if (item.plate) {
                                    html += `<p style='margin: 0 0 5px 0; font-size: 0.9em;'><i class="fas fa-id-card"></i> Plate: <span style='color: ${color}; font-weight: 600;'>${item.plate}</span></p>`;
                                }
                                
                                if (item.frame) {
                                    html += `<p style='margin: 0 0 5px 0; font-size: 0.85em; color: var(--text-muted);'><i class="fas fa-film"></i> Frame: ${item.frame}</p>`;
                                }
                                
                                if (item.severity) {
                                    const severityColor = item.severity === 'high' ? '#ef4444' : '#f59e0b';
                                    html += `<p style='margin: 0; font-size: 0.85em; color: ${severityColor};'><i class="fas fa-exclamation-circle"></i> Severity: ${item.severity.toUpperCase()}</p>`;
                                }
                            }
                            
                            html += `</div>`;
                        });
                    } else {
                        html += "<div style='padding: 30px; text-align: center; color: var(--text-muted);'>";
                        html += "<i class='fas fa-check-circle fa-3x' style='color: #10b981; margin-bottom: 15px;'></i>";
                        html += "<p>No violations detected in the processed video segment.</p>";
                        html += "</div>";
                    }
                    
                    html += "</div></div>";
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

// Vehicle Registration Functions
function openRegistrationModal() {
    $('#registrationModal').modal('show');
}

function submitVehicleRegistration() {
    const phoneNumber = document.getElementById('reg-phone').value.trim();
    const vehicleNumber = document.getElementById('reg-vehicle').value.trim().toUpperCase();
    const messageDiv = document.getElementById('registration-message');
    
    // Validation
    if (!phoneNumber || !vehicleNumber) {
        messageDiv.innerHTML = '<p style="color: #ef4444;">Please fill in all fields</p>';
        return;
    }
    
    if (phoneNumber.length !== 10 || !/^\d+$/.test(phoneNumber)) {
        messageDiv.innerHTML = '<p style="color: #ef4444;">Please enter a valid 10-digit mobile number</p>';
        return;
    }
    
    // Submit to backend
    fetch('/register-vehicle/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            phone_number: phoneNumber,
            vehicle_number: vehicleNumber
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            messageDiv.innerHTML = `
                <div style="padding: 15px; background: rgba(16, 185, 129, 0.1); border-left: 4px solid #10b981; border-radius: 8px;">
                    <i class="fas fa-check-circle" style="color: #10b981; margin-right: 8px;"></i>
                    <span style="color: #10b981; font-weight: 600;">${data.message}</span>
                    <br><small style="color: #94a3b8; display: block; margin-top: 8px;">
                        Vehicle: ${data.vehicle_number}<br>
                        You will receive alerts when this vehicle violates traffic rules.
                    </small>
                </div>
            `;
            // Clear form after 3 seconds
            setTimeout(() => {
                document.getElementById('vehicle-registration-form').reset();
                messageDiv.innerHTML = '';
                $('#registrationModal').modal('hide');
            }, 3000);
        } else {
            messageDiv.innerHTML = `<p style="color: #ef4444;">Error: ${data.message}</p>`;
        }
    })
    .catch(error => {
        messageDiv.innerHTML = `<p style="color: #ef4444;">Connection error: ${error.message}</p>`;
    });
}

// Vibration Alert Function
function triggerVibrationAlert(violatingPlates) {
    fetch('/trigger-alert/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            violating_plates: violatingPlates
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success' && data.alerts_sent > 0) {
            // Trigger browser vibration API if supported
            if (navigator.vibrate) {
                // Pattern: vibrate 500ms, pause 200ms, vibrate 500ms
                navigator.vibrate([500, 200, 500]);
            }
            
            // Show notification toast
            showVibrationNotification(data.matched_users || data.alerts);
        }
    })
    .catch(error => {
        console.error('Vibration alert error:', error);
    });
}

function showVibrationNotification(alerts) {
    // Create notification element
    const notification = document.createElement('div');
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: linear-gradient(135deg, #ef4444, #dc2626);
        color: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 10px 40px rgba(239, 68, 68, 0.4);
        z-index: 10000;
        max-width: 400px;
        animation: slideIn 0.3s ease-out;
    `;
    
    let html = `
        <div style="display: flex; align-items: start;">
            <i class="fas fa-exclamation-triangle" style="font-size: 1.5em; margin-right: 15px;"></i>
            <div style="flex: 1;">
                <h4 style="margin: 0 0 10px 0; font-weight: 700;">🚨 Vehicle Violation Alert!</h4>
                <p style="margin: 0 0 10px 0; font-size: 0.9em; opacity: 0.9;">Registered vehicles detected violating traffic rules:</p>
                <ul style="margin: 0; padding-left: 20px;">
    `;
    
    alerts.forEach(alert => {
        html += `
            <li style="margin-bottom: 5px;">
                <strong>${alert.vehicle_number}</strong> - Phone: ${alert.phone_number}
            </li>
        `;
    });
    
    html += `
                </ul>
            </div>
            <button onclick="this.parentElement.parentElement.remove()" style="background: none; border: none; color: white; cursor: pointer; font-size: 1.2em; padding: 0; margin-left: 10px;">&times;</button>
        </div>
    `;
    
    notification.innerHTML = html;
    document.body.appendChild(notification);
    
    // Auto-remove after 10 seconds
    setTimeout(() => {
        if (notification && notification.parentElement) {
            notification.style.animation = 'slideOut 0.3s ease-out';
            setTimeout(() => notification.remove(), 300);
        }
    }, 10000);
}

// Add CSS animations for notifications
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from { transform: translateX(400px); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    @keyframes slideOut {
        from { transform: translateX(0); opacity: 1; }
        to { transform: translateX(400px); opacity: 0; }
    }
`;
document.head.appendChild(style);

