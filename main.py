
# dictionary with product info
products = {
    'Product_A': 20,
    'Product_B': 40,
    'Product_C': 50
}

# dictionary to hold cart details
cart = {}

# dictionary to hold the discount details
choose_discount = {}

# Prompt the user for the quantity of each product needed and if it is a gift
prod_a_quant = int(input("Quantity of Product A needed? "))
prod_a_wrap = input("Should the product be wrapped as a gift?  yes / no (Gift wrap = 1$) ")
prod_b_quant = int(input("Quantity of Product B needed? "))
prod_b_wrap = input("Should the product be wrapped as a gift?  yes / no (Gift wrap = 1$) ")
prod_c_quant = int(input("Quantity of Product C needed? "))
prod_c_wrap = input("Should the product be wrapped as a gift?  yes / no (Gift wrap = 1$) ")


def update_cart(cart, products, product, prod_quant, prod_wrap):
    """ function takes the products and the input from the user and updates the cart dictionary"""
    cart.update({product: {
        'quantity': prod_quant,
        'price': products.get(product) * prod_quant,
        'gift': prod_wrap
    }})


# Updating the cart with products
update_cart(cart, products, 'Product_A', prod_a_quant, prod_a_wrap)
update_cart(cart, products, 'Product_B', prod_b_quant, prod_b_wrap)
update_cart(cart, products, 'Product_C', prod_c_quant, prod_c_wrap)

# Calculate total cart items
total_quantity = 0
for key, value in cart.items():
    if value and 'quantity' in value.keys():
        total_quantity += value['quantity']

# Calculate subtotal(total without discount or extra fees)
sub_total = 0
for key, value in cart.items():
    if value and 'price' in value.keys():
        sub_total += value['price']

gift_wrap_amount = 0
for key, value in cart.items():
    if value and 'quantity' in value.keys():
        if value and 'gift' in value.keys():
            if value['gift'] == 'yes':
                gift_wrap_amount += value['quantity'] * 1


def flat_10_discount(sub_total):
    """ apply the 10$ discount and add the discount to the choose_discount dict """
    if sub_total > 200:
        discount = 10
        choose_discount.update({'flat_10_discount': discount})


def bulk_5_discount(cart):
    """ apply the bulk 5% discount and add the discount to the choose_discount dict """
    discount = 0
    for key, value in cart.items():
        if value and 'quantity' in value.keys():
            if value['quantity'] > 10:
                discount = value['price'] * .05
    if discount != 0:
        choose_discount.update({'bulk_5_discount': discount})


def bulk_10_discount(sub_total, total_quantity):
    """ apply the bulk 10% discount and add the discount to the choose_discount dict """
    if total_quantity > 20:
        discount = sub_total * .10
        choose_discount.update({'bulk_10_discount': discount})


def tiered_50_discount(total_quantity, cart, products):
    """ apply the tiered 50% discount and add the discount to the choose_discount dict """
    discount = 0
    if total_quantity > 30:
        for key, value in cart.items():
            if value and 'quantity' in value.keys():
                if value['quantity'] > 15:
                    # print(key)
                    units_for_discount = value['quantity'] - 15
                    price_for_units = products[key]
                    # print(price_for_units)
                    discount += (units_for_discount * price_for_units) // 2
    if discount != 0:
        choose_discount.update({'tiered_50_discount': discount})


# calling the discount functions
flat_10_discount(sub_total)
bulk_5_discount(cart)
bulk_10_discount(sub_total, total_quantity)
tiered_50_discount(total_quantity, cart, products)

# calculate shipping fee ( 5$ per package, 1 package = 10 units)
shipping_fee = 0
if total_quantity % 10 != 0:
    total_packages = total_quantity // 10 + 1
    shipping_fee = total_packages * 5
else:
    total_packages = total_quantity // 10
    shipping_fee = total_packages * 5


def find_discount(choose_discount):
    """ Function to find the best discount for the user form the choose_discount dict"""
    selected_discount = max(choose_discount, key=lambda x: choose_discount[x])
    return selected_discount


discount = ""
if len(choose_discount) != 0:
    discount = find_discount(choose_discount)

if discount:
    total = ((sub_total - choose_discount[discount])+shipping_fee+gift_wrap_amount)
else:
    total = sub_total + shipping_fee + gift_wrap_amount


# Printing the output
print('\n--------CART---------\n')
print(f"Total Items\t\t\t:\t{total_quantity}")
print("-"*30)
for key,value in cart.items():
    print(f"{key}\tX\t{value['quantity']}\t:\t{value['price']}$")
print("-"*30)
print(f"SubTotal\t\t\t:\t{sub_total}$")
print("-"*30)
if discount:
    print(f"{discount}\t:\t-{choose_discount[discount]}$")
print(f"Shipping Fee\t\t:\t{shipping_fee}$")
print(f"Gift wrap fee\t\t:\t{gift_wrap_amount}$")
print("-"*30)
print(f"Total\t\t\t\t:\t{total}$")


'''Sample Output'''

"""
Quantity of Product A needed? 10
Should the product be wrapped as a gift?  yes / no (Gift wrap = 1$) yes
Quantity of Product B needed? 5
Should the product be wrapped as a gift?  yes / no (Gift wrap = 1$) no
Quantity of Product C needed? 16
Should the product be wrapped as a gift?  yes / no (Gift wrap = 1$) no

--------CART---------

Total Items			:	31
------------------------------
Product_A	X	10	:	200$
Product_B	X	5	:	200$
Product_C	X	16	:	800$
------------------------------
SubTotal			:	1200$
------------------------------
bulk_10_discount	:	-120.0$
Shipping Fee		:	20$
Gift wrap fee		:	10$
------------------------------
Total				:	1110.0$
"""
