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
import core.descriptors.class_descriptor as class_descriptor
import core.descriptors.enum_descriptor as enum_descriptor
import core.descriptors.property_descriptor as property_descriptor
import utils.utils as utils

def test_property_descriptor():

    property_name = "foo"
    package_name = "schemaorg"

    class_list = [
        "LoremIpsum",
        "Dolor",
        "Amet"
    ]

    field_types = [
        "LoremIpsum",       # Defined class
        "Ipsum",            # Undefined class
        "DolorQuisque",     # Defined class
        "Sit",              # Undefined class
        "Amet",             # Defined class
        "Text",             # Datatype
        "URL",              # Datatype
        "Boolean"           # Datatype
    ]

    comment = "First line of comment.\nSecond line of comment."

    expected ="""
    // First line of comment.
    // Second line of comment.
    message FooProperty { 
        option (type) = "Property";
        oneof values {
            Amet amet = 1; 
            bool boolean = 2; 
            string dolor_quisque = 3; 
            string ipsum = 4; 
            LoremIpsum lorem_ipsum = 5; 
            string sit = 6; 
            string text = 7; 
            string url = 8; 
        }
    }
    """

    p = property_descriptor.PropertyDescriptor(property_name, field_types, class_list, package_name)
    output = p.to_proto(comment)

    expected = " ".join(expected.split())
    output = " ".join(output.split())

    assert output == expected, "Test for Property Descriptor has failed."


def test_class_descriptor():

    package_name = "schemaorg"
    class_name = "Foo"

    field_types = [
        utils.PropertyToParent("LoremIpsum", "Thing"),  # Property from parent
        utils.PropertyToParent("Ipsum", "Movie"),       # Property from parent
        utils.PropertyToParent("DolorQuisque", "Foo"),  # Property from self
        utils.PropertyToParent("Sit", "Thing"),         # Property from parent
        utils.PropertyToParent("Amet", "Foo")           # Property from self
    ]

    comment = "First line of comment.\nSecond line of comment."

    expected = """
    // First line of comment.
    // Second line of comment.
    message Foo { 
        option (type) = "Foo";

        // Properties from Foo.
        string id = 1 [json_name = "@id"]; 
        repeated AmetProperty amet = 2 [json_name = "Amet"];
        repeated DolorQuisqueProperty dolor_quisque = 3 [json_name = "DolorQuisque"];

        // Properties from Movie.
        repeated IpsumProperty ipsum = 4 [json_name = "Ipsum"];

        // Properties from Thing.
        repeated LoremIpsumProperty lorem_ipsum = 5 [json_name = "LoremIpsum"];
        repeated SitProperty sit = 6 [json_name = "Sit"];
    }
    """

    c = class_descriptor.ClassDescriptor(class_name, field_types, package_name)
    output = c.to_proto(comment)

    expected = " ".join(expected.split())
    output = " ".join(output.split())

    assert output == expected, "Test for Class Descriptor has failed."

def test_enum_descriptor():
    package_name = "schemaorg"
    class_name = "Foo"

    field_types = [
        utils.PropertyToParent("LoremIpsum", "Thing"),  
        utils.PropertyToParent("Ipsum", "Movie"),       
        utils.PropertyToParent("DolorQuisque", "Foo"),
        utils.PropertyToParent("Sit", "Thing"),       
        utils.PropertyToParent("Amet", "Foo")    
    ]

    enum_values = [
        "LoremValue",
        "IpsumValue",
        "Dolor",
        "AMET"
    ]

    comment = "First line of comment.\nSecond line of comment."

    expected = """
    // First line of comment.
    // Second line of comment.
    message FooClass { 
        option (type) = "Foo";

        enum Id {
            UNKNOWN = 0 [(schemaorg_value)="Unknown"];
            AMET = 1 [(schemaorg_value) = "https://schema.org/AMET"];
            DOLOR = 2 [(schemaorg_value) = "https://schema.org/Dolor"];
            IPSUM_VALUE = 3 [(schemaorg_value) = "https://schema.org/IpsumValue"];
            LOREM_VALUE = 4 [(schemaorg_value) = "https://schema.org/LoremValue"];
        }

        // Properties from Foo.
        string id = 1 [json_name = "@id"]; 
        repeated AmetProperty amet = 2 [json_name = "Amet"];
        repeated DolorQuisqueProperty dolor_quisque = 3 [json_name = "DolorQuisque"];

        // Properties from Movie.
        repeated IpsumProperty ipsum = 4 [json_name = "Ipsum"];

        // Properties from Thing.
        repeated LoremIpsumProperty lorem_ipsum = 5 [json_name = "LoremIpsum"];
        repeated SitProperty sit = 6 [json_name = "Sit"];
    }

    message Foo {
        option (type) = "EnumWrapper";
        oneof values {
            FooClass.Id id = 1;
            FooClass foo = 2;
        }
    }
    """

    e = enum_descriptor.EnumDescriptor(class_name, field_types,enum_values, package_name)
    output = e.to_proto(comment)

    expected = " ".join(expected.split())
    output = " ".join(output.split())

    assert output == expected, "Test for Enum Descriptor has failed."

