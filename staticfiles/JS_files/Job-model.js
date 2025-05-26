
        function openApplicationForm() {
            document.getElementById('applicationModal').classList.add('active');
            document.body.style.overflow = 'hidden';
        }

        function closeApplicationForm() {
            document.getElementById('applicationModal').classList.remove('active');
            document.body.style.overflow = 'auto';
        }

        // Fermer le modal en cliquant sur l'overlay
        document.getElementById('applicationModal').addEventListener('click', function(e) {
            if (e.target === this) {
                closeApplicationForm();
            }
        });

        // Fermer avec la touche Escape
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape') {
                closeApplicationForm();
            }
        });

        // Gestion des fichiers uploadés
        document.getElementById('cv').addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                const btn = document.querySelector('.upload-btn');
                btn.textContent = file.name;
            }
        });
        
        document.getElementById('certificates').addEventListener('change', function(e) {
            const files = e.target.files;
            if (files.length > 0) {
                const btn = document.querySelectorAll('.upload-btn')[1];
                btn.textContent = `${files.length} file(s) selected`;
            }
        });

        // Soumission du formulaire
        document.querySelector('.submit-btn').addEventListener('click', function(e) {
            e.preventDefault();
            
            // Simulation de l'envoi
            const submitBtn = this;
            const originalText = submitBtn.textContent;
            
            submitBtn.textContent = 'Submitting...';
            submitBtn.disabled = true;
            
            setTimeout(function() {
                alert('Application submitted successfully!');
                closeApplicationForm();
                
                // Reset form
                document.getElementById('fullName').value = '';
                document.getElementById('email').value = '';
                document.getElementById('phone').value = '';
                document.getElementById('preferredContact').value = '';
                document.getElementById('coverLetter').value = '';
                document.getElementById('experience').value = '';
                document.getElementById('skills').value = '';
                document.getElementById('availability').value = '';
                document.getElementById('location').value = '';
                
                // Reset file uploads
                document.getElementById('cv').value = '';
                document.getElementById('certificates').value = '';
                document.querySelectorAll('.upload-btn')[0].textContent = 'Upload CV';
                document.querySelectorAll('.upload-btn')[1].textContent = 'Upload Files';
                
                submitBtn.textContent = originalText;
                submitBtn.disabled = false;
            }, 2000);
        });
