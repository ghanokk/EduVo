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
