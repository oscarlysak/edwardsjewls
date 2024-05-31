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

    // Add to cart functionality
    $('.product-frame').on('click', '.addtocart', function(event) {
        event.preventDefault();
        var productId = $(this).closest('.product-frame').data('product-id');
        var csrfToken = '{{ csrf_token }}';

        $.ajax({
            url: '{% url "add_to_cart" %}',
            method: 'POST',
            data: {
                'product_id': productId,
                'quantity': 1,
                'csrfmiddlewaretoken': csrfToken
            },
            success: function(data) {
                $('.cart-quantity').text(data.cart_quantity);
                $('.cart-body p').text('Subtotal: £' + data.cart_subtotal);
                updateCartContents();
            },
            error: function() {
                alert('An error occurred while adding the product to the cart.');
            }
        });
    });

    // Function to update cart contents
    function updateCartContents() {
        $.ajax({
            url: '{% url "cart_contents" %}',
            method: 'GET',
            success: function(data) {
                var cartBody = $('.cart-body');
                cartBody.empty();
                cartBody.append('<p>Subtotal: £' + data.cart_subtotal + '</p>');
                $.each(data.cart_items, function(index, item) {
                    cartBody.append('<div class="cart-item">' +
                        '<p>' + item.product_name + ' - ' + item.quantity + ' x £' + item.product_price + '</p>' +
                        '</div>');
                });
                cartBody.append('<button class="apple-pay-button">Apple Pay</button>');
                cartBody.append('<a href="{% url "checkout" %}" class="checkout-button">Continue to Checkout</a>');
            },
            error: function() {
                alert('An error occurred while fetching the cart contents.');
            }
        });
    }
});
