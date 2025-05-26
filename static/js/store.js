if (!localStorage.getItem("cart")) {
    localStorage.setItem("cart", JSON.stringify([]));
}

function addToCart(){
    const input = document.querySelector(".quantity-input");
    const quantity = parseInt(input.value);
    const sku = input.dataset.productSku;
    const price = parseFloat(input.dataset.price);
    const name = input.dataset.productName
    const image = input.dataset.productImage
    const maxStock = parseInt(input.dataset.maxStock)
    const subtotal = price * quantity
    let cart = JSON.parse(localStorage.getItem("cart")) || [];

    const existingItem = cart.find(item => item.sku === sku);
    const currentQuantity = existingItem ? parseInt(existingItem.quantity) : 0;

    if (currentQuantity + quantity > maxStock) {
        alert(`Max quantity of ${name} is ${maxStock}`);
        return;
    }
    
    if (existingItem){
        existingItem.quantity = (parseInt(existingItem.quantity)) + quantity;
    } else {
        cart.push({sku, name, quantity, image, maxStock, price, subtotal});
        console.log(price);
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