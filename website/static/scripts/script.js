const logoTxt = document.querySelector('.logo-txt')
const navBar = document.querySelector('.nav-bar')

document.addEventListener('scroll',(scroll)=>{
    // console.log(scroll);
    if(document.documentElement.scrollTop>= 100){
setTimeout(()=>{
    logoTxt.style.transform = "translateX(-200px)";
    navBar.style.position = "fixed"
    navBar.style.boxshadow ="-2px -9px 20px #6f6a6a;"
},200)
    }
    else{
        logoTxt.style.transform = "translateX(200px)"
        navBar.style.position = "absolute"
    }



    
})
