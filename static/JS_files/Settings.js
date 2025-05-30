 const textarea = document.getElementById("bio");

    function autoResize(el) {
      el.style.height = 'auto';
      el.style.height = el.scrollHeight + 'px';
    }

    textarea.addEventListener('input', () => autoResize(textarea));
    window.addEventListener('DOMContentLoaded', () => autoResize(textarea));
