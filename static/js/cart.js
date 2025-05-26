function displayCartItems() {
    const container = document.getElementById("cart-items-container");
    const cart = JSON.parse(localStorage.getItem("cart")) || [];

    if (cart.length === 0) {
        container.innerHTML = "<p class='text-muted'>Your cart is empty.</p>";
        return;
    }

    container.innerHTML = "";

    cart.forEach(item => {
            const col = document.createElement("div");

            const subtotal = item.price * item.quantity
            col.className = "col-12 col-md-8 col-lg-6 mx-auto";

            col.innerHTML = `
                <div class="card shadow-sm h-100 d-flex flex-row align-items-center p-2" style="margin-bottom: 5px;">
                    <img src="${item.image}" alt="${item.name}" class="rounded me-3" style="width: 100px; height: 100px; object-fit: cover;">
                    <div class="card-body p-2">
                        <h5 class="card-title mb-1">${item.name}</h5>
                        <label class="card-text mb-0">Quantity:
                            <input type="number" 
                                    class="form-control quantity-input" 
                                    data-sku="${item.sku}" 
                                    data-max-stock="${item.maxStock}"
                                    data-price="${item.price}" 
                                    value="${item.quantity}" 
                                    min="1" 
                                    style="width: 80px; display: inline-block; margin-left: 5px;">
                        </label>
                        <p>Subtotal: €<span class="subtotal">${(subtotal).toFixed(2)}</span></p>
                    </div>
                    <button class="btn btn-danger remove-itm-btn" data-sku="${item.sku}">Remove</button>
                </div>
            `;

            container.appendChild(col);
    });
    applyQuantityBlurListeners();
    calculateTotal();
}

function emptyCart(){
    const container = document.getElementById("cart-items-container");

    localStorage.setItem("cart", JSON.stringify([]));
    container.innerHTML = "<p class='text-muted'>Your cart is empty.</p>";
    calculateTotal();
    return;
    
}

const emptyCartButton = document.querySelector('.empty-cart-btn');

emptyCartButton.addEventListener('click', emptyCart);

document.addEventListener('click', function(event) {
    if (event.target.classList.contains('remove-itm-btn')) {
        const skuToRemove = event.target.dataset.sku;
        
        let cart = JSON.parse(localStorage.getItem("cart")) || [];

        cart = cart.filter(item => item.sku !== skuToRemove);

        localStorage.setItem("cart", JSON.stringify(cart));

        displayCartItems();
        calculateTotal();
    }
});

document.addEventListener('change', function(event) {
    if (event.target.classList.contains('quantity-input')) {
        const input = event.target;
        const sku = event.target.dataset.sku;
        const newQuantity = parseInt(event.target.value);
        const price = parseFloat(input.dataset.price);

        if (newQuantity >= 1) {
            let cart = JSON.parse(localStorage.getItem('cart')) || [];
            const item = cart.find(item => item.sku === sku);

            if (item) {
                item.quantity = newQuantity;
                
                const cardBody = input.closest('.card-body');
                const subtotalSpan = cardBody.querySelector('.subtotal');
                const newSubtotal = (price * newQuantity).toFixed(2);
                subtotalSpan.textContent = newSubtotal;

                calculateTotal();
            }
        }
    }
});

function applyQuantityBlurListeners() {
    document.querySelectorAll('.quantity-input').forEach(input => {
        input.addEventListener('blur', () => {
            const max = parseInt(input.dataset.maxStock, 10);
            const min = parseInt(input.getAttribute('min'), 10);
            let value = parseInt(input.value, 10);

            if (isNaN(value) || value < min) {
                value = min;
            } else if (value > max) {
                value = max;
                alert(`Maximum available stock is ${max}`);
            }

            input.value = value;

            const sku = input.dataset.sku;
            let cart = JSON.parse(localStorage.getItem("cart")) || [];
            const item = cart.find(i => i.sku === sku);
            if (item) {
                item.quantity = value;
                localStorage.setItem("cart", JSON.stringify(cart));
            }
        });
    });
}

function calculateTotal(){
    const subtotals = document.querySelectorAll(".subtotal");
    let total = 0;
    const totalPrice = document.querySelector("#total-price");

    subtotals.forEach(span =>{
        total += parseFloat(span.textContent);
    });
    
    totalPrice.innerText = `Total: €${total.toFixed(2)}`;
}


