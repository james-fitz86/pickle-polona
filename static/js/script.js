const navButton = document.querySelector(".navbar-toggler");
const navBar = document.getElementById("navbarNav");

navButton.addEventListener("click", function(){
  navBar.classList.toggle("show");
});