import serializer as serializer
import schema_pb2 as schema


def test_date():
    """Test serialization of date.
    Procedure:
        - Create a new serializer.
        - Create a date object in proto.
        - Set values for year, month and day.
        - Make the expected output string in ISO8601 format.
        - Call the serialize_proto function of serializer along with schema
          and date object.

    Verification:
        - Check if the returned string is equal to expected string and is in
          ISO8601 format.
    """

    j = serializer.JSONLDSerializer()

    dt = schema.Date()
    dt.year = 2000
    dt.month = 2
    dt.day = 9

    expected = '2000-02-09'
    output = j.serialize_proto(dt, schema)
    assert output == expected, 'Date serialization failed.'


def test_time():
    """Test serialization of time.
    Procedure:
        - Create a new serializer.
        - Create a time object in proto for following cases.
            * Without timezone.
            * With timezone.
        - Set values for hours, minutes and seconds.
        - Make the expected output string for both cases in ISO8601 format.
        - Call the serialize_proto function of serializer along with schema and
          time object for both cases.

    Verification:
        - Check if the returned string is equal to expected string and is in
          ISO8601 format.
        - Check if the timezone is added correctly.
    """

    j = serializer.JSONLDSerializer()

    tm = schema.Time()
    tm.hours = 6
    tm.minutes = 30
    tm.seconds = 15

    expected = '06:30:15'
    output = j.serialize_proto(tm, schema)
    assert output == expected, 'Time(without timezone) serialization failed.'

    tm.timezone = '+05:30'

    expected = '06:30:15+05:30'
    output = j.serialize_proto(tm, schema)
    assert output == expected, 'Time(with timezone) serialization failed.'


def test_datetime():
    """Test serialization of datetime.
    Procedure:
        - Create a new serializer.
        - Create a datetime object in proto for following cases.
            * Without timezone.
            * With timezone.
        - Set values for hours, minutes and seconds.
        - Set values for year, month and day.
        - Make the expected output string for both cases in ISO8601 format.
        - Call the serialize_proto function of serializer along with schema
          and datetime object for both cases.

    Verification:
        - Check if the returned string is equal to expected string and is in
          ISO8601 format.
        - Check if the timezone is added correctly.
    """

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

    expected = '2000-02-09T06:30:15'
    output = j.serialize_proto(dtt, schema)
    assert output == expected, 'DateTime(without timezone) serialization failed.'

    tm.timezone = '+05:30'

    expected = '2000-02-09T06:30:15+05:30'
    output = j.serialize_proto(dtt, schema)
    assert output == expected, 'DateTime(with timezone) serialization failed.'


def test_duration():
    """Test serialization of duration.
    Procedure:
        - Create a new serializer.
        - Create a duration object in proto
        - Set value for seconds.
        - Make the expected output string in ISO8601 duration format.
        - Call the serialize_proto function of serializer along with schema
          and duration object.

    Verification:
        - Check if the returned string is equal to expected string and is in
          ISO8601 duration format.
    """

    j = serializer.JSONLDSerializer()

    dur = schema.Duration()
    dur.seconds = 100456123

    expected = 'P1162DT16H28M43S'
    output = j.serialize_proto(dur, schema)
    assert output == expected, 'Duration serialization failed.'


def test_quantitative():
    """Test serialization of quantitative values.
    Procedure:
        - Create a new serializer.
        - Create object of following types in proto:
            * Mass
            * Distance
            * Energy
        - Set the fields unit and value for each of the objects.
        - Make the expected output string for each object.
        - Call the serialize_proto function of serializer along with schema
          and each object.

    Verification:
        - Check if the returned string is equal to '<value> <unit>' for each
          object.
    """

    j = serializer.JSONLDSerializer()

    ms = schema.Mass()
    ms.value = 10.5
    ms.unit = 'KG'

    expected = '10.5 KG'
    output = j.serialize_proto(ms, schema)
    assert output == expected, 'Mass serialization failed.'

    ds = schema.Distance()
    ds.value = 10.5
    ds.unit = 'Metre'

    expected = '10.5 Metre'
    output = j.serialize_proto(ds, schema)
    assert output == expected, 'Distance serialization failed.'

    eg = schema.Energy()
    eg.value = 10.5
    eg.unit = 'Joules'

    expected = '10.5 Joules'
    output = j.serialize_proto(eg, schema)
    assert output == expected, 'Mass serialization failed.'


def test_property():
    """Test serialization of property.
    Procedure:
        - Create a new serializer.
        - Create a proto property.
        - Set any two fields of the property.
        - Call the serialize_proto function of serializer along with schema and
          property.

    Verification:
        - Check if the returned value is that of field set at last and that it
          is not enclosed inside any dict.
    """

    j = serializer.JSONLDSerializer()
    prop = schema.PositionProperty()
    prop.text = 'abc'
    prop.url = 'def'

    expected = 'def'
    output = j.serialize_proto(prop, schema)

    assert output == expected, 'Property serialization failed.'


def test_class():
    """Test serialization of class.
    Procedure:
        - Create a new serializer.
        - Create a proto class.
        - Set two properties such that:
            * It has a single value.
            * It has multiple values.
        - Set id for the class.
        - Call the serialize_proto function of serializer along with schema and
          class.

    Verification:
        - Check if the returned value is an python dict.
        - Check if the property having single value is not enclosed in an an
          array/list.
        - Check if the property having multiple values is enclosed inside an
          array.
        - Check if the dict has '@type' key with value as schemaorg name of
          class.
        - Check if the dict has '@id' field set to the id of class.
    """

    j = serializer.JSONLDSerializer()

    c = schema.Movie()
    c.id = 'test id 1'
    # Single value for property.
    c.name.add().text = 'Name 1'
    # Multiple values for same property.
    c.url.add().url = 'URL 1'
    c.url.add().url = 'URL 2'

    expected = {
        '@id': 'test id 1',
        '@type': 'Movie',
        'name': 'Name 1',
        'url': [
            'URL 1',
            'URL 2'
        ]
    }

    output = j.serialize_proto(c, schema)

    assert output == expected, 'Class serialization failed.'


def test_enumeration():
    """Test serialization of enumeration.
    Procedure:
        - Create a new serializer.
        - Create proto enumeration such it behaves as:
            * Enumeration of multiple values.
            * Class
        - Set the value for the enumeration that behaves like enumeration of
          values.
        - Set a property for the enumeration that behaves like a class.
        - Set a id for the enumeration that behaves like a class.
        - Call the serialize_proto function of serializer along with each of
          the enumeration.

    Verification:
        - For enumeration that behaves like a enumeration of values check
          if returned value is a string pointing to its schema.org url.
        - For enumeration that behaves as a class do the following:
            * Check if the returned value is an python dict.
            * Check if the property is populated.
            * Check if the dict has '@type' key with value as schemaorg name of
              enumeration.
            * Check if the dict has '@id' field set to the id of enumeration.
    """

    j = serializer.JSONLDSerializer()

    c = schema.RsvpResponseType()
    c.id = schema.RsvpResponseTypeClass.Id.RSVP_RESPONSE_YES

    expected = 'http://schema.org/RsvpResponseYes'
    output = j.serialize_proto(c, schema)
    assert output == expected, 'Enumeration(Id) serialization failed.'

    c.rsvp_response_type.alternate_name.add().text = 'Alternate Name 1'
    c.rsvp_response_type.id = 'test id 1'
    expected = {
        '@id': 'test id 1',
        '@type': 'RsvpResponseType',
        'alternateName': 'Alternate Name 1'
    }
    output = j.serialize_proto(c, schema)
    assert output == expected, 'Enumeration(Class) serialization failed.'
