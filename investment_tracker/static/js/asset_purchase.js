function updateTotalCost() {
    const price = parseFloat(document.getElementById('price').textContent);
    const quantity = parseFloat(document.getElementById('quantity').value);
    if (!isNaN(price) && !isNaN(quantity)) {
        document.getElementById('total_cost').value = (price * quantity).toFixed(2);
    }
}

function updateQuantity() {
    const price = parseFloat(document.getElementById('price').textContent);
    const totalCost = parseFloat(document.getElementById('total_cost').value);
    if (!isNaN(price) && !isNaN(totalCost) && price !== 0) {
        document.getElementById('quantity').value = (totalCost / price).toFixed(3);
    }
}