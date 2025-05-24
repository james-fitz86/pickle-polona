if (!localStorage.getItem("cart")) {
    localStorage.setItem("cart", JSON.stringify([]));
}

function addToCart(){
    const input = document.querySelector(".quantity-input");
    const quantity = parseInt(input.value);
    const sku = input.dataset.productSku;
    const name = input.dataset.productName
    const image = input.dataset.productImage
    let cart = JSON.parse(localStorage.getItem("cart")) || [];

    const existingItem = cart.find(item => item.sku === sku);
    
    if (existingItem){
        existingItem.quantity = (parseInt(existingItem.quantity)) + quantity;
        console.log(`Quanity of ${name} has been updated`);
    } else {
        cart.push({sku, name, quantity, image});
        console.log(`${quantity} of ${name} added to cart`);
    }

    localStorage.setItem("cart", JSON.stringify(cart));
    
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