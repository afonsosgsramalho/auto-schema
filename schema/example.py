# Tables metadata
table_order = {
    'order': [
        ['string', 'id'],
        ['string', 'customer_id'],
        ['string', 'date'],
        ['string', 'status'],
    ]
}

table_order_item = {
    'order_item': [
        ['string', 'id'],
        ['string', 'order_id'],
        ['string', 'product_id'],
        ['string', 'quantity'],
        ['string', 'price'],
    ]
}

table_product = {
    'product': [
        ['string', 'id'],
        ['string', 'name'],
        ['string', 'description'],
        ['string', 'price'],
    ]
}

table_category = {
    'category': [
        ['string', 'id'],
        ['string', 'name'],
    ]
}

table_product_category = {
    'product_category': [
        ['string', 'product_id'],
        ['string', 'category_id'],
    ]
}

table_payment = {
    'payment': [
        ['string', 'id'],
        ['string', 'order_id'],
        ['string', 'amount'],
        ['string', 'method'],
        ['string', 'date'],
    ]
}

table_shipping = {
    'shipping': [
        ['string', 'id'],
        ['string', 'order_id'],
        ['string', 'address'],
        ['string', 'status'],
        ['string', 'date'],
    ]
}

table_review = {
    'review': [
        ['string', 'id'],
        ['string', 'customer_id'],
        ['string', 'product_id'],
        ['string', 'rating'],
        ['string', 'comment'],
        ['string', 'date'],
    ]
}

table_employee = {
    'employee': [
        ['string', 'id'],
        ['string', 'name'],
        ['string', 'position'],
        ['string', 'salary'],
    ]
}

table_employee_assignment = {
    'employee_assignment': [
        ['string', 'id'],
        ['string', 'employee_id'],
        ['string', 'order_id'],
        ['string', 'task'],
        ['string', 'date'],
    ]
}

tables = [
    table_order, 
    table_order_item, 
    table_product, 
    table_category, 
    table_product_category,
    table_payment,
    table_shipping,
    table_review,
    table_employee,
    table_employee_assignment
]