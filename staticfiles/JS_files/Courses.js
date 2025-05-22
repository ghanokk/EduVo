const prevButton = document.querySelector('.prev');
const nextButton = document.querySelector('.next');
const carousel = document.querySelector('.carousel');
let currentIndex = 1;

function showSlide(index) {
    const totalItems = carousel.children.length;

    if (index >= totalItems) {
        currentIndex = 0; // Revenir au premier élément
    } else if (index < 0) {
        currentIndex = totalItems - 1; // Revenir au dernier élément
    }

    // Appliquer la transformation pour déplacer le carousel avec une animation
    carousel.style.transform = `translateX(-${currentIndex * 100}%)`;
}

prevButton.addEventListener('click', () => {
    currentIndex--;
    showSlide(currentIndex);
});

nextButton.addEventListener('click', () => {
    currentIndex++;
    showSlide(currentIndex);
});

// Initialisation du premier slide
showSlide(currentIndex);

console.log(carousel.children[0]);

// ------------------------------------------------browse category---------------------

// const catBtn = document.querySelector('.search-category-btn');
// const catMenu = document.querySelector('.search-category')
// catBtn.addEventListener('mouseenter',()=>{
// catMenu.style.display='block';
// });

// catBtn.addEventListener('mouseleave',()=>{

//   catMenu.style.display='none';
//   });

// Filter functionality
function filterCourses() {
    // Get all filter values
    const selectedRating = document.querySelector('.selected-rating span').textContent;
    const selectedPriceType = document.querySelector('input[name="price_type"]:checked')?.value;
    const selectedLevel = document.querySelector('input[name="level"]:checked')?.value;
    const searchQuery = document.querySelector('.search-bar-input').value;

    // Build query parameters
    const params = new URLSearchParams();
    if (selectedRating) params.append('rating', selectedRating);
    if (selectedPriceType) params.append('price_type', selectedPriceType);
    if (selectedLevel) params.append('level', selectedLevel);
    if (searchQuery) params.append('search', searchQuery);

    // Redirect to filtered URL
    window.location.href = `${window.location.pathname}?${params.toString()}`;
}

// Rating selection
const ratingItems = document.querySelectorAll('.rating-item');
const selectedRatingSpan = document.querySelector('.selected-rating span');

ratingItems.forEach(item => {
    item.addEventListener('click', () => {
        const rating = item.getAttribute('data-rating');
        selectedRatingSpan.textContent = rating;
        
        // Update star colors
        ratingItems.forEach(star => {
            if (star.getAttribute('data-rating') <= rating) {
                star.style.color = '#FFD700';
            } else {
                star.style.color = '#ccc';
            }
        });
    });
});

// Clear filters
document.querySelector('.clear').addEventListener('click', () => {
    // Reset rating
    selectedRatingSpan.textContent = '0';
    ratingItems.forEach(star => star.style.color = '#ccc');
    
    // Reset price type
    const priceInputs = document.querySelectorAll('input[name="price_type"]');
    priceInputs.forEach(input => input.checked = false);
    
    // Reset level
    const levelInputs = document.querySelectorAll('input[name="level"]');
    levelInputs.forEach(input => input.checked = false);
    
    // Reset search
    document.querySelector('.search-bar-input').value = '';
    
    // Redirect to base URL without filters
    window.location.href = window.location.pathname;
});

// Apply all button
document.querySelector('.apply').addEventListener('click', filterCourses);

// Add click handlers for course list boxes
document.addEventListener('DOMContentLoaded', function() {
    const courseBoxes = document.querySelectorAll('.course-list-box');
    courseBoxes.forEach(box => {
        box.addEventListener('click', function() {
            const url = this.getAttribute('data-course-url');
            if (url) {
                window.location.href = url;
            }
        });
    });
});
