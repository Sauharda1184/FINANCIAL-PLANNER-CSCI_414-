// JavaScript to enhance interactivity

// Example: Add confirmation for delete actions
document.addEventListener('DOMContentLoaded', () => {
    const deleteButtons = document.querySelectorAll('.delete-btn');
    deleteButtons.forEach(button => {
        button.addEventListener('click', (event) => {
            if (!confirm('Are you sure you want to delete this item?')) {
                event.preventDefault();
            }
        });
    });
});

// Example: Add dynamic budget total calculations
function calculateTotal() {
    const amounts = document.querySelectorAll('.amount');
    let total = 0;
    amounts.forEach(amount => {
        total += parseFloat(amount.textContent) || 0;
    });
    document.getElementById('total').textContent = total.toFixed(2);
}
