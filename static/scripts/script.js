// showing navbar when click menu on mobile view
const mobile = document.querySelector('.menu-toggle')
const mobileLink = document.querySelector('.sidebar')

mobile.addEventListener("click", function(){
    mobile.classList.toggle("is-active");
    mobileLink.classList.toggle("active");
});

// close menu when click
mobileLink.addEventListener("click", function(){
    const menuBars = document.querySelector("is-active")
    if(window.innerWidth<=786 && menuBars){
        mobile.classList.toggle("is-active");
        mobileLink.classList.toggle("active");
    }
})

