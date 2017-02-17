""" docstring for module """


import argparse  # for command line arguments
import pandas as pa
from py2neo import *



def main():
    """This is run if file is directly executed, but not if imported as 

    function for testing"""

    # Create a new neo4j graph object with py2neo
    graph   = Graph("http://localhost:7474/data/",user="neo4j",password="new")
    
    # Person nodes
    a  = Node("Person", name="Alice",born=1953,state="MN",job="Wrestler")
    b  = Node("Person", name="Bob", born=1955,state="MN",job="Doctor")
    c  = Node("Person", name="John",born=1960,state="TN",job="Doctor")
    d  = Node("Person", name="Tom",born=1990,state="MN",job="Graduate Student")
    e  = Node("Person", name="Jack",born=1991,state="MI",job="Graduate Student")

    # Movie nodes
    # Can property be an array ?
    # CREATE (gdb:Movie { title: 'Back to the Future',
    #               authors: ['Ian Robinson', 'Jim Webber'] })
    m1  = Node("Movie",title="Back to the Future")
    m2  = Node("Movie",title="Jaws")
    m3  = Node("Movie",title="Home Alone")
    m4  = Node("Movie",title="Lion King")

    am1       = Relationship(a, "WATCHED", m1, stars=3)
    am2       = Relationship(a, "WATCHED", m2, stars=3)
    am3       = Relationship(a, "WATCHED", m3, stars=5)
    bm4       = Relationship(b, "WATCHED", m4, stars=5)
    cm4       = Relationship(c, "WATCHED", m4, stars=5)
    em4       = Relationship(e, "WATCHED", m4, stars=5)
    dm4       = Relationship(d, "WATCHED", m4, stars=5)
    cm1       = Relationship(c, "WATCHED", m1, stars=4)

    ab       = Relationship(a, "KNOWS", b, years=20)    
    ac       = Relationship(a, "KNOWS", c, years=30)
    ca       = Relationship(a, "KNOWS", c, years=30)
    ad       = Relationship(a, "KNOWS", d, years=27)
    cb       = Relationship(c, "KNOWS", b, years=8)
    bc       = Relationship(b, "KNOWS", c, years=8)
    cd       = Relationship(c, "KNOWS", d, years=27)
    dc       = Relationship(d, "KNOWS", c, years=27)
    ce       = Relationship(c, "KNOWS", e, years=27)
    ec       = Relationship(c, "KNOWS", e, years=27)
    de       = Relationship(d, "KNOWS", e, years=2)
    ed       = Relationship(e, "KNOWS", d, years=2)
    
    tx = graph.begin()
    relationships = [ab, ac, ca, ad, cb, bc, cd, dc, ce, ec, de, ed, am1, am2, am3, bm4, cm4, em4, dm4, cm1]
    for rel in relationships:
        tx.merge(rel)
    
    tx.commit()

    # * Match function *
    print("- Match function -")
    for rel in graph.match(start_node=c, rel_type="KNOWS"):
        print(a["name"]," knows ",rel.end_node()["name"])
    
    print()
    print("- NodeSelector -")
    selector    = NodeSelector(graph)
    mn_people   = selector.select("Person", state="MN")
    
    for node in mn_people:
        print(node['name']," lives in MN")
    
    m_age      = selector.select("Person").where("_.state =~ 'M.*'", "1960 <= _.born > 1950")
    for node in m_age:
        print(node['name']," lives in MI or MN and was born between 1950 and 1960")

    print()
    print("- find -")
    names = ("John","Alice","Bob")
    found_list = [found.properties["job"] for found in graph.find(property_key='name',property_value=names,label="Person")]
    print(found_list)
    
    print()
    print("- data -")
    cypher_query = "MATCH (a:Person)-[r:KNOWS]-(b) return a.name,b.name,r.years"
    years_known  = pa.DataFrame(graph.data(cypher_query))
    print(years_known)
    
    # MATCH  (a:Person)-[r:KNOWS]-(b:Person),(b)-[r2:LIKES]-(movie:Movie)
    # WHERE r.years > 10 
    # AND   NOT    (a)-[:LIKES]->(movie)
    # AND  r2.stars > 4
    # RETURN a.name,b.name,movie.title,r2.stars
    # ORDER BY r2.stars DESC
    print()
    print("- data -")
    cypher_query   = "MATCH  (a:Person)-[r:KNOWS]-(b:Person),(b)-[r2:WATCHED]-(movie:Movie) WHERE r.years > 10 AND   NOT    (a)-[:LIKES]->(movie) AND  r2.stars >= 4 RETURN a.name,b.name,movie.title,r2.stars ORDER BY r2.stars DESC"
    recomendations = pa.DataFrame(graph.data(cypher_query))
    print(recomendations)



if __name__ == '__main__':
    """The following will be run if file is executed directly, 
    but not if imported as a module"""
    main()
