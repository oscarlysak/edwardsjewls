$(document).ready(function() {
    // Open cart dropdown
    $('.w-commerce-commercecartopenlink').on('click', function(event) {
        event.preventDefault();
        $('.cart-dropdown').toggleClass('open');
    });

    // Close cart dropdown
    $('.close-cart').on('click', function(event) {
        event.preventDefault();
        $('.cart-dropdown').removeClass('open');
    });

    // Close cart dropdown when clicking outside of it
    $(document).on('click', function(event) {
        if (!$(event.target).closest('.navbasket').length) {
            $('.cart-dropdown').removeClass('open');
        }
    });
});
