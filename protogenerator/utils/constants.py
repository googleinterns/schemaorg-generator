# Copyright 2020 Google LLC

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     https://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import rdflib

proto_primitives = {
    'double',
    'float',
    'int32',
    'int64',
    'uint32',
    'uint64',
    'sint32',
    'sint64',
    'fixed32',
    'fixed64',
    'sfixed32',
    'sfixed64',
    'bool',
    'string',
    'bytes'}

schema_primitives = {
    'Text': 'string',
    'Number': 'double',
    'Boolean': 'bool',
    'Integer': 'int64',
    'Float': 'double',
    'URL': 'string',
    }

schema_datatypes = {'Date', 'DateTime', 'Time', 'DataType', 'Duration', 'Distance', 'Energy', 'Mass'}

schema_constants = {
    'Type': rdflib.URIRef('http://www.w3.org/1999/02/22-rdf-syntax-ns#type'),
    'Class': rdflib.URIRef('http://www.w3.org/2000/01/rdf-schema#Class'),
    'Property': rdflib.URIRef('http://www.w3.org/1999/02/22-rdf-syntax-ns#Property'),
    'rangeIncludes': rdflib.URIRef('http://schema.org/rangeIncludes'),
    'domainIncludes': rdflib.URIRef('http://schema.org/domainIncludes'),
    'subClassOf': rdflib.URIRef('http://www.w3.org/2000/01/rdf-schema#subClassOf'),
    'Enumeration': rdflib.URIRef('http://schema.org/Enumeration'),
    'Thing': rdflib.URIRef('http://schema.org/Thing'),
    'Number': rdflib.URIRef('http://schema.org/Number'),
    'Integer': rdflib.URIRef('http://schema.org/Integer'),
    'Float': rdflib.URIRef('http://schema.org/Float'),
    'Text': rdflib.URIRef('http://schema.org/Text'),
    'URL': rdflib.URIRef('http://schema.org/URL'),
    'Comment': rdflib.URIRef('http://www.w3.org/2000/01/rdf-schema#comment')
}
