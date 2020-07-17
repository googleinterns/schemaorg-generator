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
import json
import datetime
import isodate
from types import ModuleType


class JSONLDSerializer():
    """The JSONLDSerializer generates JSONLD output for protocol buffer
    objects, that are generated from schemaorg releases.

    Attributes:
        _primitive_types (set): Set of primitive types in python.
    """

    def __init__(self):
        self._primitive_types = {float, int, str, bool, str}

    def write(self, obj, outfile, schema):
        """Write JSONLD output to outfile.

        Args:
            obj (protobuf object): Protobuf object that needs to be serialized.
            outfile (str): Outfile to write the output.
            schema (module): Module containing compiled proto schema.
        """

        assert isinstance(
            outfile, str), "Invalid parameter 'outfile' must be 'str'."
        assert isinstance(
            schema, ModuleType), "Invalid parameter 'schema' must be <class 'module'>."

        out_obj = self.serialize_proto(obj, schema)
        out_obj['@context'] = 'http://schema.org'

        fp = open(outfile, 'w')
        json.dump(out_obj, fp, indent=4, sort_keys=True)
        fp.close()

    def __serialize_class(self, obj, schema):
        """Convert a schema class to dictionary.

        Args:
            obj (protobuf object): Protobuf object of schema class.
            schema (module): Module containing compiled proto schema.

        Returns:
            out_obj: The schema class as a dictionary.
        """

        out_obj = {}
        out_obj['@type'] = obj.DESCRIPTOR.GetOptions().Extensions[schema.type]
        for descriptor in obj.DESCRIPTOR.fields:
            value = getattr(obj, descriptor.name)

            if descriptor.name == 'id':
                if len(value) > 0:
                    out_obj[descriptor.json_name] = value
            elif len(value) > 0:
                out_obj[descriptor.json_name] = [
                    self.serialize_proto(x, schema) for x in value]
                if len(out_obj[descriptor.json_name]) == 1:
                    out_obj[descriptor.json_name] = out_obj[descriptor.json_name][0]

        return out_obj

    def __serialize_property(self, obj, schema):
        """Get value of a schema property.

        Args:
            obj (protobuf object): Protobuf object of schema property.
            schema (module): Module containing compiled proto schema.

        Returns:
            value: The value of schema property.
        """

        for descriptor in obj.DESCRIPTOR.fields:
            if obj.HasField(descriptor.name):
                value = getattr(obj, descriptor.name)
                return self.serialize_proto(value, schema)

    def __serialize_enum(self, obj, schema):
        """Convert a schema enumeration to dictionary or string.

        Args:
            obj (protobuf object): Protobuf object of schema enumeration.
            schema (module): Module containing compiled proto schema.

        Returns:
            value: The schema class as a dictionary or string.
        """

        desciptor = obj.DESCRIPTOR.fields[0]

        value = getattr(obj, desciptor.name)
        name = desciptor.enum_type.values[value].name

        if name != 'UNKNOWN':
            return desciptor.enum_type.values[value].GetOptions(
            ).Extensions[schema.schemaorg_value]
        else:
            desciptor = obj.DESCRIPTOR.fields[1]
            value = getattr(obj, desciptor.name)
            return self.serialize_proto(value, schema)

    def __serialize_date(self, obj):
        """Convert a protobuf date object to python date object.

        Args:
            obj (protobuf object): Protobuf object of date.
            schema (module): Module containing compiled proto schema.

        Returns:
            date: Python date object of protobuf date.
        """

        year = getattr(obj, 'year')
        month = getattr(obj, 'month')
        day = getattr(obj, 'day')

        date = datetime.date(year=year, month=month, day=day)
        return date.isoformat()

    def __serialize_time(self, obj):
        """Convert a protobuf time object to python time object.

        Args:
            obj (protobuf object): Protobuf object of time.
            schema (module): Module containing compiled proto schema.

        Returns:
            date: Python time object of protobuf time.
        """

        hours = getattr(obj, 'hours')
        minutes = getattr(obj, 'minutes')
        seconds = getattr(obj, 'seconds')
        timezone = getattr(obj, 'timezone')

        time = datetime.time(hour=hours, minute=minutes, second=seconds)

        if timezone:
            time_string = time.isoformat()
            time_string = time_string + timezone
            time = datetime.time.fromisoformat(time_string)

        return time.isoformat()

    def __serialize_datetime(self, obj):
        """Convert a protobuf datetime object to isostring format.

        Args:
            obj (protobuf object): Protobuf object of datetime.
            schema (module): Module containing compiled proto schema.

        Returns:
            date_time: Isostring format of proto datetime.
        """

        year = getattr(getattr(obj, 'date'), 'year')
        month = getattr(getattr(obj, 'date'), 'month')
        day = getattr(getattr(obj, 'date'), 'day')
        hours = getattr(getattr(obj, 'time'), 'hours')
        minutes = getattr(getattr(obj, 'time'), 'minutes')
        seconds = getattr(getattr(obj, 'time'), 'seconds')
        timezone = getattr(getattr(obj, 'time'), 'timezone')

        date_time = datetime.datetime(
            year=year,
            month=month,
            day=day,
            hour=hours,
            minute=minutes,
            second=seconds)

        if timezone:
            date_time_string = date_time.isoformat()
            date_time_string = date_time_string + timezone
            date_time = datetime.datetime.fromisoformat(date_time_string)

        return date_time.isoformat()

    def __serialize_duration(self, obj):
        """Convert a proto duration object to ISO8601 string.

        Args:
            obj (protobuf object): Protobuf object of duration.

        Returns:
            string: The duration as ISO8601 string.
        """

        sec = obj.seconds
        d = datetime.timedelta(seconds=sec)
        return isodate.duration_isoformat(d)

    def __serialize_quantitative(self, obj):
        """Convert a proto quantitative object to string.

        Args:
            obj (protobuf object): Protobuf object of quantitative object.

        Returns:
            string: The quantitative object as string.
        """

        value = obj.value
        unit = obj.unit
        return str(value) + ' ' + unit

    def __check_primitive(self, obj):
        """Check if an object is python primitive type.

        Args:
            obj (object): Object that needs to checked.

        Returns:
            bool: If it is primitive type or not.
        """

        for x in self._primitive_types:
            if isinstance(obj, x):
                return True
        return False

    def serialize_proto(self, obj, schema):
        """Convert a protobuf schema object to dictionary recursively.

        Args:
            obj (protobuf object): Protobuf object of schema.
            schema (module): Module containing compiled proto schema.

        Returns:
            dict: The schema object as a dictionary/list/string depending on 
                  the schema type.
        """

        if self.__check_primitive(obj):
            return obj

        messageType = obj.DESCRIPTOR.GetOptions().Extensions[schema.type]
        if messageType == 'Property':
            return self.__serialize_property(obj, schema)

        elif messageType == 'EnumWrapper':
            return self.__serialize_enum(obj, schema)

        elif messageType == 'DatatypeDate':
            return self.__serialize_date(obj)

        elif messageType == 'DatatypeTime':
            return self.__serialize_time(obj)

        elif messageType == 'DatatypeDateTime':
            return self.__serialize_datetime(obj)

        elif messageType == 'DatatypeQuantitative':
            return self.__serialize_quantitative(obj)

        elif messageType == 'DatatypeDuration':
            return self.__serialize_duration(obj)

        else:
            return self.__serialize_class(obj, schema)


class JSONLDFeedSerializer(JSONLDSerializer):
    """The JSONLDFeedSerializer generates serialized JSONLD output for entities
    as a ItemList or DataFeed types.

    Attributes:
        _validator (set): Set of primitive types in python.
        _feed_type (string): The type of feed that has to be generated 
                             (ItemList/DateFeed).
        _count (int): The count of items added to the feed.
        _outfile (File): The file where the feed has to be generated.
    """

    def __init__(self, outfile, feed_type='ItemList', validator=None):

        JSONLDSerializer.__init__(self)
        assert isinstance(
            outfile, str), "Invalid parameter 'outfile' must be 'str'."
        assert feed_type == 'ItemList' or feed_type == 'DataFeed', "feed_type must be 'ItemList' or 'DataFeed'."

        self._validator = validator
        self._feed_type = feed_type
        self._count = 0
        self._outfile = open(outfile, 'w')

        if self._feed_type == 'ItemList':
            self._outfile.write('{\n')
            self._outfile.write("\t\"@context\":\"https://schema.org\",\n")
            self._outfile.write("\t\"@type\":\"ItemList\",\n")
            self._outfile.write("\t\"itemListElement\":[")
        elif self._feed_type == 'DataFeed':
            self._outfile.write('{\n')
            self._outfile.write("\t\"@context\":\"https://schema.org\",\n")
            self._outfile.write("\t\"@type\":\"DataFeed\",\n")
            self._outfile.write("\t\"dataFeedElement\":[")

    def add_item(self, obj, schema):
        """Call self.serialize_proto serialize the item and write to file.

        Args:
            obj (protobuf object): Protobuf object that needs to be serialized.
            schema (module): Module containing compiled proto schema.
        """

        assert self._outfile.closed == False, 'The serializer had been already closed.'

        obj = self.serialize_proto(obj, schema)

        if (not self._validator) or (self._validator.add_entity(obj)):
            out_obj = {}

            if self._feed_type == 'ItemList':
                out_obj['@type'] = 'ListItem'
                out_obj['item'] = obj
                out_obj['position'] = self._count + 1

            elif self._feed_type == 'DataFeed':
                out_obj = obj

            out_obj = json.dumps(out_obj, indent=4, sort_keys=True)
            if self._count:
                out_obj = ',\n' + out_obj
            else:
                out_obj = '\n' + out_obj

            out_obj = out_obj.replace('\n', '\n\t\t')
            self._outfile.write(out_obj)
            self._count = self._count + 1

    def close(self):
        """Close the serializer.

        Close the validator if specified.
        """

        assert self._outfile.closed == False, 'The serializer had been already closed.'

        self._outfile.write('\n\t]\n')
        self._outfile.write('}\n')
        self._outfile.close()

        if self._validator:
            self._validator.close()
