import re
import utils.constants as constants
import rdflib


def to_snake_case(x):
    """Return snake_case of x.

    Args:
        x (str): The string that has to be converted to snake case.

    Returns:
        x_s: Snake case of x.
    """

    x_s = x
    x_s = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', x_s)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', x_s).lower()


def get_property_name(x):
    """Return message name of property in proto.

    Args:
        x (str): The name of property.

    Returns:
        x_name: Message name of property in proto .
    """

    x_name = x[0].upper()
    x_name += x[1:]
    x_name += 'Property'
    return x_name


def get_enum_value_name(x):
    """Return value name of enum value in proto.

    Args:
        x (str): The name of enum value.

    Returns:
        x_name: Value name of enum value in proto .
    """

    x_name = to_snake_case(x).upper()
    return x_name


def get_class_type(x, class_list):
    """Return message name of a class in proto. If the class is a schema
    primitive then the corresponding primitive datatype in proto is returned,
    else the name itself is returned.

    Args:
        x (str): The name of class.
        class_list (set(str)): All defined classes in schema.

    Returns:
        class_type: Type in proto.
    """
    class_type = ''
    if x in constants.schema_primitives:
        class_type = constants.schema_primitives[x]
    elif x in class_list:
        class_type = x
    else:
        class_type = "string"

    return class_type


def strip_url(x):
    """Return the name of the schema entity after stripping url.

    Args:
        x (str): URL of the enitity.

    Returns:
        x_strip: The name of entity.
    """

    x_strip = str(x).split('/')[-1]
    return x_strip


def add_url(x):
    """Return the url of the schema entity after adding url.

    Args:
        x (str): The name of the enitity.

    Returns:
        url: The url of entity.
    """

    url = rdflib.URIRef('http://schema.org/' + x)
    return url


def topological_sort(graph):
    """Call topological_sort_util() and return the toplogically sorted answer.

    Args:
        graph (dict(string, set)): Dictionary representing the graph.

    Returns:
        answer: The toplogically sorted nodes as a list.
    """

    seen = set()
    answer = []

    for x in graph:
        if x not in seen:
            seen = topological_sort_util(x, graph, seen, answer)

    return answer


def topological_sort_util(src, graph, seen, answer):
    """Do topological sorting.

    Args:
        src (str): Source/Current node of the graph.
        graph (dict(string, set)): Dictionary representing the graph.
        seen (set): Set of seen nodes.
        answer (list): List where nodes should be put in order.

    Returns:
        seen (set): Set of seen nodes.
    """

    seen.add(src)

    for i in graph[src]:
        if i not in seen:
            seen = topological_sort_util(i, graph, seen, answer)
    answer.insert(0, src)

    return seen


def get_children(graph):
    """Return a mapping between class to it childrens.

    Args:
        graph (dict(string, set)): Dictionary representing the graph.

    Returns:
        class_to_children(dict(set)): Dictionary containing mapping between class to its children.
    """

    class_to_children = {}
    seen = set()

    for x in graph.keys():
        if x not in seen:
            class_to_children, seen = get_children_util(x, graph, seen, class_to_children)
    
    return class_to_children

def get_children_util(src, graph, seen, class_to_children):
    """Helper function to assist get_childern in mapping classes and their children.

    Args:
        src (str): Source/Current node of the graph.
        graph (dict(string, set)): Dictionary representing the graph.
        seen (set): Set of seen nodes.
        class_to_children(dict(set)): Dictionary containing mapping between class to its children.

    Returns:
        class_to_children(dict(set)): Dictionary containing mapping between class to its children.
        seen (set): Set of seen nodes.
    """

    seen.add(src)
    
    if src not in class_to_children:
        class_to_children[src] = set()
    
    for i in graph[src]:
        class_to_children[src].add(i)
        if i not in seen:
            class_to_children, seen = get_children_util(i, graph, seen, class_to_children)
        
        class_to_children[src] = class_to_children[src] | class_to_children[i]
    
    return class_to_children, seen

class PropertyToParent():

    def __init__(self, name, parent):
        self.name = name
        self.parent = parent
    
    def __hash__(self):
        return hash(self.name)
    
    def __eq__(self, other):
        return self.name == other.name
