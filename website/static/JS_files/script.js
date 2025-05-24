window.addEventListener("DOMContentLoaded", () => {
    const defaultBtn = document.querySelector(".tab-btn.active");
    const bg = document.querySelector(".tab-bg");

    if (defaultBtn && bg) {
        bg.style.width = defaultBtn.offsetWidth + "px";
        bg.style.left = defaultBtn.offsetLeft + "px";
    }

    // Initialize Google Sign-In
    google.accounts.id.initialize({
        client_id: "YOUR_GOOGLE_CLIENT_ID",
        callback: handleGoogleSignIn
    });
    google.accounts.id.renderButton(
        document.querySelector('.google'),
        { theme: "outline", size: "large" }
    );

    // Initialize LinkedIn Sign-In
    IN.init({
        api_key: "YOUR_LINKEDIN_CLIENT_ID"
    });
});

function handleSocialLogin(provider) {
    if (provider === 'google') {
        google.accounts.id.prompt();
    } else if (provider === 'linkedin') {
        IN.UI.Authorize().placeAt('.linkedin');
    }
}

function handleGoogleSignIn(response) {
    // Send Google ID token to your backend
    fetch('/api/auth/google/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            credential: response.credential
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            window.location.href = '/'; // Redirect to home page
        }
    })
    .catch(error => console.error('Error:', error));
}

function handleSignup() {
    const fullname = document.getElementById('fullname').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const confirmation = document.getElementById('confirmation').value;
    const privacyChecked = document.querySelector('.toggle-btn').classList.contains('active');

    if (!privacyChecked) {
        alert('Please agree to the Terms of Service and Privacy Policy');
        return;
    }

    if (password !== confirmation) {
        alert('Passwords do not match');
        return;
    }

    // Send registration data to backend
    fetch('/api/register/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            fullname,
            email,
            password
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Show verification form
            document.getElementById('signup-form').style.display = 'none';
            document.getElementById('verification-form').style.display = 'block';
        } else {
            alert(data.error || 'Registration failed');
        }
    })
    .catch(error => console.error('Error:', error));
}

function verifyEmail() {
    const code = document.getElementById('verification-code').value;
    const email = document.getElementById('email').value;

    fetch('/api/verify-email/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            email,
            code
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            document.getElementById('verification-form').style.display = 'none';
            document.getElementById('success-message').style.display = 'block';
            setTimeout(() => {
                window.location.href = '/'; // Redirect to home page
            }, 3000);
        } else {
            alert(data.error || 'Invalid verification code');
        }
    })
    .catch(error => console.error('Error:', error));
}

function activateTab(button, tabId) {
    // Buttons
    document.querySelectorAll(".tab-btn").forEach(btn => btn.classList.remove("active"));
    button.classList.add("active");

    // Content
    document.querySelectorAll(".tab-content").forEach(c => c.classList.remove("active"));
    setTimeout(() => {
        document.getElementById(tabId).classList.add("active");
    }, 30);

    // Move the blue background behind the active button
    const bg = document.querySelector(".tab-bg");
    bg.style.width = button.offsetWidth + "px";
    bg.style.left = button.offsetLeft + "px";
}

function toggleSwitch() {
    document.querySelector(".toggle-btn").classList.toggle('active');
    document.querySelector('.circle').classList.toggle('active');
    document.getElementById("signup-btn").classList.toggle("disabled");
}

function changeWelcoming(id) {
    if (id === 'signup') {
        document.querySelector('.welcoming-header').textContent = "Join Us";
        document.querySelector('.welcome').textContent = "Sign Up with";
        document.querySelector('.welcome-p').textContent = "Welcome to Eduvo, the platform designed for your success";
    } else if (id === 'login') {
        document.querySelector('.welcoming-header').textContent = "Welcome Back";
        document.querySelector('.welcome').textContent = "Login with";
        document.querySelector('.welcome-p').textContent = "";
    }
}