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
import rdflib

def test_to_snake_case():
    ip1 = "NameName"
    op1 = "name_name"

    ip2 = "NAMEName"
    op2 = "name_name"

    ip3 = "nameName"
    op3 = "name_name"

    ip4 = "nameABCName"
    op4 = "name_abc_name"

    assert utils.to_snake_case(ip1) == op1, "Test pascal case."
    assert utils.to_snake_case(ip2) == op2, "Test pascal case with multiple upper case at start."
    assert utils.to_snake_case(ip3) == op3, "Test camel case."
    assert utils.to_snake_case(ip4) == op4, "Test camel case with multiple upper case at middle."


def test_get_property_name():
    ip1 = "name"
    op1 = "NameProperty"

    ip2 = "Name"
    op2 = "NameProperty"

    ip3 = "nameProperty"
    op3 = "NamePropertyProperty"

    assert utils.get_property_name(ip1) == op1, "Test lower case."
    assert utils.get_property_name(ip2) == op2, "Test pascal case."
    assert utils.get_property_name(ip3) == op3, "Test camel case."

def test_get_enum_value_name():

    ip1 = "enumValue"
    op1 = "ENUM_VALUE"

    ip2 = "EnumValue"
    op2 = "ENUM_VALUE"

    ip3 = "ENUMValue"
    op3 = "ENUM_VALUE"

    ip4 = "EnumABCValue"
    op4 = "ENUM_ABC_VALUE"

    assert utils.get_enum_value_name(ip1) == op1, "Test camel case."
    assert utils.get_enum_value_name(ip2) == op2, "Test pascal case."
    assert utils.get_enum_value_name(ip3) == op3, "Test pascal case with multiple upper case at start."
    assert utils.get_enum_value_name(ip4) == op4, "Test pascal case with multiple upper case at middle."

def test_strip_url():

    ip1 = "http://abc.com/entity"
    op1 = "entity"

    ip2 = "entity"
    op2 = "entity"

    ip3 = "abc.com/entity"
    op3 = "entity"


    ip4 = "http://abc.com/sub/entity"
    op4 = "entity"

    assert utils.strip_url(ip1) == op1, "Test a normal URL."
    assert utils.strip_url(ip2) == op2, "Test a non URL."
    assert utils.strip_url(ip3) == op3, "Test a URL without protocol."
    assert utils.strip_url(ip4) == op4, "Test a nested URL."
    
def test_get_class_type():

    class_list = {"randomClass", "RandomClass"}

    ip1 = "RandomClass"
    op1 = "RandomClass"

    ip2 = "randomClass"
    op2 = "randomClass"

    ip3 = "randomclass"
    op3 = "string"

    ip4 = "Text"
    op4 = "string"

    ip5 = "Number"
    op5 = "double"
    
    ip6 = "Float"
    op6 = "double"

    ip7 = "Integer"
    op7 = "int64"

    ip8 = "URL"
    op8 = "string"

    ip9 = "Boolean"
    op9 = "bool"

    assert utils.get_class_type(ip1, class_list) == op1, "Test if for a defined class the class name is returned."
    assert utils.get_class_type(ip2, class_list) == op2, "Test if for a defined class the class name is returned."
    assert utils.get_class_type(ip3, class_list) == op3, "Test if for an undefined class the string is returned."
    assert utils.get_class_type(ip4, class_list) == op4, "Test if Text is mapped to string."
    assert utils.get_class_type(ip5, class_list) == op5, "Test if Number is mapped to double."
    assert utils.get_class_type(ip6, class_list) == op6, "Test if Float is mapped to double."
    assert utils.get_class_type(ip7, class_list) == op7, "Test if Integer is mapped to int64."
    assert utils.get_class_type(ip8, class_list) == op8, "Test if URL is mapped to string."
    assert utils.get_class_type(ip9, class_list) == op9, "Test if Boolean is mapped to bool."

def test_add_url():

    ip1 = "abc"
    op1 = rdflib.URIRef("http://schema.org/abc")

    ip2 = "Abc"
    op2 = rdflib.URIRef("http://schema.org/Abc")

    assert utils.add_url(ip1) == op1, "Test string"
    assert utils.add_url(ip2) == op2, "Test string"

def test_topological_sort():

    graph = dict()
    for i in range(6):
        graph[i] = set()
    
    graph[2].add(3)
    graph[3].add(1)
    graph[4].add(0)
    graph[4].add(1)
    graph[5].add(0)
    graph[5].add(2)

    answer = [5, 4, 2, 3, 1, 0]

    assert utils.topological_sort(graph) == answer, "Test toplogical_sort."

def test_get_children():

    graph = dict()
    answer = dict()

    for i in range(15):
        graph[i] = set()
        answer[i] = set()
        
        if 2*i + 1 < 15:
            parent = i 
            graph[i].add(2*i + 1)
            while(parent):
                answer[parent].add(2*i + 1)
                parent = int((parent-1)/2)
            answer[0].add(2*i + 1)
            

        if 2*i + 2 < 15:
            parent = i 
            graph[i].add(2*i + 2)
            while(parent):
                answer[parent].add(2*i + 2)
                parent = int((parent-1)/2)
            answer[0].add(2*i + 2)
    

    assert utils.get_children(graph) == answer, "Test get_children."

