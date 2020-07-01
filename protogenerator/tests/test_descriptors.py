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
    """Test the property descriptor.

    Procedure:
        - Create a list of defined classes.
        - Create a list of field types that include defined classes, undefined classes and datatypes.
        - Create a property descriptor from the class_list and field_list.
        - Create multiline comments to be added.
        - Call to_proto function along with comments to get the protobuf code in string format.
    
    Verification:
        - Check if the classes are sorted in alphabetical order.
        - Check if the class has a (type) option with value 'Property'.
        - Check if multiline comments are properly formatted.
        - Check if datatypes are mapped to their corresponding proto primitves.
        - Check if undefined classes are converted to string.
        - Check if all defined classes are used as such.
        - Check if all fields are enclosed inside a oneof.

    """

    property_name = "foo"

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

    p = property_descriptor.PropertyDescriptor(property_name, field_types, class_list)
    output = p.to_proto(comment)

    expected = " ".join(expected.split())
    output = " ".join(output.split())

    assert output == expected, "Test for Property Descriptor has failed."


def test_class_descriptor():
    """Test the class descriptor.

    Procedure:
        - Create a list of field_types
        - The field type shud be mapped to their parents using utils.PropertyToParent class.
        - Create a class descriptor from the field_list.
        - Create multiline comments to be added.
        - Call to_proto function along with comments to get the protobuf code in string format.
    
    Verification:
        - Check if the first field is id and is a singular field.
        - Check if the class has a (type) option with value as the name of the class.
        - Check if multiline comments are properly formatted.
        - Check if the properties that are not inherited appear before the properties that are inherited.
        - Check if the all the properties that belong to same parent appear together..
        - Check if all the properties are repeated fields.
        - Check if every property have (json_name) option with value as the name of property.
    
    """

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

    c = class_descriptor.ClassDescriptor(class_name, field_types)
    output = c.to_proto(comment)

    expected = " ".join(expected.split())
    output = " ".join(output.split())

    assert output == expected, "Test for Class Descriptor has failed."

def test_enum_descriptor():
    """Test the enum descriptor.

    Procedure:
        - Create a list of field_types
        - The field type shud be mapped to their parents using utils.PropertyToParent class.
        - Create a list values that enumeration can have
        - Create a enum descriptor from the field_list and enum_values.
        - Create multiline comments to be added.
        - Call to_proto function along with comments to get the protobuf code in string format.
    
    Verification:
        - Check if two messages are generated.
        - Check if the first message has a nested enum definition.
        - Check if the nested enum defenition has all the values in enum_values along with default unknown value,
        - Check if the every value in enum definition has a option (schemaorg_value) pointing to schem.org url.
        - Check the following for first message
            * Check if the first field is id and is a singular field.
            * Check if the message has a (type) option with value as the name of the class.
            * Check if multiline comments are properly formatted.
            * Check if the properties that are not inherited appear before the properties that are inherited.
            * Check if the all the properties that belong to same parent appear together..
            * Check if all the properties are repeated fields.
            * Check if every property have (json_name) option with value as the name of property.
        - Check the following for second message.
            * Check if the first field is the enum defined in first message.
            * Check if the second field is the first message itself.
            * Check if the message has a (type) option with value as 'EnumWrapper'.
            * Check if all fields are enclosed inside a oneof.
        
    """
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

    e = enum_descriptor.EnumDescriptor(class_name, field_types,enum_values)
    output = e.to_proto(comment)

    expected = " ".join(expected.split())
    output = " ".join(output.split())

    assert output == expected, "Test for Enum Descriptor has failed."

