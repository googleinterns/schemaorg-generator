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

        out_obj = self.__proto_to_dict(obj, schema)
        out_obj['@context'] = 'http://schema.org'

        fp = open(outfile, 'w')
        json.dump(out_obj, fp, indent=4, sort_keys=True)
        fp.close()

    def __class_to_dict(self, obj, schema):
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
            if len(value) > 0:
                out_obj[descriptor.json_name] = [
                    self.__proto_to_dict(x, schema) for x in value]
                if len(out_obj[descriptor.json_name]) == 1:
                    out_obj[descriptor.json_name] = out_obj[descriptor.json_name][0]

        return out_obj

    def __get_property_value(self, obj, schema):
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
                print(value)
                return self.__proto_to_dict(value, schema)

    def __enum_to_dict(self, obj, schema):
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
            return self.__proto_to_dict(value, schema)

    def __parse_date(self, obj):
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
        # Need to handle timezone

        date = datetime.date(year=year, month=month, day=day)
        return date

    def __parse_time(self, obj):
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
        # Need to handle timezone

        time = datetime.time(hour=hours, minute=minutes, second=seconds)
        return time

    def __datetime_to_string(self, obj):
        """Convert a protobuf datetime object to isostring format.

        Args:
            obj (protobuf object): Protobuf object of datetime.
            schema (module): Module containing compiled proto schema.

        Returns:
            date_time: Isostring format of proto datetime.
        """

        date = self.__parse_date(getattr(obj, 'date'))
        time = self.__parse_time(getattr(obj, 'time'))

        date_time = datetime.datetime(
            year=date.year,
            month=date.month,
            day=date.day,
            hour=time.hour,
            minute=time.minute,
            second=time.second).isoformat()

        return date_time

    def __duration_to_string(self, obj):
        """Convert a proto duration object to ISO8601 string.

        Args:
            obj (protobuf object): Protobuf object of duration.

        Returns:
            string: The duration as ISO8601 string.
        """
        
        sec = obj.seconds
        d = datetime.timedelta(seconds=sec)
        return isodate.duration_isoformat(d)
    
    def __quantitative_to_string(self, obj):
        """Convert a proto quantitative object to string.

        Args:
            obj (protobuf object): Protobuf object of quantitative object.

        Returns:
            string: The quantitative object as string.
        """
        
        value = obj.value
        unit = obj.unit
        return str(value) + " " + unit

    def __check_primtive(self, obj):
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

    def __proto_to_dict(self, obj, schema):
        """Convert a protobuf schema message to dictionary.

        Args:
            obj (protobuf object): Protobuf object of schema.
            schema (module): Module containing compiled proto schema.

        Returns:
            dict: The schema object as a dictionary/list/string depending on the schema type.
        """

        if self.__check_primtive(obj):
            return str(obj)

        messageType = obj.DESCRIPTOR.GetOptions().Extensions[schema.type]
        if messageType == 'Property':
            return self.__get_property_value(obj, schema)
        elif messageType == 'EnumWrapper':
            return self.__enum_to_dict(obj, schema)
        elif messageType == 'DatatypeDate':
            return self.__parse_date(obj).isoformat()
        elif messageType == 'DatatypeTime':
            return self.__parse_time(obj).isoformat()
        elif messageType == 'DatatypeDateTime':
            return self.__datetime_to_string(obj)
        elif messageType == 'DatatypeQuantitaive':
            return self.__quantitative_to_string(obj)
        elif messageType == 'DatatypeDuration':
            return self.__duration_to_string(obj)
        else:
            return self.__class_to_dict(obj, schema)

# Test code to be removed later
# import schema_pb2
# movie = schema_pb2.Movie()
# actor = movie.actor.add()
# person = actor.person
# name = person.name.add()
# name.text = "Johnny Depp"
# actor = movie.actor.add()
# person = actor.person
# name = person.name.add()
# name.text = "Penelope Cruz"
# actor = movie.actor.add()
# person = actor.person
# name = person.name.add()
# name.text = "Ian McShane"

# serializer = JSONLDSerializer()
# serializer.write(movie, "./test.json", schema_pb2)

# print(type(schema_pb2))
