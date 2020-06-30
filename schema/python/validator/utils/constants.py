import rdflib
result_constants = {
    "Type": rdflib.URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#type"),
    "ValidationResult": rdflib.URIRef("http://www.w3.org/ns/shacl#ValidationResult"),
    "ResultPath": rdflib.URIRef("http://www.w3.org/ns/shacl#resultPath"),
    "Value": rdflib.URIRef("http://www.w3.org/ns/shacl#value"),
    "ResultSeverity": rdflib.URIRef("http://www.w3.org/ns/shacl#resultSeverity"),
    "FocusNode": rdflib.URIRef("http://www.w3.org/ns/shacl#focusNode"),
    "Name": rdflib.URIRef("http://schema.org/name"),
    "Url": rdflib.URIRef("http://schema.org/url"),
    "Message": rdflib.URIRef("http://www.w3.org/ns/shacl#resultMessage")
}