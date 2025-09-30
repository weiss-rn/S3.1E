// The original used document.write(...).repeat(5) which doesn't repeat document.write calls.
// To preserve intent, write the string 5 times.
for (let i = 0; i < 5; i++) {
    document.write("Ulangi kalimat ini sebanyak 5 kali.<br/>");
}
