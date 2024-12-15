function generateQR() {
    document.getElementById('qr-form').style.display = 'block';
}

function generate() {
    var numStudents = document.getElementById('numStudents').value;
    if (numStudents) {
        alert(`Generating QR codes for ${numStudents} students...`);
        window.location.href = `generate_qr?num_students=${numStudents}`;
    } else {
        alert('Please enter the number of students.');
    }
}

function scanQR() {
    alert('Scanning QR codes...');
    window.location.href = 'scan_qr';
}
