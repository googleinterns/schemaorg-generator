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
from jinja2 import Environment, FileSystemLoader
from typing import List
from utils.utils import PropertyToParent as PropertyToParent


class ClassDescriptor:
    """The ClassDescriptor generates protocol buffer code for schema class.

    Args:
        name (str): Name of the schema class.
        field_types (list[PropertyToParent]): The schema properties that belong
                                              to the schema class.

    Attributes:
        name (str): Name of the schema class.
        field_types (list[PropertyToParent]): The schema properties that belong
                                              to the schema class.
    """

    def __init__(self, name: str, field_types: List[PropertyToParent]):

        assert isinstance(name, str), "Invalid parameter 'name' must be 'str'."
        assert isinstance(
            field_types, list), "Invalid parameter 'field_types' must be 'list'."

        for x in field_types:
            assert isinstance(
                x, utils.PropertyToParent), "Every member of 'field_types' must be 'utils.PropertyToParent'."

        self.name = name
        self.field_types = field_types

    def to_proto(self, comment: str) -> str:
        """Return proto code for the schema class.

        Args:
            comment (str): The comment to be added to the code.

        Returns:
            str: The proto code for the schema class as a string.
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
        prop_inherited = collections.OrderedDict(
            sorted(prop_inherited.items()))

        file_loader = FileSystemLoader('./core/templates')
        env = Environment(
            loader=file_loader,
            trim_blocks=True,
            lstrip_blocks=True)
        env.globals['get_property_name'] = utils.get_property_name
        env.globals['to_snake_case'] = utils.to_snake_case
        env.globals['sorted'] = sorted

        comment = '// ' + comment.replace('\n', '\n// ')
        proto_string = env.get_template('class.txt').render(
            name=self.name,
            prop_from_self=prop_from_self,
            prop_inherited=prop_inherited,
            comment=comment)

        return proto_string
