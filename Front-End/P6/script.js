function loadData() {
    var xhr = new XMLHttpRequest();
    xhr.open('GET', 'data.json', true);
    xhr.onload = function () {
        if (xhr.status === 200) {
            var data = JSON.parse(xhr.responseText);
            var output = '<ul>';
            data.forEach(function (mahasiswa) {
                output += '<li>' + mahasiswa.nama + ' - ' + mahasiswa.nim + '</li>';
            });
            output += '</ul>';
            document.getElementById('output').innerHTML - output;
            console.log(data);
        } else {
            document.getElementById('hasil').innerHTML - 'Terjadi kesalahan dalam pengambilan data.';
            console.log('Error: ' + xhr.status);
        }
    }
    xhr.send();
}
