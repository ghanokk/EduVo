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


document.getElementById('edit-profile-form').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const username = userInput.value;
    const wilaya = document.getElementById('wilaya').value;
    const bio = bioField.value;

    try {
        // Validate username first
        const isValidUsername = await validateUsername(username);
        if (!isValidUsername) return;

        // Prepare data to send
        const formData = new FormData();
        formData.append('username', username);
        formData.append('wilaya', wilaya);
        formData.append('bio', bio);

        // Send update request
        const response = await fetch('/profile/update-profile/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': document.querySelector('input[name="csrfmiddlewaretoken"]').value
            },
            body: formData
        });
        const data = await response.json();

        if (data.success) {
            // Update the UI
            username.textContent = username;
            localisation.textContent = `Algeria, ${data.wilaya_display}`;
            bioField.textContent = bio;
            hideEditForm();
        } else {
            alert('Error updating profile');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error updating profile');
    }
});

async function saveEdit() {
    const username = document.getElementById('user-input').value;
    const wilaya = document.getElementById('wilaya').value;
    const bio = document.getElementById('biographie-field').value;
    const messageElement = document.getElementById('save-message');

    if (!username.trim()) {
        messageElement.textContent = 'Username cannot be empty';
        messageElement.style.color = 'red';
        return;
    }

    try {
        // Validate username first
        const response = await fetch('/profile/validate-username/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': document.querySelector('input[name="csrfmiddlewaretoken"]').value
            },
            body: new URLSearchParams({
                username: username
            })
        });
        const data = await response.json();

        if (!data.is_valid) {
            messageElement.textContent = data.message;
            messageElement.style.color = 'red';
            return;
        }

        // Prepare data to send
        const formData = new FormData();
        formData.append('username', username);
        formData.append('wilaya', wilaya);
        formData.append('bio', bio);

        // Send update request
        const updateResponse = await fetch('/profile/update-profile/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': document.querySelector('input[name="csrfmiddlewaretoken"]').value
            },
            body: formData
        });
        const updateData = await updateResponse.json();

        if (updateData.success) {
            // Update the UI
            document.getElementById('username-value').textContent = updateData.username;
            document.getElementById('loc').textContent = updateData.wilaya_display;
            document.getElementById('bio-space').textContent = updateData.bio;
            hideEditForm();
            messageElement.textContent = updateData.message;
            messageElement.style.color = 'green';
            setTimeout(() => {
                messageElement.textContent = '';
            }, 3000);
        } else {
            messageElement.textContent = updateData.error || 'Error updating profile';
            messageElement.style.color = 'red';
        }
    } catch (error) {
        console.error('Error:', error);
        messageElement.textContent = 'Error updating profile';
        messageElement.style.color = 'red';
    }
}

// Username validation
async function validateUsername(username) {
    const response = await fetch('/profile/validate-username/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({ username: username })
    });
    const data = await response.json();
    if (data.exists) {
        alert('Username already exists');
        return false;
    }
    return true;
}

// Utility function to get CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function showImgForm(){
    document.querySelector('.add-picture').classList.remove('hidden');
}

// Handle file selection
document.getElementById('fileInput').addEventListener('change', function(e) {
    const file = e.target.files[0];
    if (file) {
        document.getElementById('fileName').textContent = file.name;
        
        // Show file preview
        const previewImg = document.getElementById('preview-img');
        const reader = new FileReader();
        reader.onload = function(e) {
            previewImg.src = e.target.result;
            previewImg.style.display = 'block';
        }
        reader.readAsDataURL(file);
    }
});

function uploadProfilePicture() {
    const file = document.getElementById('fileInput').files[0];
    if (!file) {
        alert('Please select a file first');
        return;
    }

    const formData = new FormData();
    formData.append('profile_picture', file);
    
    fetch('/profile/update-picture/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': document.querySelector('input[name="csrfmiddlewaretoken"]').value
        },
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Update the profile picture in the UI
            document.getElementById('pro-pic').src = data.image_url;
            document.querySelector('.add-picture').classList.add('hidden');
            document.getElementById('preview-img').style.display = 'none';
            document.getElementById('fileName').textContent = 'No file chosen';
        } else {
            alert('Error updating profile picture');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error uploading profile picture');
    });
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

const addJobForm = document.querySelector('.add-job')
function showJobForm(){
  addJobForm.style.display ='block'
}

function closeJobForm(){
  addJobForm.style.display = 'none'
}


const addCourseForm = document.querySelector('.add-course')
function showCourseForm(){
addCourseForm.style.display='block'
}

function closeCourseForm(){
  addCourseForm.style.display='none'
}


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




