import serializer.serializer as serializer
import serializer.schema_pb2 as schema

def test_date():
    
    j = serializer.JSONLDSerializer()
    
    dt = schema.Date()
    dt.year = 2000
    dt.month = 2
    dt.day = 9

    expected = "2000-02-09"
    output = j.proto_to_dict(dt, schema)
    assert output == expected, "Date serialization failed."

def test_time():
    
    j = serializer.JSONLDSerializer()

    tm = schema.Time()
    tm.hours = 6
    tm.minutes = 30
    tm.seconds = 15

    expected = "06:30:15"
    output = j.proto_to_dict(tm, schema)
    assert output == expected, "Time(without timezone) serialization failed."

    tm.timezone = "+05:30"
    
    expected = "06:30:15+05:30"
    output = j.proto_to_dict(tm, schema)
    assert output == expected, "Time(with timezone) serialization failed."


def test_datetime():
    
    j = serializer.JSONLDSerializer()
    
    dtt = schema.DateTime()
    dt = dtt.date
    dt.year = 2000
    dt.month = 2
    dt.day = 9

    tm = dtt.time
    tm.hours = 6
    tm.minutes = 30
    tm.seconds = 15

    expected = "2000-02-09T06:30:15"
    output = j.proto_to_dict(dtt, schema)
    assert output == expected, "DateTime(without timezone) serialization failed."

    tm.timezone = "+05:30"
    
    expected = "2000-02-09T06:30:15+05:30"
    output = j.proto_to_dict(dtt, schema)
    assert output == expected, "DateTime(with timezone) serialization failed."

def test_duration():
    
    j = serializer.JSONLDSerializer()

    dur = schema.Duration()
    dur.seconds = 100456123

    expected = "P1162DT16H28M43S"
    output = j.proto_to_dict(dur, schema)
    assert output == expected, "Duration serialization failed."

def test_quantitative():
    
    j = serializer.JSONLDSerializer()

    ms = schema.Mass()
    ms.value = 10.5
    ms.unit = "KG"

    expected = "10.5 KG"
    output = j.proto_to_dict(ms, schema)
    assert output == expected, "Mass serialization failed."

    ds = schema.Distance()
    ds.value = 10.5
    ds.unit = "Metre"

    expected = "10.5 Metre"
    output = j.proto_to_dict(ds, schema)
    assert output == expected, "Distance serialization failed."

    eg = schema.Energy()
    eg.value = 10.5
    eg.unit = "Joules"

    expected = "10.5 Joules"
    output = j.proto_to_dict(eg, schema)
    assert output == expected, "Mass serialization failed."

def test_property():
    
    j = serializer.JSONLDSerializer()
    prop = schema.PositionProperty()
    prop.text = "abc"
    prop.url = "def"

    expected = "def"
    output = j.proto_to_dict(prop, schema)

    assert output == expected, "Property serialization failed."

def test_class():
    
    j = serializer.JSONLDSerializer()
    
    c = schema.Movie()
    # Single value for property.
    c.name.add().text = "Name 1"  
    # Multiple values for same property.
    c.url.add().url = "URL 1"
    c.url.add().url = "URL 2"

    expected = {
        "@type": "Movie",
        "name": "Name 1",
        "url": [
            "URL 1",
            "URL 2"
            ]
        }

    output = j.proto_to_dict(c, schema)

    assert output == expected, "Class serialization failed."

def test_enumeration():

    j = serializer.JSONLDSerializer()

    c = schema.RsvpResponseType()
    c.id = schema.RsvpResponseTypeClass.Id.RSVP_RESPONSE_YES

    expected = "https://schema.org/RsvpResponseYes"
    output = j.proto_to_dict(c, schema)
    assert output == expected, "Enumeration(Id) serialization failed."

    c.rsvp_response_type.alternate_name.add().text = "Alternate Name 1"
    expected = {
        "@type": "RsvpResponseType",
        "alternateName": "Alternate Name 1"
    }
    output = j.proto_to_dict(c, schema)
    assert output == expected, "Enumeration(Class) serialization failed."

