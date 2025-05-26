// Function to toggle course sections
function toggleSection(header) {
    // Get the section element
    const section = header.parentElement;
    const content = section.querySelector('.section-content');
    
    // Toggle active class on section
    section.classList.toggle('active');
    
    // Toggle content visibility with smooth animation
    if (section.classList.contains('active')) {
        content.style.maxHeight = content.scrollHeight + "px";
        content.style.opacity = "1";
        header.querySelector('img').style.transform = "rotate(180deg)";
    } else {
        content.style.maxHeight = "0";
        content.style.opacity = "0";
        header.querySelector('img').style.transform = "rotate(0deg)";
    }
}

// Initialize all sections on page load
document.addEventListener('DOMContentLoaded', function() {
    // Get all section headers
    const sectionHeaders = document.querySelectorAll('.section-header');
    
    // Add click event listeners
    sectionHeaders.forEach(header => {
        const section = header.parentElement;
        const content = section.querySelector('.section-content');
        
        // Set initial state
        if (section.classList.contains('active')) {
            content.style.maxHeight = content.scrollHeight + "px";
            content.style.opacity = "1";
            header.querySelector('img').style.transform = "rotate(180deg)";
        } else {
            content.style.maxHeight = "0";
            content.style.opacity = "0";
            header.querySelector('img').style.transform = "rotate(0deg)";
        }
    });
}); 