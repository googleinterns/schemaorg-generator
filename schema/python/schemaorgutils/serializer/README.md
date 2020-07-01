# JSON-LD Serializer Python
This directory contains JSON-LD serializer for generating schema.org compliant data feed using python.

## Usage

### Example Code
```
#The compiled proto schema in python
import /path/to/schema/schema_pb2 as schema_pb2
import /path/to/directory/serializer as serializer

movie = schema_pb2.Movie()

for x in ["Johnny Depp", "Penelope Cruz", "Ian McShane"]:
	actor = movie.actor.add()
	person = actor.person
	name = person.name.add()
	name.text = x

my_serializer = new serializer.JSONLDSerializer()
serializer.write(movie, "/path/to/outfile/", schema_pb2) 
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
