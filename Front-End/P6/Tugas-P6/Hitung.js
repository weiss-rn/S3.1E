// Note: Ensure that xml_grabber_script.js is included in your HTML file (e.g., Tugas.html) to load the XML data.

const form = document.querySelector('form');

function calculateShipping(event) {
    // Prevent form submission if event provided
    if (event) event.preventDefault();

    // Retrieve form values
    var weight = parseFloat(document.getElementById('berat-barang').value);
    var kotaAsal = document.getElementById('kota-asal').value;
    var kotaTujuan = document.getElementById('kota-tujuan').value;

    // Input validation
    if (isNaN(weight) || weight <= 0) {
        alert('Please enter a valid weight');
        return;
    }

    // Base rate per weight unit
    var rate = 10000;
    var cost = weight * rate;

    // If both cities are selected and they differ, add a fixed surcharge
    if (kotaAsal !== '' && kotaTujuan !== '' && kotaAsal !== kotaTujuan) {
        cost += 5000;
    }

    // Update the total field
    document.getElementById('total').value = cost;
    return cost;
}

if(form) {
    form.addEventListener('submit', calculateShipping);
}