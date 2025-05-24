if (!localStorage.getItem("cart")) {
    localStorage.setItem("cart", JSON.stringify([]));
}

function addToCart(){
    const input = document.querySelector(".quantity-input");
    const quantity = input.value;
    const sku = input.dataset.productSku;
    cart = JSON.parse(localStorage.getItem("cart")) || [];

    
    cart.push({sku, quantity});

    localStorage.setItem("cart", JSON.stringify(cart));

    console.log(`${quantity} of ${sku} added to cart`)
}

function seeCart(){
    cart = JSON.parse(localStorage.getItem("cart"));
    console.log(cart);

}

function emptyCart(){
    localStorage.setItem("cart", JSON.stringify([]));
}
const addToCartButton = document.querySelector('.add-to-cart-btn');

addToCartButton.addEventListener('click', addToCart);