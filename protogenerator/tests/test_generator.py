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
import rdflib
import utils.constants as constants
import utils.utils as utils
import core.schema_generator as schema_generator
import os


def test_generator():
    """Test the schema generator.

    Procedure:
        - Create root class, child classes and grandchildren to the root class.
        - Create enumeration and add values to it.
        - Create properties and attach them to each of the classes and 
          enumerations.
        - Create comments.
        - Add the range of each property.

    Verification:
        - Check if classes and enumerations have all their properties.
        - Check if child classes inherit properties of parent classes.
        - Check if the enumerations generate two messages as defined in the 
          specification.
        - Check if the enumerations inherit properties of 'enumeration' class.
        - Check if the enumerations have all values attached to it.
        - Check if properties point to classes in range and their child classes.
        - Check if comments are generated properly.
    """

    gen = schema_generator.SchemaGenerator('./tests/files/test_graph.nt')
    gen.write_proto('./tests/files/', 'schemaorg')

    expected_proto = open('./tests/files/test_schema.proto', 'r').read()
    out_proto = open('./tests/files/schema.proto', 'r').read()

    expected_descriptor = open(
        './tests/files/test_schema_descriptor.json',
        'r').read()
    out_descriptor = open('./tests/files/schema_descriptor.json', 'r').read()

    os.remove('./tests/files/schema.proto')
    os.remove('./tests/files/schema_descriptor.json')

    assert out_proto == expected_proto, 'Error in schema proto.'
    assert out_descriptor == expected_descriptor, 'Error in schema descriptor.'
