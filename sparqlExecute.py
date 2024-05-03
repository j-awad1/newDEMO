from rdflib import Graph, Namespace
import streamlit as st

class sparqlExecution():
    def execute(self):
        # Load the data from the Subset.ttl file
        g = Graph().parse("Subset.ttl", format="turtle")

        # Define the namespaces
        owl = Namespace("http://www.w3.org/2002/07/owl#")
        rdfs = Namespace("http://www.w3.org/2000/01/rdf-schema#")

        # Execute the SPARQL query
        # query = """
        # PREFIX owl: <http://www.w3.org/2002/07/owl#>
        # PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

#         SELECT ?property ?comment
#         WHERE {
#             ?class rdfs:subClassOf [
#                 rdf:type owl:Restriction ;
#                 owl:onProperty ?property
#             ] .
#             ?class rdfs:comment ?comment .
#             ?class rdf:type owl:Class ;
#                    rdfs:label "FloodResponse"
#         }
        # """

        query = """
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns##>
        BASE <http://mismo.org/Subset/>
        
            SELECT ?propertyName ?comment
            WHERE {
                :FloodResponse rdfs:subClassOf/owl:onProperty/rdfs:label ?propertyName .
            }
        """
        
        qres = g.query(query)
        # st.write(qres)
        # Print the results
        for row in qres:
            st.write(f"propertyName: {row.propertyName}, Comment: {row.comment}")
        # for row in qres:
        #     st.write(f"Property: {row.property}")