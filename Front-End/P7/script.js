const tombolBuka = document.getElementById("tombolBuka");
const tombolTutup = document.getElementById("tomboltutup");
const modalOverlay = document.getElementById("modalOverlay");

tombolBuka.addEventListener("click", () => {
    modalOverlay.classList.add("pop-shown");
});

tombolTutup.addEventListener("click", () => {
    modalOverlay.classList.remove("pop-shown");
});

modalOverlay.addEventListener("click", (e) => {
    if (e.target === modalOverlay) {
        modalOverlay.classList.remove("pop-shown");
    }
});