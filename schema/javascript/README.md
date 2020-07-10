# SchemaOrgUtils Javascript
This directory contains an install-able javascript library that can be used to serialize and validate feed.


## Usage
### Install the package
- From this directory.
```
npm install
npm link .
```
- Inside the directory where this package has to be used.
```
npm link schemaorgutils
```
	 
### SchemaValidator

SchemaValidator is used to validate a JSON-LD schema graph against SHACL constraints.

#### Functions and parameters
##### constructor(constraintsFile, reportFile):
Initialize the validator.
 - ```constraintsFile``` - The path to the file containing SHACL constraints against which the entities need to be validated. The constraints file must be in *Turtle* format.
 - ```reportFile``` - The path to file where report must be generated. The report file must be in *html* format.
 
##### async loadShapes():
 Loads the SHACL shapes graph. Must be called before any entity can be validated.
 
##### async addEntity(entity):
 Validate item and process the validation errors.
 - ```entity``` - The entity that must be validated.
 
##### close():
 Close the validator and generate the report.

#### General Usage
```
const  SchemaValidator = require("schemaorgutils").SchemaValidator;

let  validator = new  SchemaValidator("/path/to/constraints.ttl", "/path/to/report.html");

await  validator.loadShapes();

const  feed = "JSON-LD feed that needs to be validated";

for(let  x  of  feed){

	await  validator.addEntity(x);

}

validator.close();

```
 
#### Usage for ItemList
To validate an ItemList it must of the following format.

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
const  SchemaValidator = require("schemaorgutils").SchemaValidator;

let  validator = new  SchemaValidator("/path/to/constraints.ttl", "/path/to/report.html");

await  validator.loadShapes();

const  itemList = "JSON-LD ItemList that needs to be validated";

await  validator.addEntity(itemList);

validator.close();
```

#### Usage for DataFeed
To validate a DataFeed it must be of the following format.

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
const  SchemaValidator = require("schemaorgutils").SchemaValidator;

let  validator = new  SchemaValidator("/path/to/constraints.ttl", "/path/to/report.html");

await  validator.loadShapes();

const  dataFeed = "JSON-LD DataFeed that needs to be validated";

await  validator.addEntity(dataFeed);

validator.close();
```


### JSONLDSerializer
JSONLDSerializer takes in a proto object of schema and serializes it and writes to file.

#### Functions and parameters
##### constructor():
Initialize the serializer.
 
##### writeToFile(obj, objectType, schemaDescriptor, outFile):
Serialize and write to file.

 - ```obj```: Object that needs to be serialized.
 - ```objectType```: Schemaorg type of object that needs to be serialized.
 - ```schemaDescriptor```: JSON descriptor for the specific release of schema. 
 - ```outfile```: Path to file where output needs to be written to.
	 

 
#### Code
```
const JSONLDSerializer = require("schemaorgutils").JSONLDSerializer;
const schemaDescriptor = require("/path/to/schema_descriptor.json");
const schema = require("/path/to/schema_pb");

let  serializer = new  JSONLDSerializer();
let actors = ["Johnny Depp", "Penelope Cruz", "Ian McShane"];

let movie = new schema.Movie()

for(let x of actors) {
        let actor = new schema.ActorProperty();
        let person = new schema.Person();
        let name = new schema.NameProperty();
        name.setText(x);
        person.addName(name);
        actor.setPerson(person);
        movie.addActor(actor);
}

serializer.writeToFile(movie,"Movie",schemaDescriptor,"/path/to/outfile.json");
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
##### constructor(outFile, feedType, validator = null):
Initialize the serializer.

 - ```outFile```: Path to file where output has to be written.
 - ```feedType```: Type of feed that has to be generated. "ItemList" or "DataFeed".
 - ```validator```: Validator that can be used to validate the feed. If the validator returns false the feed wont be validated. Defaulted to no validator.

 
##### addItem(entity, entityType, schemaDescriptor):
Serialize the entity if validation is successful.

 - ```entity```: Entity that needs to be serialized.
 - ```entityType```: Schmeaorg type of entity that needs to be serialized.
 - ```schemaDescriptor```: JSON descriptor for the specific release of schema. 

##### close():
Close the serializer and validator if exists.


#### Code
```
const JSONLDFeedSerializer = require("schemaorgutils").JSONLDFeedSerializer;
const schemaDescriptor = require("/path/to/schema_descriptor.json");
const schema = require("/path/to/schema_pb");

let  serializer = new  JSONLDFeedSerializer("/path/to/outfile.json", "ItemList");

for(let i=0; i<3; i++) {
		let movie = new schema.Movie();
        let name = new schema.NameProperty();
        name.setText("Movie " + (i+1).toString());
        movie.addName(name);
        movie.setId("Id of Movie " + (i+1).toString());
        serializer.addItem(movie, "Movie", schemaDescriptor);
}

serializer.close();

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
 - Copy compiled proto schema to the example folder. ``` cp /path/to/schema_pb.js schema_pb.js ```
 - Copy schema descriptor to the example folder. ``` cp /path/to/schema_descriptor.json schema_descriptor.json ```
 - Run index.js. ``` node index.js ```

### Run tests
To run tests follow the instructions below:

 - Copy compiled proto schema to the test folder. ``` cp /path/to/schema_pb.js test/schema_pb.js ```
 - Copy schema descriptor to the example folder. ``` cp /path/to/schema_descriptor.json  test/schema_descriptor.json ```
 - Run tests. ``` npm run test ```
