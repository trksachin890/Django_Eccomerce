from django import template

register=template.Library()

@register.filter(name='is_in_cart')
def is_in_cart(product,cart):
    keys=(cart.keys())

    for id in keys:
        # Check if id is 'null' or an empty string before converting to int
        if id and id != 'null' and int(id) == product.product_id:
            return True

    return False



@register.filter(name='cart_quantity')
def is_in_cart(product,cart):
    keys=(cart.keys())

    for id in keys:
        # Check if id is 'null' or an empty string before converting to int
        if id and id != 'null' and int(id) == product.product_id:
            return cart.get(id)

    return 0








