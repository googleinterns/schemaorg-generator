# SchemaOrgUtils Python
This directory contains an install-able python library that can be used to serialize and validate feed.

## Usage
### Install the package
```
pip3 install . --user
```
	 
### SchemaValidator

SchemaValidator is used to validate a JSON-LD schema graph against SHACL constraints.

#### Functions and parameters
##### constructor(constraints_file, report_file):
Initialize the validator.
 - ```constraints_file``` - The path to the file containing SHACL constraints against which the entities need to be validated. The constraints file must be in *Turtle* format.
 - ```report_file``` - The path to file where report must be generated. The report file must be in *html* format.
 
##### add_item(entity):
 Validate item and process the validation errors.
 - ```entity``` - The entity that must be validated.
 
##### close():
 Close the validator and generate the report.

#### General Usage
```
import schemaorgutils.validator.validator as validator

v = validator.SchemaValidator("/path/to/constraints.ttl", "/path/to/report.html")

feed = "JSON-LD feed that needs to be validated"

for x in feed:
	v.add_entity(x)

v.close()

```
 
#### Usage for ItemList
To validate an *ItemList* it must of the following format.

```
{
	"@context":"https://schema.org",
	"@type":"ItemList",
	"itemListElement":[
		{
			"@type": "ListItem",
			"item": {
						"First item to be validated"
					}
		},
		{
			"@type": "ListItem",
			"item": {
						"Second item to be validated"
					}
		},
		...
		...
		...
		]
}
```

##### Code
This code validates every entity which appear as "item" attribute of each "itemListElement".
```
import schemaorgutils.validator.validator as validator

v = validator.SchemaValidator("/path/to/constraints.ttl", "/path/to/report.html")

itemlist = "JSON-LD ItemList that needs to be validated"

v.add_entity(itemlist)

v.close()
```

#### Usage for DataFeed
To validate a *DataFeed* it must be of the following format.

```
{
	"@context":"https://schema.org",
	"@type":"DataFeed",
	"dataFeedElement":[
		{
			"First item to be validated"
		},
		{
			"Second item to be validated"
		},
		...
		...
		...
		]
}
```

##### Code
This code validates every entity which appear as "dataFeedElement".
```
import schemaorgutils.validator.validator as validator

v = validator.SchemaValidator("/path/to/constraints.ttl", "/path/to/report.html")

datafeed = "JSON-LD DataFeed that needs to be validated"

v.add_entity(datafeed)

v.close()
```


### JSONLDSerializer
JSONLDSerializer takes in a proto object of schema and serializes it and writes to file.

#### Functions and parameters
##### constructor():
Initialize the serializer.
 
##### write(obj, outfile, schema):
Serialize and write to file.

 - ```obj```: The object that needs to be serialized.
 - ```outfile```: The path to file where output needs to be written to.
 - ```schema```: Module containing the compiled proto schema in python. 

	 

 
#### Code
```
import schema_pb2 as schema #The compiled proto schema in python
import schemaorgutils.serializer.serializer as serializer

movie = schema.Movie()

for x in ["Johnny Depp", "Penelope Cruz", "Ian McShane"]:
        actor = movie.actor.add()
        person = actor.person
        name = person.name.add()
        name.text = x

ser = new serializer.JSONLDSerializer()
ser.write(movie, "/path/to/outfile.json", schema) 
```

#### Output
```
{
    "@context": "http://schema.org",
        "@type": "Movie",
        "actor": [
                {
                        "@type": "Person",
                        "name": "Johnny Depp"
                },
                {
                        "@type": "Person",
                        "name": "Penelope Cruz"
                },
                {
                        "@type": "Person",
                        "name": "Ian McShane"
                }
        ]
}
```

### JSONLDFeedSerializer
JSONLDFeedSerializer is used for serializing feeds that contain huge number of entities. Each entity will be written to file as soon as add_item() is called thus saving the memory. Users fetching feed from database are advised to use ServerSideCursor and serialize the entities item by item in order to save memory.

#### Functions and parameters
##### constructor(outfile, feed_type, validator = None):
Initialize the serializer.

 - ```outfile```: Path to file where output has to be written.
 - ```feed_type```: Type of feed that has to be generated. "ItemList" or "DataFeed".
 - ```validator```: Validator that can be used to validate the feed. If the validator returns false the feed wont be validated. Defaulted to no validator.

 
##### add_item(obj, schema):
Serialize the entity if validation is successful.

 - ```obj```: The entity that needs to be serialized.
 - ```schema```: Module containing the compiled proto schema in python. 

##### close():
Close the serializer and validator if exists.


#### Code
```
import schemaorgutils.serializer.serializer as serializer
import schemaorgutils.validator.validator as validator
import serializer.schema_pb2 as schema

v = validator.SchemaValidator("/path/to/constraints.ttl", "/path/to/report.html")
jfs = serializer.JSONLDFeedSerializer("/path/to/outfile.json", feed_type="ItemList", validator=v)

for i in  range(3):
	mv = schema.Movie()
	mv.name.add().text = "Movie " + str(i+1)
	mv.id = "Id of Movie " + str(i+1)
	jis.add_item(mv, schema)

jis.close()

```

#### Output(If every movie passed validation)
```
{
        "@context":"https://schema.org",
        "@type":"ItemList",
        "itemListElement":[
                {
                    "@type": "ListItem",
                    "item": {
                        "@id": "Id of Movie 1",
                        "@type": "Movie",
                        "name": "Movie 1"
                    },
                    "position": 1
                },
                {
                    "@type": "ListItem",
                    "item": {
                        "@id": "Id of Movie 2",
                        "@type": "Movie",
                        "name": "Movie 2"
                    },
                    "position": 2
                },
                {
                    "@type": "ListItem",
                    "item": {
                        "@id": "Id of Movie 3",
                        "@type": "Movie",
                        "name": "Movie 3"
                    },
                    "position": 3
                }
		 ]
 }
```

### Running Example
The example does the following:

 - Read data from example/dump.json and seed the Database using IMDBSeeder class. This is done to simulate an environment where data is stored in database and the requirement is to generate JSON-LD feed from database.
 - The IMDBExample class reads from database and generates proto representation for that and uses the JSONLDFeedSerializer to serialize the proto objects into an ItemList.
 - The final generated feed is stored in example/generated-feed.json.

 Steps to be followed to run example.
 - Move into example folder. ``` cd example ```
 - Copy config.example.json to config.json. ``` cp config.example.json config.json ```
 - Populate config.json with credentials.
 - Copy compiled proto schema to the example folder. ``` cp /path/to/schema_pb2.py schema_pb2.py ```
 - Run main.py. ``` python3 main.py ```

### Run tests
To run tests follow the instructions below:

 - Install pytest. ```pip3 install pytest```
 - Copy compiled schema to tests folder. ```cp /path/to/schema_pb2.py tests/schema_pb2.py ```
 - Run tests. ``` pytest ```
