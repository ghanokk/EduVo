function openApplicationForm() {
    document.getElementById('applicationModal').classList.add('active');
    document.body.style.overflow = 'hidden';
}

function closeApplicationForm() {
    document.getElementById('applicationModal').classList.remove('active');
    document.body.style.overflow = 'auto';
}

// Close modal when clicking on overlay
document.getElementById('applicationModal').addEventListener('click', function(e) {
    if (e.target === this) {
        closeApplicationForm();
    }
});

// Close modal with Escape key
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
        closeApplicationForm();
    }
});

// Update file button text for CV
document.getElementById('cv').addEventListener('change', function(e) {
    const file = e.target.files[0];
    if (file) {
        const btn = document.querySelector('.upload-btn');
        btn.textContent = file.name;
    }
});

// Update file button text for certificates
document.getElementById('certificates').addEventListener('change', function(e) {
    const files = e.target.files;
    if (files.length > 0) {
        const btn = document.querySelectorAll('.upload-btn')[1];
        btn.textContent = `${files.length} file(s) selected`;
    }
});