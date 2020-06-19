# JSON-LD Serializer Python
This directory contains JSON-LD serializer for generating schema.org compliant data feed using javascript.

## Usage

### Example Code
```
const schema = require('./path/to/schema');
const schemaDescriptor = require("./path/to/jsondescriptor");
const JSONLDSerializer = require("./path/to/serializer").JSONLDSerializer;


let movie = new schema.Movie();

for( let i of ["Johnny Depp", "Penelope Cruz", "Ian McShane"]){
    let actor = new schema.ActorProperty();
    let person = new schema.Person();
    let name = new schema.NameProperty();
    name.setText(i);
    person.addName(name);
    actor.setPerson(person);
    movie.addActor(actor);
}

let serializer = new JSONLDSerializer()
serializer.writeToFile(movie, "Movie", schemaDescriptor, "./out.json");

```

### Output
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
