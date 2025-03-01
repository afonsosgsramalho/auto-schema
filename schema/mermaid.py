from diagram import Diagram, Class, Relationship
from parser import read_json, read_output
from model import call_api


def force_diagram():
    pass

def update_diagram():
    pass


def main():
    content = read_json('schema/example.json')
    response = call_api(content)
    response_parsed = read_output(response)

    diagram = Diagram()

    # Create classes
    for table in content:
        diagram.add_class(Class(table, content[table]))
    
    # Create relationships
    for table in response_parsed:
        table1, table2 = table.split('-')
        diagram.add_relationship(Relationship(table1, table2, '||--o{', response_parsed[table][0][0]))
        

    return diagram


if __name__ == '__main__':
    print(main())