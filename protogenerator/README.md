
# ProtoBuf Code Generator

This directory contains a library that can be used to generate protocol buffer code for any schema.org release or any graph that follows certains specifications. The specifications are listed in following section.

## Specifications
- Type is identified using **http://www.w3.org/1999/02/22-rdf-syntax-ns#type** predicate.
- Subclass is identified using **http://www.w3.org/2000/01/rdf-schema#subClassOf** predicate.
- All classes have type of **http://www.w3.org/2000/01/rdf-schema#Class**.
- All properties have type of **http://www.w3.org/1999/02/22-rdf-syntax-ns#Property**.
- All enumerations are subclass of **http://schema.org/Enumeration**.
- Properties are mapped to their corresponding classes or enumerations using **http://schema.org/domainIncludes**. 
- Properties are mapped to their possible values (classes/enumerations/datatypes) using **http://schema.org/rangeIncludes**. 
- Children classes are subclass of parent classes.
- Possible value of an enumeration is mapped to the enumeration using **http://www.w3.org/1999/02/22-rdf-syntax-ns#type** predicate.
- Classes which are considered as datatypes are:
	1) http://schema.org/Text
	2) http://schema.org/URL
	3) http://schema.org/Number
	4) http://schema.org/Float
	5) http://schema.org/Integer
	6) http://schema.org/Boolean
	7) http://schema.org/Date
	8) http://schema.org/DateTime
	9) http://schema.org/Time
	10) http://schema.org/Duration
	11) http://schema.org/Distance
	12) http://schema.org/Energy
	13) http://schema.org/Mass
	
- All comments that need to be added to message definition in the proto file is mapped using **http://www.w3.org/2000/01/rdf-schema#comment** predicate.
- Refer schema.org releases for further insight.

## Usage
- Install required modules. `pip3 install requiremnts.txt`
-  Run main.py
```
main.py [-h] (-s SRC | -v VER) -o OUT -p PKG

optional arguments:
  -h, --help         show this help message and exit
  -s SRC, --SRC SRC  Path to source file
  -v VER, --VER VER  Schema.org release number
  -o OUT, --OUT OUT  Path to output directory
  -p PKG, --PKG PKG  Proto package name
```
- Note that either of SRC or VER is madatory. SRC indicates path to schema file while VER indicates release number. 
- If you use VER it automatically downloads the schema from schema.org github repo and use it for generating the protocol buffer codes and cleans the downloaded schema on successful execution.
- This generates two files named `schema.proto` and `schema_descriptor.json`.
- `schema.proto` is the actual proto code while `schema_descriptor.json` is the JSON Descriptor to be used by serializers that does not have native proto descriptors.
- The source schema file can be in any format supported by the python package `rdflib`.

### Sample usage

    python3 main.py -v 8.0 -o ./ -p schemaorg
    python3 main.py -s ./schema.nt -o ./ -p schemaorg
