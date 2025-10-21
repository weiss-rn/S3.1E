function loadCity() {
    fetch("data.xml")
        .then(r => {
            if (!r.ok) throw new Error("Network response was not ok");
            return r.text();
        })
        .then(xmlText => {
            const parser = new DOMParser();
            const xmlDoc = parser.parseFromString(xmlText, "application/xml");
            populateSelect(xmlDoc);
        })
        .catch(err => console.error("Error fetching XML:", err));
}

function populateSelect(xmlDoc) {
    const options = xmlDoc.getElementsByTagName("option");
    const selectAsal = document.getElementById("kota-asal");
    const selectTujuan = document.getElementById("kota-tujuan");

    const clear = sel => {
        while (sel.options.length > 1) sel.remove(1);
    };
    clear(selectAsal);
    clear(selectTujuan);

    for (let i = 0; i < options.length; i++) {
        const opt = options[i];
        const value = opt.getAttribute("value");
        const text = opt.textContent;

        const optAsal = document.createElement("option");
        optAsal.value = value;
        optAsal.text = text;
        selectAsal.add(optAsal);

        const optTujuan = document.createElement("option");
        optTujuan.value = value;
        optTujuan.text = text;
        selectTujuan.add(optTujuan);
    }
}

document.addEventListener("DOMContentLoaded", loadCity);