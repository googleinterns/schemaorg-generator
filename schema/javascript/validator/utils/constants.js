const factory = require('rdf-ext');

const resultConstants = {
    "Type": factory.namedNode("http://www.w3.org/1999/02/22-rdf-syntax-ns#type"),
    "ValidationResult": factory.namedNode("http://www.w3.org/ns/shacl#ValidationResult"),
    "ResultPath": factory.namedNode("http://www.w3.org/ns/shacl#resultPath"),
    "Value": factory.namedNode("http://www.w3.org/ns/shacl#value"),
    "ResultSeverity": factory.namedNode("http://www.w3.org/ns/shacl#resultSeverity"),
    "FocusNode": factory.namedNode("http://www.w3.org/ns/shacl#focusNode"),
    "Name": factory.namedNode("http://schema.org/name"),
    "Url": factory.namedNode("http://schema.org/url"),
    "Message": factory.namedNode("http://www.w3.org/ns/shacl#resultMessage")
};

let dataTypes = {
    "http://www.w3.org/2001/XMLSchema#integer": "integer",
    "http://www.w3.org/2001/XMLSchema#double": "double",
    "http://www.w3.org/2001/XMLSchema#boolean": "boolean",
    "http://www.w3.org/2001/XMLSchema#string": "string"
};

module.exports.resultConstants = resultConstants;
module.exports.dataTypes = dataTypes;
