const navButton = document.querySelector(".navbar-toggler");
const navBar = document.getElementById("navbarNav");

navButton.addEventListener("click", function(){
  navBar.classList.toggle("show");
});

function updateCartBadge() {
    const cart = JSON.parse(localStorage.getItem('cart')) || [];
    const badge = document.getElementById('cart-badge');

    if (!badge) return;

    const itemCount = cart.length;

    if (itemCount > 0) {
        badge.textContent = itemCount;
        badge.classList.remove('d-none');
    } else {
        badge.classList.add('d-none');
    }
}

updateCartBadge();