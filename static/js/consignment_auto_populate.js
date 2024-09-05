// static/js/consignment_auto_populate.js
document.addEventListener('DOMContentLoaded', function() {
    function updateFields(consignmentId) {
        if (consignmentId) {
            fetch(`/admin/kenetassets/consignment/${consignmentId}/details/`)
                .then(response => response.json())
                .then(data => {
                    document.getElementById('id_name').value = data.supplier || '';
                    document.getElementById('id_model').value = data.invoice_number || '';
                    document.getElementById('id_category').value = data.location || '';
                });
        }
    }

    const consignmentSelect = document.querySelector('.consignment-select');
    if (consignmentSelect) {
        consignmentSelect.addEventListener('change', function() {
            updateFields(this.value);
        });

        // Initialize fields if a consignment is already selected
        const initialConsignmentId = consignmentSelect.value;
        if (initialConsignmentId) {
            updateFields(initialConsignmentId);
        }
    }
});
