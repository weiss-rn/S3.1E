// Variable
var name = "Javascript";
var visitCount = "200000";
var isActive = true;
var url = "https://example.com";

// Alert
alert("Welcome to " + name + "!");

// Document Write output - Dapat dilihat di browser
document.write("Welcome to " + name + "!" + "<br>");
document.write("This page total visitor is " + visitCount + "<br>");
document.write("and this page is " + (isActive ? "active" : "inactive" ) + "<br>");
document.write("and this page url is " + url + "<br>");

// Console Log output - Hanya bisa dilihat lewat Debugging lewat browser
console.log("Welcome to " + name + "!");
console.log("This page total visitor is " + visitCount);
console.log("and this page is " + (isActive ? "active" : "inactive" ));
console.log("and this page url is " + url);

// Overwrite Variable - variable diatas akan di overwrite oleh dibawah ini
name = "Javascript-P2";
visitCount = "100000";
isActive = false;
url = "https://example.com";

// Penghapusan variable - variable diatas akan hilang
// delete name;
// delete visitCount;
// delete isActive;
// delete url;

// Dialog Alert
window.alert("Hello, world!");

// Dialog Prompt
var ur_name = prompt("Insert your name","");
document.write("<p>Hello, " + ur_name + "!</p>");

// Prompt
var password = prompt("Enter password:", "");
if (password === "Kucing") {
    alert("Access granted!");
} else {
    alert("Access denied!");
}

// Dialog Confirm
var benar_not = confirm("Are you sure to visit this page?");

if (benar_not) {
    window.location.href = "https://example.com";
    alert("You clicked OK!");
} else {
    alert("You clicked Cancel!");
}
