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
    } else {
        cart.push({sku, name, quantity, image});
    }

    localStorage.setItem("cart", JSON.stringify(cart));
    updateCartBadge();
    
}

const addToCartButton = document.querySelector('.add-to-cart-btn');

addToCartButton.addEventListener('click', addToCart);

document.querySelectorAll('.quantity-input').forEach(input => {
    input.addEventListener('blur', () => {
        const max = parseInt(input.getAttribute('max'), 10);
        const min = parseInt(input.getAttribute('min'), 10);
        let value = parseInt(input.value, 10);

        if (isNaN(value) || value < min) {
            value = min;
        } else if (value > max) {
            value = max;
        }

        input.value = value;
    });
});