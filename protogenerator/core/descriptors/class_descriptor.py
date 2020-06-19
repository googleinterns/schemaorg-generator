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
import collections


class ClassDescriptor:
    """The ClassDescriptor generates protocol buffer code for schema class.

    Args:
        name (str): Name of the schema class.
        field_types (list[utils.PropertyToParent]): The schema properties that belong to the schema class.
        package_name (str): Package name for the proto code.

    Attributes:
        name (str): Name of the schema class.
        field_types (list[utils.PropertyToParent]): The schema properties that belong to the schema class.
        package_name (str): Package name for the proto code.
    """

    def __init__(self, name, field_types, package_name):

        assert isinstance(name, str), "Invalid parameter 'name' must be 'str'."
        assert isinstance(
            package_name, str), "Invalid parameter 'package_name' must be 'str'."
        assert isinstance(
            field_types, list), "Invalid parameter 'field_types' must be 'list'."

        for x in field_types:
            assert isinstance(
                x, utils.PropertyToParent), "Every member of 'field_types' must be 'utils.PropertyToParent'."

        self.name = name
        self.field_types = field_types
        self.package_name = package_name

    def to_proto(self, add_header, add_import, comment):
        """Return proto code for the schema class.

        Args:
            add_header (bool): If header of proto file needs to be added.
            add_import (bool): If import statements need to be added.
            comment (string): The comment to be added to the code.

        Returns:
            proto_string: The proto code for the schema class as a string.
        """
        assert isinstance(
            add_header, bool), "Invalid parameter 'add_header' must be 'bool'."
        assert isinstance(
            add_import, bool), "Invalid parameter 'add_import' must be 'bool'."
        assert isinstance(
            comment, str), "Invalid parameter 'comment' must be 'str'."

        proto_string = ''

        if add_header:
            proto_string += "syntax = \"proto3\"; \n"
            proto_string += 'package {}; \n\n'.format(self.package_name)

        if add_import:
            proto_string += "import \"google/protobuf/descriptor.proto\";\n"
            proto_string += "import \"protoOptions/message_options.proto\";\n\n"

            s = set(self.field_types)

            # Every unique field type is imported without any exclusion because
            # every property is modelled as a message and needs to be imported.
            for x in s:
                proto_string += "import \"properties/{}.proto\"; \n".format(
                    utils.to_snake_case(utils.get_property_name(x)))

            proto_string += '\n'
        
        proto_string += "// " + comment.replace("\n", "\n// ") + "\n"
        proto_string += 'message {} {{ \n'.format(self.name)
        proto_string += "\toption (type) = \"{}\";\n".format(self.name)

        field_number = 1

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

        if len(prop_from_self) > 0:
            proto_string += "\n\t// Properties from " + self.name + ".\n"

        for x in prop_from_self:
            field_number = field_number if field_number < 19000 or field_number > 20000 else 20000

            proto_string += "\trepeated {} {} = {} [json_name = \"{}\"]; \n".format(
                utils.get_property_name(x), utils.to_snake_case(x), field_number, x)
            field_number = field_number + 1
        
        for ky in prop_inherited:
            props = sorted(prop_inherited[ky])

            if len(props) > 0:
                proto_string += "\n\t// Properties from " + ky + ".\n"

            for x in props:
                field_number = field_number if field_number < 19000 or field_number > 20000 else 20000

                proto_string += "\trepeated {} {} = {} [json_name = \"{}\"]; \n".format(
                    utils.get_property_name(x), utils.to_snake_case(x), field_number, x)
                field_number = field_number + 1

        proto_string += '}\n'

        return proto_string
