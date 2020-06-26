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
import os
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

        out_obj = self.proto_to_dict(obj, schema)
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
            
            if descriptor.name == "id":
                if len(value) > 0:
                    out_obj[descriptor.json_name] = value
            elif len(value) > 0:
                out_obj[descriptor.json_name] = [
                    self.proto_to_dict(x, schema) for x in value]
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
                return self.proto_to_dict(value, schema)

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
            return self.proto_to_dict(value, schema)

    def __date_to_string(self, obj):
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

    def __time_to_string(self, obj):
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

    def __datetime_to_string(self, obj):
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

    def proto_to_dict(self, obj, schema):
        """Convert a protobuf schema message to dictionary.

        Args:
            obj (protobuf object): Protobuf object of schema.
            schema (module): Module containing compiled proto schema.

        Returns:
            dict: The schema object as a dictionary/list/string depending on the schema type.
        """

        if self.__check_primtive(obj):
            return obj

        messageType = obj.DESCRIPTOR.GetOptions().Extensions[schema.type]
        if messageType == 'Property':
            return self.__get_property_value(obj, schema)
        
        elif messageType == 'EnumWrapper':
            return self.__enum_to_dict(obj, schema)
        
        elif messageType == 'DatatypeDate':
            return self.__date_to_string(obj)
        
        elif messageType == 'DatatypeTime':
            return self.__time_to_string(obj)
        
        elif messageType == 'DatatypeDateTime':
            return self.__datetime_to_string(obj)
        
        elif messageType == 'DatatypeQuantitaive':
            return self.__quantitative_to_string(obj)
        
        elif messageType == 'DatatypeDuration':
            return self.__duration_to_string(obj)
        
        else:
            return self.__class_to_dict(obj, schema)

class JSONLDItemListSerializer(JSONLDSerializer):

    def __init__(self, outfile):
            
            JSONLDSerializer.__init__(self)
            assert isinstance(outfile, str), "Invalid parameter 'outfile' must be 'str'."

            self.count = 0
            self.outfile  = open(outfile, "wb")
            self.outfile.write(bytes("{\n", 'utf-8'))
            self.outfile.write(bytes("\t\"@context\":\"https://schema.org\",\n", 'utf-8'))
            self.outfile.write(bytes("\t\"@type\":\"ItemList\",\n", 'utf-8'))
            self.outfile.write(bytes("\t\"itemListElement\":[", 'utf-8'))

    def add_item(self, list_item, schema):
        
        assert self.outfile.closed == False, "The serializer had been already closed."
        assert isinstance(list_item, schema.ListItem), "'list_item' must be an instance of schema.ListItem"

        list_item = self.proto_to_dict(list_item, schema)
        list_item = json.dumps(list_item, indent=4, sort_keys=True)
        list_item = "\n" + list_item
        list_item = list_item.replace("\n", "\n\t\t")
        list_item = list_item + ","
        self.outfile.write(bytes(list_item, 'utf-8'))
        self.count = self.count + 1
        
    
    def close(self):

        assert self.outfile.closed == False, "The serializer had been already closed."

        if self.count:
            self.outfile.seek(-1, os.SEEK_CUR)
        
        self.outfile.write(bytes("\n\t]\n", 'utf-8'))
        self.outfile.write(bytes("}\n", 'utf-8'))
        self.outfile.close()
        

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
# movie.id = "id no 1"

# serializer = JSONLDSerializer()
# serializer.write(movie, "./test.json", schema_pb2)

# print(type(schema_pb2))
