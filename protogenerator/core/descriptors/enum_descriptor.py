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
import utils.utils as utils
import utils.constants as constants
import collections
from jinja2 import Environment, FileSystemLoader


class EnumDescriptor:
    """The EnumDescriptor generates protocol buffer code for schema
    enumeration.

    Args:
        name (str): Name of the schema enumeration.
        field_types (list[utils.PropertyToParent]): The schema properties that belong to the schema enumeration.
        enum_values (list[str]): The possible values of the schema enumeration.

    Attributes:
        name (str): Name of the schema enumeration.
        field_types (list[utils.PropertyToParent]): The schema properties that belong to the schema enumeration.
        enum_values (list[str]): The possible values of the schema enumeration.
    """

    def __init__(self, name, field_types, enum_values):

        assert isinstance(name, str), "Invalid parameter 'name' must be 'str'."
        assert isinstance(
            field_types, list), "Invalid parameter 'field_types' must be 'list'."
        assert isinstance(
            enum_values, list), "Invalid parameter 'enum_values' must be 'list'."

        for x in field_types:
            assert isinstance(
                x, utils.PropertyToParent), "Every member of 'field_types' must be 'utils.PropertyToParent'."

        for x in enum_values:
            assert isinstance(
                x, str), "Every member of 'enum_values' must be 'str'."

        self.name = name
        self.field_types = field_types
        self.enum_values = enum_values

    def to_proto(self, comment):
        """Return proto code for the schema enumeration.

        Args:
            comment (string): The comment to be added to the code.

        Returns:
            proto_string: The proto code for the schema enumeration as a string.
        """

        assert isinstance(
            comment, str), "Invalid parameter 'comment' must be 'str'."

        prop_from_self = list()
        prop_inherited = dict()

        for x in self.field_types:
            if x.parent == self.name:
                prop_from_self.append(x.name)
            else:
                if x.parent not in prop_inherited:
                    prop_inherited[x.parent] = list()
                
                prop_inherited[x.parent].append(x.name)
        
        prop_from_self = sorted(prop_from_self)
        prop_inherited = collections.OrderedDict(sorted(prop_inherited.items()))

        file_loader = FileSystemLoader('./core/templates')
        env = Environment(loader=file_loader, trim_blocks=True, lstrip_blocks=True)
        env.globals["get_property_name"] = utils.get_property_name
        env.globals["to_snake_case"] = utils.to_snake_case
        env.globals["sorted"] = sorted
        env.globals["get_enum_value_name"] = utils.get_enum_value_name

        comment = "// " + comment.replace("\n", "\n// ")
        proto_string = env.get_template('enumeration.txt').render(
                                                                name = self.name, 
                                                                prop_from_self = prop_from_self,
                                                                prop_inherited = prop_inherited, 
                                                                comment = comment,
                                                                enum_values = self.enum_values,
                                                                )

        return proto_string
