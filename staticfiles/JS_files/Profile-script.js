const btn = document.querySelector('.circle');
const btnArea = document.querySelector('.toggle-btn');
const settingPage = document.querySelector('.settings-page')
const all = document.querySelector('.all')
const textarea = document.querySelector('#bio-space')
const editPage = document.querySelector('.edit-profile-page')
const username = document.querySelector('#username-value')
const userInput = document.querySelector('#user-input')
const editForm = document.querySelector('.edit-form-container')
const inputForm = document.querySelector('#user-input')
const localisation = document.querySelector('#loc')
const wilaya = document.querySelector('#wilaya')
const country = document.querySelector('#country')
const imgForm = document.querySelector('.add-picture')
const bio = document.querySelector('#bio-space')
const bioField = document.querySelector('#bio-field')
const usernameSaved = document.querySelector('#username1')
const localisationSaved = document.querySelector('#location1')





function showSettings(){
settingPage.classList.add('shown')
settingPage.classList.remove('hidden')
all.style
document.body.style.overflow='hidden'

}


function hideSettings(){
    settingPage.classList.remove('shown')
    settingPage.classList.add('hidden')
    all.style.filter = 'blur(0px)'
    document.body.style.overflow=''
    hideImgForm()
}

function toggleBtn(){
btnArea.classList.toggle('enabled')
btn.classList.toggle('on');
}

textarea.addEventListener('input', () => {
  textarea.style.height = 'auto';
  textarea.style.height = textarea.scrollHeight + 'px';
});


function showEdit(){
    editPage.style.display='block'
    all.style.filter ='blur(5px)'
    document.body.style.overflow=''
}

function hideEdit(){
    editPage.style.display='none'
     all.style.filter =''
     document.body.style.overflow=''


}




function showEditForm(){
    editForm.classList.remove('hidden')
    editForm.classList.add('shown')
    editPage.style.filer
}

function hideEditForm(){
    editForm.classList.remove('shown')
    editForm.classList.add('hidden')
    editPage.style.filter = ''
    imgForm.style.display = 'none'
}


function edit(){
    if(userInput.value == ""){
        userInput.value = username.textContent
    }

    if(bioField.value == ""){
        bioField.value = bio.textContent
    }
    
    
    username.textContent =inputForm.value ; 
    localisation.textContent = country.textContent +', ' + wilaya.options[wilaya.selectedIndex].textContent;
    // bioField = bio
    hideEditForm()

    
}

function showImgForm(){
    
    if(imgForm.classList.contains('hidden')){
        imgForm.classList.remove('hidden')
        imgForm.classList.add('shown')
    }

    else{
        hideImgForm()
    }

    
}

function hideImgForm(){
    imgForm.style.display='none'
}

function enableEditBio(){
bio.removeAttribute('readonly')
}

function saveEdit(){
    usernameSaved.textContent = inputForm.value
    localisationSaved.textContent = country.textContent +', ' + wilaya.options[wilaya.selectedIndex].textContent;
    bioField.textContent = bio.textContent


    hideEdit()
}

const listStats = document.querySelector('.clickable')

document.querySelectorAll('.clickable').forEach(listStats => {
  listStats.addEventListener('click', () => {
    // Enlève la classe active des autres
    document.querySelectorAll('.clickable').forEach(s => s.classList.remove('active'));

    // Ajoute l'animation de soulignement avec radius
    listStats.classList.add('active');
  });
});




// const prevButton = document.querySelector('.prev');
// const nextButton = document.querySelector('.next');
// const carousel = document.querySelector('.carousel');
// let currentIndex = 0;

// function showSlide(index) {
//   const totalItems = carousel.children.length;
  
//   if (index >= totalItems) {
//     currentIndex = 0; // Revenir au premier élément
//   } else if (index < 0) {
//     currentIndex = totalItems - 1; // Revenir au dernier élément
//   }

//   // Appliquer la transformation pour déplacer le carousel avec une animation
//   carousel.style.transform = `translateX(-${currentIndex * 100}%)`;
// }

// prevButton.addEventListener('click', () => {
//   currentIndex--;
//   showSlide(currentIndex);
// });

// nextButton.addEventListener('click', () => {
//   currentIndex++;
//   showSlide(currentIndex);
// });

// // Initialisation du premier slide
// showSlide(currentIndex);


const track = document.getElementById("carouselTrack");
    const prevBtn = document.getElementById("prevBtn");
    const nextBtn = document.getElementById("nextBtn");
    const totalItems = document.querySelectorAll(".carousel-item").length;
    const itemsPerPage = 3;
    const maxIndex = Math.ceil(totalItems / itemsPerPage) - 1;

    let currentIndex = 0;

    function updateCarousel() {
      const offset = -(100 / itemsPerPage) * itemsPerPage * currentIndex;
      track.style.transform = `translateX(${offset}%)`;
      prevBtn.disabled = currentIndex === 0;
      nextBtn.disabled = currentIndex >= maxIndex;
    }

    function next() {
      if (currentIndex < maxIndex) {
        currentIndex++;
        updateCarousel();
      }
    }

    function prev() {
      if (currentIndex > 0) {
        currentIndex--;
        updateCarousel();
      }
    }

    updateCarousel(); // init



//basculement de page

// function showPage(id) {
//   document.querySelectorAll('.page').forEach(page => {
//     if (page.id === id) {
//       page.classList.add('yes');
//     } else {
//       page.classList.remove('yes');
//     }
//   });
// }


function showCC(){
    document.querySelector('.course-and-certifications').style.display = 'block'
    document.querySelector('.summary-page').style.display = 'none'
    document.querySelector('.jobs-page').style.display = 'none'
    document.querySelector('.skills-page').style.display = 'none'
}


function showSS(){
    document.querySelector('.course-and-certifications').style.display = 'none'
    document.querySelector('.summary-page').style.display = 'block'
    document.querySelector('.jobs-page').style.display = 'none'
    document.querySelector('.skills-page').style.display = 'none'
}


function showJS(){
     document.querySelector('.course-and-certifications').style.display = 'none'
    document.querySelector('.summary-page').style.display = 'none'
    document.querySelector('.jobs-page').style.display = 'block'
    document.querySelector('.skills-page').style.display = 'none'
}














// ----------------------------Add courses----------------------

function createSection(){
    const sectionInput = document.getElementById('creeSection')
    const section = document.getElementById('section')

    if(sectionInput.value === ''){
        sectionInput = ''
    }

    section.innerHTML += `
    <option value="dzqdz">${sectionInput.value}</option>
    
    `
    
}





const addCourseBtn = document.getElementById("showPageBtn");
const hiddenPage = document.getElementById("hiddenPage");
const closeBtn = document.querySelector('.close')

addCourseBtn.addEventListener("click", () => {
  hiddenPage.classList.add("active");
  hiddenPage.style.minHeight ='1700px';

//   document.body.style.overflow = 'hidden'
});

closeBtn.addEventListener("click" , ()=>{
    hiddenPage.classList.remove("active");
  hiddenPage.style.minHeight ='0';
})


window.onload = () => {
  const values = document.querySelectorAll(".progression-value");
  const bars = document.querySelectorAll(".progression-bar");

  values.forEach((val, index) => {
    const percent = val.textContent.trim();
    if (bars[index]) {
      bars[index].style.width = percent;
    }
  });

  const values1 = document.querySelectorAll(".l-progression-value");
  const bars1 = document.querySelectorAll(".l-progression-bar");

  values1.forEach((val1, index1) => {
    const percent = val1.textContent.trim();
    if (bars1[index1]) {
      bars1[index1].style.width = percent;
    }
  });
};



