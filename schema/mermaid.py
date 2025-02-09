from diagram import Diagram, Class, Relationship


def force_diagram():
    pass

def update_diagram():
    pass

def main():
    title = 'teste'
    # Create some classes
    class_customer = Class("Customer", [["id", "int"], ["name", "str"]])
    class_product = Class("Product", [["id", "int"], ["name", "str"], ["price", "float"]])
    class_order = Class("Order", [["id", "int"], ["order_date", "date"]])

    # Create some relationships
    relationship1 = Relationship("Customer", "Order", "||--o{", "customer_id")
    relationship2 = Relationship("Product", "Order", "||--o{", "product_id")

    # Create a diagram
    diagram = Diagram()

    # Add classes and relationships to the diagram
    diagram.add_class(class_customer)
    diagram.add_class(class_product)
    diagram.add_class(class_order)

    diagram.add_relationship(relationship1)
    diagram.add_relationship(relationship2)

    # Print the diagram
    return diagram

if __name__ == '__main__':
    print(main())