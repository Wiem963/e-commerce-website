let search = document.querySelector('.search-box');

document.querySelector('#search-icon').onclick = () => {
    search.classList.toggle('active');
    menu.classList.toggle('active');
}
let menu = document.querySelector('.navbar');

document.querySelector('#menu-icon').onclick = () => {
    menu.classList.toggle('active');
}

let header = document.querySelector('header');

window.addEventListener('scroll',()=>{
    header.classList.toggle('shadow',window.scrollY>0);
});