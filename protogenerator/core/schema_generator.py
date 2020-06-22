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
import core.descriptors.class_descriptor as class_descriptor
import core.descriptors.property_descriptor as property_descriptor
import core.descriptors.enum_descriptor as enum_descriptor
import utils.utils as utils
import utils.constants as constants
import json
import collections
from bs4 import BeautifulSoup

class SchemaGenerator():
    """The SchemaGenerator is a class that generates protocol buffer code given
    a schema.

    Args:
        src_file_path (str): Path to the file containing schema.

    Attributes:
        graph (rdflib.Graph): Graph which is result of parsing the schema.
    """

    def __init__(self, src_file_path):

        assert isinstance(
            src_file_path, str), "Invalid parameter 'src_file_path' must be 'str'."

        self.graph = rdflib.Graph()
        self.graph.parse(
            src_file_path,
            format=rdflib.util.guess_format(src_file_path))

    def write_proto(self, dst_path, package_name):
        """Write the protobuf code for the graph to file.

        Args:
            dst_path (str): Path to the output directory where code has to be written.
            package_name (str): Package name for the proto code.
        """

        assert isinstance(
            dst_path, str), "Invalid parameter 'dst_path' must be 'str'."
        outFile = open(dst_path+"schema.proto", 'w')

        class_to_prop, prop_to_class, enumerations = self.__get_values()

        proto_string = ''
        proto_string += self.__get_header(package_name)
        proto_string += self.__get_options()
        proto_string += self.__get_datatypes()
        proto_string += self.__class_to_proto(
            class_to_prop, enumerations, package_name)
        proto_string += self.__enum_to_proto(
            class_to_prop, enumerations, package_name)
        proto_string += self.__prop_to_proto(prop_to_class,set(class_to_prop.keys()), package_name)

        outFile.write(proto_string)
        outFile.close()

        outFile = open(dst_path+"schema_descriptor.json", 'w')
        json_descriptor = self.__get_json_descriptor(class_to_prop, prop_to_class, enumerations)
        json.dump(json_descriptor, outFile, indent=4)
        outFile.close()

    def __class_to_proto(self, class_to_prop, enumerations, package_name):
        """Call ClassDescriptor.to_proto() and get proto code for every schema
        class.

        Args:
            class_to_prop (dict(set): Dictionary containing set of properties for every class.
            enumerations (set): Set containing the enumerations in the schema.
            package_name (str): Package name for the proto code.

        Returns:
            proto_class: The proto code for all the schema classes in class_to_prop as a string.
        """
        proto_class = '// Definition of classes begin here.\n\n'

        for x in sorted(class_to_prop.keys()):
            if x not in enumerations and x not in constants.schema_datatypes and x not in constants.schema_primitives:
                
                comment = ""

                for _, _, c in self.graph.triples((utils.add_url(x), constants.schema_constants['Comment'], None)):
                    comment += c

                soup = BeautifulSoup(comment, "html.parser")
                comment = soup.get_text()

                proto_class += class_descriptor.ClassDescriptor(x, list(class_to_prop[x]), package_name).to_proto(False, False, comment)
                proto_class += '\n'

        return proto_class

    def __prop_to_proto(self, prop_to_class, class_list, package_name):
        """Call PropertyDescriptor.to_proto() and get proto code for every
        schema property.

        Args:
            prop_to_class (dict(set)): Dictionary containing range of class/datatypes for every property.
            class_list (set): Set of defined classes.
            package_name (str): Package name for the proto code.

        Returns:
            proto_property: The proto code for all the schema property in prop_to_class as a string.
        """
        proto_property = '// Definition of properties begin here.\n\n'

        for x in sorted(prop_to_class.keys()):
            if len(prop_to_class[x]) > 0:
                comment = ""
                for _, _, c in self.graph.triples((utils.add_url(x), constants.schema_constants['Comment'], None)):
                    comment += c

                soup = BeautifulSoup(comment, "html.parser")
                comment = soup.get_text()

                proto_property += property_descriptor.PropertyDescriptor(x, list(prop_to_class[x]),list(class_list), package_name).to_proto(False, False, comment)
                proto_property += '\n'

        return proto_property

    def __enum_to_proto(self, class_to_prop, enumerations, package_name):
        """Call EnumDescriptor.to_proto() and get proto code for every schema
        enumeration.

        Args:
            class_to_prop (dict(set): Dictionary containing set of properties for every class.
            enumerations (set): Set containing the enumerations in the schema.
            package_name (str): Package name for the proto code.

        Returns:
            proto_enum: The proto code for all the schema enumerations in enumerations as a string.
        """

        proto_enum = '// Definition of enumerations begin here.\n\n'

        for x in sorted(enumerations):
            enum_values = set()

            for ev, _, _ in self.graph.triples(
                    (None, constants.schema_constants['Type'], utils.add_url(x))):
                enum_values.add(utils.strip_url(ev))

            comment = ""
            for _, _, c in self.graph.triples((utils.add_url(x), constants.schema_constants['Comment'], None)):
                comment += c
            
            soup = BeautifulSoup(comment, "html.parser")
            comment = soup.get_text()

            proto_enum += enum_descriptor.EnumDescriptor(x,list(
                class_to_prop[x]), list(enum_values), package_name).to_proto(False, False, comment)
            proto_enum += '\n'

        return proto_enum

    def __get_values(self):
        """Call utils.toplogical_sort(), compress the inheritance heirarchy and
        return mappings between schema classes, schema properties and schema
        enumerations.

        Returns:
            class_to_prop (dict(set): Dictionary containing set of properties for every class.
            prop_to_class (dict(set): Dictionary containing range of class/datatypes for every property.
            enumerations (set): Set containing the enumerations in the schema.
        """

        class_to_prop = dict()
        inheritance_graph = dict()

        for class_name, _, _ in self.graph.triples(
                (None, constants.schema_constants['Type'], constants.schema_constants['Class'])):
            class_to_prop[utils.strip_url(class_name)] = set()

            for property_name, _, _ in self.graph.triples(
                    (None, constants.schema_constants['domainIncludes'], class_name)):
                prop = utils.PropertyToParent(utils.strip_url(property_name), utils.strip_url(class_name))
                class_to_prop[utils.strip_url(class_name)].add(prop)

        for class_name, _, _ in self.graph.triples(
                (None, constants.schema_constants['Type'], constants.schema_constants['Class'])):

            if class_name not in inheritance_graph:
                inheritance_graph[class_name] = set()

            for _, _, parent_class in self.graph.triples(
                    (class_name, constants.schema_constants['subClassOf'], None)):

                if parent_class not in inheritance_graph:
                    inheritance_graph[parent_class] = set()

                inheritance_graph[parent_class].add(class_name)

        topsort_order = utils.topological_sort(inheritance_graph)

        for class_name in topsort_order:
            for _, _, parent_class in self.graph.triples(
                    (class_name, constants.schema_constants['subClassOf'], None)):
                if utils.strip_url(parent_class) in class_to_prop:
                    class_to_prop[utils.strip_url(class_name)] = class_to_prop[utils.strip_url(class_name)] | class_to_prop[utils.strip_url(parent_class)]

        enumerations = set()

        for enum, _, _ in self.graph.triples(
                (None, constants.schema_constants['subClassOf'], constants.schema_constants['Enumeration'])):
            enumerations.add(utils.strip_url(enum))

        class_to_children = utils.get_children(inheritance_graph)

        # Temporary Code
        class_to_children[rdflib.URIRef('http://schema.org/Audience')].add(rdflib.URIRef("http://schema.org/Researcher"))
        class_to_prop["SteeringPositionValue"] = class_to_prop["Enumeration"]
        class_to_prop["DriveWheelConfigurationValue"] = class_to_prop["Enumeration"]
        enumerations.add("SteeringPositionValue")
        enumerations.add("DriveWheelConfigurationValue")
        # End of temporary code

        prop_to_class = dict()

        for property_name, _, _ in self.graph.triples(
                (None, constants.schema_constants['Type'], constants.schema_constants['Property'])):
            prop_to_class[utils.strip_url(property_name)] = set()

            for _, _, class_name in self.graph.triples(
                    (property_name, constants.schema_constants['rangeIncludes'], None)):
                prop_to_class[utils.strip_url(property_name)].add(utils.strip_url(class_name))
                if class_name in class_to_children:
                    prop_to_class[utils.strip_url(property_name)] = prop_to_class[utils.strip_url(property_name)] | set(map(utils.strip_url, class_to_children[class_name]))

                if class_name == constants.schema_constants['Number']:
                    prop_to_class[utils.strip_url(property_name)].add(
                        utils.strip_url(constants.schema_constants['Integer']))
                    prop_to_class[utils.strip_url(property_name)].add(
                        utils.strip_url(constants.schema_constants['Float']))

                if class_name == constants.schema_constants['Text']:
                    prop_to_class[utils.strip_url(property_name)].add(
                        utils.strip_url(constants.schema_constants['URL']))

        return class_to_prop, prop_to_class, enumerations

    def __get_header(self, package_name):
        """Return the header for proto code file.

        Args:
            package_name (str): Package name for the proto code.

        Returns:
            proto_header: The proto code of header as a string.
        """

        proto_header = ''
        proto_header += "syntax = \"proto3\"; \n"
        proto_header += 'package {}; \n\n'.format(package_name)
        proto_header += "import \"google/protobuf/descriptor.proto\";\n\n"
        return proto_header

    def __get_options(self):
        """Return the options for JSONLD serializer.

        Returns:
            proto_options: The proto code of options for JSONLD serializer as a string.
        """
        proto_options = ''
        proto_options += 'extend google.protobuf.MessageOptions {\n'
        proto_options += '\toptional string type = 50001;\n'
        proto_options += '}\n\n'
        proto_options += 'extend google.protobuf.EnumValueOptions {\n'
        proto_options += '\toptional string schemaorg_value = 50002;\n'
        proto_options += '}\n\n'
        return proto_options

    def __get_datatypes(self):
        """Return the datatypes in accordance with schemaorg.

        Returns:
            proto_datatypes: The proto code of datatypes in accordance with schemaorg as a string.
        """
        proto_datatypes = ''
        proto_datatypes += 'message DateTime {\n'
        proto_datatypes += "\toption (type) = \"DatatypeDateTime\";\n"
        proto_datatypes += '\tDate date = 1;\n'
        proto_datatypes += '\tTime time = 2;\n'
        proto_datatypes += '}\n\n'
        proto_datatypes += 'message Date {\n'
        proto_datatypes += "\toption (type) = \"DatatypeDate\";\n"
        proto_datatypes += '\tint32 year = 1;\n'
        proto_datatypes += '\tint32 month = 2;\n'
        proto_datatypes += '\tint32 day = 3;\n'
        proto_datatypes += '\tTimezone timezone = 4;\n'
        proto_datatypes += '}\n\n'
        proto_datatypes += 'message Time {\n'
        proto_datatypes += "\toption (type) = \"DatatypeTime\";\n"
        proto_datatypes += '\tint32 hours = 1;\n'
        proto_datatypes += '\tint32 minutes = 2;\n'
        proto_datatypes += '\tint32 seconds = 3;\n'
        proto_datatypes += '\tTimezone timezone = 4;\n'
        proto_datatypes += '}\n\n'
        proto_datatypes += 'message Timezone {\n'
        proto_datatypes += '\tstring iana_id = 1;\n'
        proto_datatypes += '}\n\n'
        proto_datatypes += 'message Duration {\n'
        proto_datatypes += '\toption (type) = "DatatypeDuration";\n'
        proto_datatypes += '\tint64 seconds = 1;\n'
        proto_datatypes += '}\n\n'
        proto_datatypes += 'message Distance {\n'
        proto_datatypes += '\toption (type) = "DatatypeQuantitative";\n'
        proto_datatypes += '\tdouble value = 1;\n'
        proto_datatypes += '\tstring unit = 2;\n'
        proto_datatypes += '}\n\n'
        proto_datatypes += 'message Energy {\n'
        proto_datatypes += '\toption (type) = "DatatypeQuantitative";\n'
        proto_datatypes += '\tdouble value = 1;\n'
        proto_datatypes += '\tstring unit = 2;\n'
        proto_datatypes += '}\n\n'
        proto_datatypes += 'message Mass {\n'
        proto_datatypes += '\toption (type) = "DatatypeQuantitative";\n'
        proto_datatypes += '\tdouble value = 1;\n'
        proto_datatypes += '\tstring unit = 2;\n'
        proto_datatypes += '}\n\n'

        return proto_datatypes

    def __get_json_descriptor(self, class_to_prop, prop_to_class, enumerations):
        """Return a json descriptor for the given schema.

        Args:
            class_to_prop (dict(set): Dictionary containing set of properties for every class.
            prop_to_class (dict(set): Dictionary containing range of class/datatypes for every property.
            enumerations (set): Set containing the enumerations in the schema.

        Returns:
            json_descriptor: The json descriptor for the schema.
        """

        defined_classes = set(class_to_prop.keys())
        total_classes = set()

        for _,_,property_name in self.graph.triples((None, utils.constants.schema_constants["rangeIncludes"], None)):
            total_classes.add(utils.strip_url(property_name))

        undefined_classes = total_classes.difference(defined_classes)
        undefined_classes = undefined_classes | set(utils.constants.schema_primitives.keys())

        message_descriptor = {}

        for x in sorted(class_to_prop.keys()):
            if x not in enumerations and x not in constants.schema_datatypes and x not in constants.schema_primitives:
                o = {}
                o["@type"] = utils.strip_url(x)

                prop_from_self = list()
                prop_inherited = dict()

                o["fields"] = list()
                o["fields"].append("@id")

                for p in class_to_prop[x]:
                    if p.parent == x:
                        prop_from_self.append(p.name)
                    else:
                        if p.parent not in prop_inherited:
                            prop_inherited[p.parent] = list()
                        
                        prop_inherited[p.parent].append(p.name)

                prop_from_self = sorted(prop_from_self)
                prop_inherited = collections.OrderedDict(sorted(prop_inherited.items()))

                for p in prop_from_self:
                    o["fields"].append(p)

                for ky in prop_inherited:
                    props = sorted(prop_inherited[ky])
                    o["fields"].extend(props)

                message_descriptor[x] = o

        
        for x in sorted(prop_to_class.keys()):
            if len(prop_to_class[x])>0:
                o = {}
                o["@type"] = "Property"
                o["fields"] = sorted(list(prop_to_class[x]))
                message_descriptor[x] = o

  
        for x in sorted(enumerations):
            enum_values = set()

            for ev, _, _ in self.graph.triples((None, constants.schema_constants['Type'], x)):
                enum_values.add(ev)
            
            o = {}
            o["@type"] = "EnumWrapper"
            o["values"] = sorted(list(enum_values))
            o["values"].insert(0, "Unknown")
            o["fields"] = ["id", x + "Class"]

            o2 = {}
            o2["@type"] = x
            prop_from_self = list()
            prop_inherited = dict()

            o2["fields"] = list()
            o2["fields"].append("@id")

            for p in class_to_prop[x]:
                if p.parent == x:
                    prop_from_self.append(p.name)
                else:
                    if p.parent not in prop_inherited:
                        prop_inherited[p.parent] = list()
                    
                    prop_inherited[p.parent].append(p.name)

            prop_from_self = sorted(prop_from_self)
            prop_inherited = collections.OrderedDict(sorted(prop_inherited.items()))

            for p in prop_from_self:
                o2["fields"].append(p)

            for ky in prop_inherited:
                props = sorted(prop_inherited[ky])
                o2["fields"].extend(props)

            
            message_descriptor[x] = o
            message_descriptor[x + "Class"] = o2

        
        message_descriptor["Date"] = {}
        message_descriptor["Date"]["@type"] = "DatatypeDate"

        message_descriptor["DateTime"] = {}
        message_descriptor["DateTime"]["@type"] = "DatatypeDateTime"

        message_descriptor["Time"] = {}
        message_descriptor["Time"]["@type"] = "DatatypeTime"

        message_descriptor["Duration"] = {}
        message_descriptor["Duration"]["@type"] = "DatatypeDuration"

        message_descriptor["Distance"] = {}
        message_descriptor["Distance"]["@type"] = "DatatypeQuantitative"

        message_descriptor["Energy"] = {}
        message_descriptor["Energy"]["@type"] = "DatatypeQuantitative"

        message_descriptor["Mass"] = {}
        message_descriptor["Mass"]["@type"] = "DatatypeQuantitative"


        json_descriptor = {}
        json_descriptor["messages"] = message_descriptor
        json_descriptor["primitives"] = list(sorted(undefined_classes))



        return json_descriptor
