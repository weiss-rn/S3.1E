async function loadHTML(id, file) {
    const element = document.getElementById(id);
    const response = await fetch(file);
    element.innerHTML = await response.text();
    element.innerHTML = html;
}

document.addEventListener("DOMContentLoaded", () => {
    loadHTML("tabel", "tabel.html");
        loadHTML("inject-tabel", "tabel.html");
});