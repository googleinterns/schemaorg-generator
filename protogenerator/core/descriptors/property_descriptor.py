import utils.utils as utils
import utils.constants as constants


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
        package_name (str): Package name for the proto code.

    Attributes:
        name (str): Name of the schema property.
        field_types (list[str]): The schema classes/datatypes that are included in range of schema property.
        class_list (list(str)): List of defined classes.
        package_name (str): Package name for the proto code.
    """

    def __init__(self, name, field_types, class_list, package_name):

        assert isinstance(name, str), "Invalid parameter 'name' must be 'str'."
        assert isinstance(
            package_name, str), "Invalid parameter 'package_name' must be 'str'."
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
        self.package_name = package_name
        self.class_list = class_list

    def to_proto(self, add_header, add_import, comment):
        """Return proto code for the schema property.

        Args:
            add_header (bool): If header of proto file needs to be added.
            add_import (bool): If import statements need to be added.
            comment (string): The comment to be added to the code.

        Returns:
            proto_string: The proto code for the schema property as a string.
        """

        assert isinstance(
            add_header, bool), "Invalid parameter 'add_header' must be 'bool'."
        assert isinstance(
            add_import, bool), "Invalid parameter 'add_import' must be 'bool'."
        assert isinstance(
            comment, str), "Invalid parameter 'comment' must be 'str'."

        proto_string = ""

        if add_header:
            proto_string += "syntax = \"proto3\"; \n"
            proto_string += 'package {}; \n\n'.format(self.package_name)

        if add_import:
            proto_string += "import \"google/protobuf/descriptor.proto\";\n"
            proto_string += "import \"protoOptions/message_options.proto\";\n\n"

            s = set(self.field_types)

            for x in s:
                proto_string += get_import_statement(x)

            proto_string += '\n'

        proto_string += "// " + comment.replace("\n", "\n//") + "\n"
        proto_string += 'message {} {{ \n'.format(
            utils.get_property_name(self.name))
        proto_string += "\toption (type) = \"Property\";\n"
        proto_string += '\toneof values {\n'

        field_number = 1

        for x in sorted(self.field_types):
            field_number = field_number if field_number < 19000 or field_number > 20000 else 20000

            proto_string += '\t\t{} {} = {}; \n'.format(
                utils.get_class_type(x, self.class_list), utils.to_snake_case(x), field_number)
            field_number = field_number + 1

        proto_string += '\t}\n'
        proto_string += '}\n'

        return proto_string
