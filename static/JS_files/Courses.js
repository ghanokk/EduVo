// Global function for filtering
function filterCourses() {
    const selectedRating = document.querySelector('.selected-rating span')?.textContent || '0';
    const selectedPriceType = document.querySelector('input[name="price_type"]:checked')?.value;
    const selectedLevel = document.querySelector('input[name="level"]:checked')?.value;
    const searchQuery = document.querySelector('.search-bar-input')?.value || '';

    const params = new URLSearchParams();
    if (selectedRating && selectedRating !== '0') params.append('rating', selectedRating);
    if (selectedPriceType) params.append('price_type', selectedPriceType);
    if (selectedLevel) params.append('level', selectedLevel);
    if (searchQuery) params.append('search', searchQuery);

    window.location.href = `${window.location.pathname}?${params.toString()}`;
}

// Initialize everything when DOM is loaded
window.addEventListener('load', function() {
    // Carousel functionality
    const prevButton = document.querySelector('.prev');
    const nextButton = document.querySelector('.next');
    const carousel = document.querySelector('.carousel');
    let currentIndex = 1;

    function showSlide(index) {
        const totalItems = carousel.children.length;
        if (totalItems === 0) return;

        if (index >= totalItems) {
            currentIndex = 0;
        } else if (index < 0) {
            currentIndex = totalItems - 1;
        }

        carousel.style.transform = `translateX(-${currentIndex * 100}%)`;
    }

    if (prevButton && nextButton) {
        prevButton.onclick = function() {
            currentIndex--;
            showSlide(currentIndex);
        };

        nextButton.onclick = function() {
            currentIndex++;
            showSlide(currentIndex);
        };

        // Initialize first slide
        showSlide(currentIndex);
    }

    // Rating functionality
    const ratingItems = document.querySelectorAll('.rating-item[data-rating]');
    const selectedRatingSpan = document.querySelector('.selected-rating span');

    if (ratingItems.length > 0 && selectedRatingSpan) {
        ratingItems.forEach(function(item) {
            item.onclick = function() {
                const rating = this.getAttribute('data-rating');
                selectedRatingSpan.textContent = rating;
                
                // Update star colors
                ratingItems.forEach(function(star) {
                    const starRating = star.getAttribute('data-rating');
                    star.style.color = starRating <= rating ? '#FFD700' : '#ccc';
                });
            };
        });
    }

    // Add click handler for filter button
    const filterButton = document.querySelector('.submit-filter');
    if (filterButton) {
        filterButton.onclick = filterCourses;
    }

    // Clear filters
    const clearButton = document.querySelector('.clear');
    if (clearButton) {
        clearButton.onclick = function() {
            // Reset rating
            if (selectedRatingSpan) {
                selectedRatingSpan.textContent = '0';
            }
            if (ratingItems.length > 0) {
                ratingItems.forEach(function(star) {
                    star.style.color = '#ccc';
                });
            }
            
            // Reset price type
            const priceInputs = document.querySelectorAll('input[name="price_type"]');
            priceInputs.forEach(function(input) {
                input.checked = false;
            });
            
            // Reset level
            const levelInputs = document.querySelectorAll('input[name="level"]');
            levelInputs.forEach(function(input) {
                input.checked = false;
            });
            
            // Reset search
            const searchInput = document.querySelector('.search-bar-input');
            if (searchInput) {
                searchInput.value = '';
            }
            
            // Redirect to base URL without filters
            window.location.href = window.location.pathname;
        };
    }

    // Apply all button
    const applyButton = document.querySelector('.apply');
    if (applyButton) {
        applyButton.onclick = filterCourses;
    }

    // Course list boxes
    const courseBoxes = document.querySelectorAll('.course-list-box');
    courseBoxes.forEach(function(box) {
        box.onclick = function() {
            const url = this.getAttribute('data-course-url');
            if (url) {
                window.location.href = url;
            }
        };
    });
});

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
