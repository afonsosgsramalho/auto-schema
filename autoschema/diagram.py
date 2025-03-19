from typing import List

class Class:
    def __init__(self, name: str, attributes: List[List[str]]):
        self.name = name
        self.attributes = attributes

    def __str__(self):
        self.string = f'{self.name} {{'
        self.string += '\n'

        for attribute in self.attributes:
            self.string += f'   {attribute[0]} {attribute[1]} \n'

        self.string += f'}}'

        return self.string
    

class Relationship:
    def __init__(self, source: str, destination: str, relation: str, connection_key: str):
        self.source = source
        self.destination = destination
        self.relation = relation
        self.connection_key = connection_key

    def __str__(self):
        return f'{self.source} {self.relation} {self.destination} : "{self.connection_key}"'


class Diagram:
    def __init__(self):
        self.classes = []
        self.relationships = []

    def add_class(self, class_obj: Class):
        self.classes.append(class_obj)

    def add_relationship(self, relationship_obj: Relationship):
        self.relationships.append(relationship_obj)

    def force_diagram(self):
        #TODO
        return
    
    def update_diagram(self):
        #TODO
        return

    def __str__(self):
        self.string = f'erDiagram \n\n'

        for class_obj in self.classes:
            self.string += f'{class_obj} \n\n'

        for rel_obj in self.relationships:
            self.string += f'{rel_obj} \n'

        return self.string

