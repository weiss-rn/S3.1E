$(function() {
    const formatRupiah = (value) => value.toLocaleString("id-ID");

    const $slider = $("#priceSlider");
    const $minLabel = $("#priceLabelMin");
    const $maxLabel = $("#priceLabelMax");
    const $productGrid = $("#productGrid");

    const filterProducts = (range) => {
        $(".product-card").each(function() {
            const price = Number($(this).data("price"));
            $(this).toggle(price >= range[0] && price <= range[1]);
        });
    };

    if ($slider.length) {
        const prices = $(".product-card").map((_, el) => Number($(el).data("price")) || 0).get();

        if (prices.length) {
            const minFromData = Number($slider.data("min"));
            const maxFromData = Number($slider.data("max"));
            const minPrice = isFinite(minFromData) && minFromData > 0 ? minFromData : Math.min(...prices);
            const maxPrice = isFinite(maxFromData) && maxFromData > 0 ? maxFromData : Math.max(...prices);

            const sliderMin = Math.max(Math.floor(minPrice / 5000) * 5000, 0);
            const sliderMax = Math.ceil(maxPrice / 5000) * 5000 || 100000;
            const safeMax = sliderMax > sliderMin ? sliderMax : sliderMin + 5000;
            const defaultRange = [sliderMin, safeMax];

            $slider.slider({
                range: true,
                min: sliderMin,
                max: safeMax,
                step: 5000,
                values: defaultRange,
                slide: (_, ui) => {
                    $minLabel.text(formatRupiah(ui.values[0]));
                    $maxLabel.text(formatRupiah(ui.values[1]));
                    filterProducts(ui.values);
                },
                change: (_, ui) => filterProducts(ui.values)
            });

            $minLabel.text(formatRupiah(defaultRange[0]));
            $maxLabel.text(formatRupiah(defaultRange[1]));
            filterProducts(defaultRange);
        } else {
            $slider.hide();
            $minLabel.text("0");
            $maxLabel.text("0");
        }
    }

    const $cartDialog = $("#cartDialog");
    if ($cartDialog.length) {
        $cartDialog.dialog({
            autoOpen: false,
            modal: true,
            width: 420
        });
    }

    let cartTotal = 0;
    $(".add-to-cart").on("click", function(event) {
        event.preventDefault();
        const $card = $(this).closest(".product-card");
        const name = $(this).data("name") || $card.find(".product-name").text();
        const price = Number($(this).data("price") ?? $card.data("price")) || 0;

        const $itemRow = $("<div/>", { class: "cart-row" })
            .append($("<span/>").text(name))
            .append($("<span/>").text(`Rp ${formatRupiah(price)}`));
        $("#cartItems").append($itemRow);

        cartTotal += price;
        $("#cartTotal").text(formatRupiah(cartTotal));

        if ($cartDialog.length) {
            $cartDialog.dialog("open");
        }
    });
});
