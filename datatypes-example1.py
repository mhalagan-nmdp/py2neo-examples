""" docstring for module """


import argparse  # for command line arguments
from py2neo import *



def main():
    """This is run if file is directly executed, but not if imported as 

    function for testing"""

    # Node(*labels, **properties)
    a  = Node("Person", name="Alice")
    b  = Node("Person", name="Bob", age=75)
    c  = Node("Person", name="John",age=55,location="MN")
    
    b_labels     = b.labels() # Get the node labels
    b_properties = len(b)     # Get the number of properties
    b_dict       = dict(b)    # Turn node into a dictionary
    b_age        = b['age']
    b_name       = b['name']
    b_haslabel   = b.has_label("Person")
    
    print(" -- Nodes -- ")
    print("Node:                 ",b)
    print("Node dictionary:      ",b_dict)
    print("Node labels:          ",b_labels)
    print("Number of properties: ",b_properties)
    print("Has label of Person:  ",b_haslabel)
    print("Person age:           ",b_age)
    print("Person name:          ",b_name)


    #  Relationship(start_node, type, end_node, **properties)
    #  Relationship(start_node, end_node, **properties)
    #  Relationship(node, type, **properties)
    #  Relationship(node, **properties)
    ab       = Relationship(a, "KNOWS", b, years=50)
    cb       = Relationship(b, "KNOWS", c)
    cb_type  = cb.type()
    dict_rel = dict(cb)
    
    print()
    print(" -- Relationships -- ")
    print("Relationship: ",cb)
    print("Relationship Type: ",cb_type)
    
    # Subgraph(nodes, relationships)
    # Union         -> subgraph | other | ...
    # Intersection  -> subgraph & other & ...
    # Difference    -> subgraph - other - ...
    # Symmetric difference  -> subgraph ^ other ^ ...
    s = ab | cb
    sub_nodes = s.nodes()
    sub_relations = s.relationships()
    
    print()
    print(" -- Subgraphs -- ")
    print("Subgraph: ",s)
    print("Subgraph nodes: ",sub_nodes)
    print("Subgraph relationships: ",sub_relations)
    
    # Walkables
    # Walkable(iterable)
    ac = Relationship(a, "KNOWS", c)
    w  = ab + Relationship(b, "LIKES", c) + ac

    print()
    print(" -- Walkables -- ")
    for n in walk(w):
        print("Node: ",n)
        print("Relationships: ",n.relationships())
        

if __name__ == '__main__':
    """The following will be run if file is executed directly, 
    but not if imported as a module"""
    main()
