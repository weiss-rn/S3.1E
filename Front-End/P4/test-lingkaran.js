<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
    <script type="module">
        import { luasLingkaran, kelilingLingkaran } from "./lingkaran.js";

        let radius = prompt ("Masukkan panjang radius lingkaran");
        let luas = luasLingkaran(radius);
        let keliling = kelilingLingkaran(radius);

        alert('luas : $(luas) | Keliling : $(keliling)');
    </script>
</body>
</html>