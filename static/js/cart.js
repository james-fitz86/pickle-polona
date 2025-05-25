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
            col.className = "col-12 col-md-8 col-lg-6 mx-auto";

            col.innerHTML = `
                <div class="card shadow-sm h-100 d-flex flex-row align-items-center p-2" style="margin-bottom: 5px;">
                    <img src="${item.image}" alt="${item.name}" class="rounded me-3" style="width: 100px; height: 100px; object-fit: cover;">
                    <div class="card-body p-2">
                        <h5 class="card-title mb-1">${item.name}</h5>
                        <label class="card-text mb-0">Quantity:
                            <input type="number" class="form-control quantity-input" data-sku="${item.sku}" value="${item.quantity}" min="1" style="width: 80px; display: inline-block; margin-left: 5px;">
                        </label>
                    </div>
                    <button class="btn btn-danger remove-itm-btn" data-sku="${item.sku}">Remove</button>
                </div>
            `;

            container.appendChild(col);
    });
}

function emptyCart(){
    const container = document.getElementById("cart-items-container");

    localStorage.setItem("cart", JSON.stringify([]));
    container.innerHTML = "<p class='text-muted'>Your cart is empty.</p>";
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
    }
});

document.addEventListener('change', function(event) {
    if (event.target.classList.contains('quantity-input')) {
        const sku = event.target.dataset.sku;
        const newQuantity = parseInt(event.target.value);

        if (newQuantity >= 1) {
            let cart = JSON.parse(localStorage.getItem('cart')) || [];
            const item = cart.find(item => item.sku === sku);

            if (item) {
                item.quantity = newQuantity;
                localStorage.setItem('cart', JSON.stringify(cart));
            }
        }
    }
});

