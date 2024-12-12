from SPARQLWrapper import SPARQLWrapper, JSON
from rdflib import Graph
import ssl
import urllib.request

def test_https():
    """
    Test if HTTPS is supported in the current Python environment.
    """
    try:
        urllib.request.urlopen("https://dbpedia.org/sparql")
        print("HTTPS is working correctly.")
    except Exception as e:
        print(f"HTTPS test failed: {e}")

def query_dbpedia(query):
    """
    Function to query the DBpedia SPARQL endpoint.

    :param query: SPARQL query string
    :return: Results of the query in JSON format
    """
    endpoint = SPARQLWrapper("https://dbpedia.org/sparql")
    endpoint.setQuery(query)
    endpoint.setReturnFormat(JSON)

    try:
        results = endpoint.query().convert()
        return results
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def process_results(results):
    """
    Process and print SPARQL query results.

    :param results: JSON results from the SPARQL query
    """
    if not results:
        print("No results to process.")
        return

    print("Results:")
    for result in results["results"]["bindings"]:
        for key, value in result.items():
            print(f"{key}: {value['value']}")
        print("---")

def main():
    """
    Main function to execute a SPARQL query against DBpedia and process results.
    """
    # Test HTTPS support
    print("Testing HTTPS connectivity...")
    test_https()

    # Define your SPARQL query
    query = """
    PREFIX dbo: <http://dbpedia.org/ontology/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

    SELECT ?label ?abstract
    WHERE {
        <http://dbpedia.org/resource/Java_(programming_language)> rdfs:label ?label ;
                                                                    dbo:abstract ?abstract .
        FILTER (lang(?label) = 'en' && lang(?abstract) = 'en')
    }
    LIMIT 10
    """

    print("Executing SPARQL query...")
    results = query_dbpedia(query)
    process_results(results)

if _name_ == "_main_":
    main()