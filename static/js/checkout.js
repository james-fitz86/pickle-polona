function displayCartItems() {
    const container = document.getElementById("cart-items-container");
    const cart = JSON.parse(localStorage.getItem("cart")) || [];

    if (cart.length === 0) {
        container.innerHTML = "";
        return;
    }

    container.innerHTML = "";

    cart.forEach(item => {
            const row = document.createElement("tr");

            const subtotal = item.price * item.quantity

            row.innerHTML = `
                    <td>${item.name}</td>
                    <td>€${item.price}</td>
                    <td>${item.quantity}</td>
                    <td>€<span class="subtotal">${(subtotal).toFixed(2)}</span></td>
            `;

            container.appendChild(row);
    });
    calculateTotal();
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