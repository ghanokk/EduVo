window.addEventListener("DOMContentLoaded", () => {
    const defaultBtn = document.querySelector(".tab-btn.active");
    const bg = document.querySelector(".tab-bg");

    if (defaultBtn && bg) {
        bg.style.width = defaultBtn.offsetWidth + "px";
        bg.style.left = defaultBtn.offsetLeft + "px";
    }
});


function activateTab(button, tabId) {
    // Boutons
    document.querySelectorAll(".tab-btn").forEach(btn => btn.classList.remove("active"));
    button.classList.add("active");

    // Contenu
    document.querySelectorAll(".tab-content").forEach(c => c.classList.remove("active"));
    setTimeout(() => {
        document.getElementById(tabId).classList.add("active");

    }, 30);

    // Déplacer le background bleu derrière le bouton actif
    const bg = document.querySelector(".tab-bg");
    bg.style.width = button.offsetWidth + "px";
    bg.style.left = button.offsetLeft + "px";


}

function toggleSwitch() {
    document.querySelector(".toggle-btn").classList.toggle('active');
    document.querySelector('.circle').classList.toggle('active');
    document.getElementById("signup-btn").classList.toggle("disabled")

}


function changeWelcoming(id) {
    if (id == 'signup') {
        document.querySelector('.welcoming-header').textContent = "Join Us"
        document.querySelector('.welcome').textContent = "Sign Up with"
        document.querySelector('.welcome-p').textContent = "Welcome to Eduvo, the platform designed for your success"

    }

    if (id == 'login') {
        document.querySelector('.welcoming-header').textContent = "Welcome Back"
        document.querySelector('.welcome').textContent = "Login with"
        document.querySelector('.welcome-p').textContent = ""
    }
}