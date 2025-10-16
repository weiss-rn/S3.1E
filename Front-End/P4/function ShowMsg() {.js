function ShowMsg() {
    alert("Hello World");
}

const ShowMsg2 = () => {
    alert("Hello World");
}

ShowMsg();
ShowMsg2();

const penjumlahan = (a, b) => {
    return a + b;
}

const halo = nama => 'Halo ${nama}!';
const penjumlahan2 = (a, b) => a + b;
const luasLingkaran = radius => {
    const phi = 3.14;
    return phi * radius ** 2;
}

const showResult = (hasil) => alert('hasil = ${hasil}');
const penjumlahan3 = (a,b,display) => {
    let hasil = a + b;
    display(hasil);
}

penjumlahan3(1,2,showResult);
penjumlahan3(2,3,(hasil) => alert('hasil = ${hasil}'));

const penjumlahan4 = (a,b) => a + b;
let hasil = penjumlahan4(1,2);
alert('Hasil = ${hasil}');

function resultAll (...values) {
    let total = 0;
    for (const value of values) {
        total += value;
    }
    return total;
}

let result1 = addEverything(1,2,3,4,5);
let result2 = addEverything(7,8,9);
alert('Hasil = ${result1}');