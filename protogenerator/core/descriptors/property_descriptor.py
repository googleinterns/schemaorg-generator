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
from jinja2 import Environment, FileSystemLoader


def get_import_statement(x):
    """Return import statement for a particular class/datatype is it needs to be imported.

    Args:
        x (string): Name of message which has to be imported/used.

    Returns:
        string: Import statement if the message type need to be imported else empty string.
    """

    if x in constants.schema_primitives:
        return ''
    elif x in constants.proto_primitives:
        return ''
    elif x in constants.schema_datatypes:
        return "import \"datatypes/{}.proto\"; \n".format(
            utils.to_snake_case(x))
    else:
        return "import \"classes/{}.proto\"; \n".format(utils.to_snake_case(x))


class PropertyDescriptor:
    """The PropertyDescriptor generates protocol buffer code for schema property.

    Args:
        name (str): Name of the schema property.
        field_types (list[str]): The schema classes/datatypes that are included in range of schema property.
        class_list (list(str)): List of defined classes.

    Attributes:
        name (str): Name of the schema property.
        field_types (list[str]): The schema classes/datatypes that are included in range of schema property.
        class_list (list(str)): List of defined classes.
    """

    def __init__(self, name, field_types, class_list):

        assert isinstance(name, str), "Invalid parameter 'name' must be 'str'."
        assert isinstance(
            field_types, list), "Invalid parameter 'field_types' must be 'list'."
        assert isinstance(
            class_list, list), "Invalid parameter 'class_list' must be 'list'."

        for x in field_types:
            assert isinstance(
                x, str), "Every member of 'field_types' must be 'str'."

        for x in class_list:
            assert isinstance(
                x, str), "Every member of 'class_list' must be 'str'."

        self.name = name
        self.field_types = field_types
        self.class_list = class_list

    def to_proto(self, comment):
        """Return proto code for the schema property.

        Args:
            comment (string): The comment to be added to the code.

        Returns:
            proto_string: The proto code for the schema property as a string.
        """

        assert isinstance(
            comment, str), "Invalid parameter 'comment' must be 'str'."
        
        file_loader = FileSystemLoader('./core/templates')
        env = Environment(loader=file_loader, trim_blocks=True, lstrip_blocks=True)
        env.globals["get_class_type"] = utils.get_class_type
        env.globals["to_snake_case"] = utils.to_snake_case

        comment = "// " + comment.replace("\n", "\n// ")
        proto_string = env.get_template('property.txt').render(
                                                            name = utils.get_property_name(self.name), 
                                                            field_types = sorted(self.field_types), 
                                                            class_list = self.class_list, 
                                                            comment=comment)

        return proto_string
