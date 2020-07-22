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
import json
import rdflib
import uuid
import os
import schemaorgutils.utils.constants as constants
import schemaorgutils.utils.utils as utils
from pyshacl import validate
from jinja2 import Environment, FileSystemLoader
from typing import Any


class SchemaValidator():
    """The SchemaValidator validates the entities against a constraints graph
    and generate a html report for the validation result.

    Attributes:
        reports (dict[list[ResultRow]]): A dictionary mapping list of all error
                                         results to an entity type.
        _constraints_file (str): The path to constraints file containing shacl
                                 validations.
        _report_file (str): The path to file where the output report has to be
                            generated.
        _position (int): The total number of entities validated.
        _is_closed (bool): The status of validator.
        _total (dict[str, int]): Number of total entities for a particular type.
    """

    def __init__(self, constraints_file: str, report_file: str):

        self.reports = dict()
        self._constraints_file = constraints_file
        self._report_file = report_file
        self._position = 0
        self._is_closed = False
        self._total = dict()

    def __add_ids(self, entity: Any) -> Any:
        """Add uids to every entity in the data graph to be validated.

        Args:
            entity (dict): The entity to which uids are to be added.

        Returns:
            dict: The entity after adding uids.
        """

        if not isinstance(entity, dict):
            return entity
        else:
            entity['@id'] = '/schemavalidator/' + str(uuid.uuid4())

            for key in sorted(entity.keys()):
                entity[key] = self.__add_ids(entity[key])

            return entity

    def add_entity(self, entity: dict) -> bool:
        """Add an entity that has to be validated.

        Args:
            entity (dict): The entity that has to be validated.

        Returns:
            bool: The conformance of entity to the constraints.
        """

        assert self._is_closed == False, 'Validator has already been closed.'

        typ = entity['@type']
        conforms = True

        if typ == 'ItemList':
            for x in entity['itemListElement']:
                c = self.add_entity(x['item'])
                conforms = conforms and c
        elif typ == 'DataFeed':
            for x in entity['dataFeedElement']:
                c = self.add_entity(x)
                conforms = conforms and c
        else:
            if typ not in self.reports:
                self.reports[typ] = list()

            if typ not in self._total:
                self._total[typ] = 0

            self._total[typ] += 1
            self._position = self._position + 1
            id = ''
            if '@id' in entity:
                id = 'Id: ' + entity['@id']
            else:
                id = 'Position: ' + str(self._position)

            entity = json.loads(json.dumps(entity))
            entity = self.__add_ids(entity)
            g = rdflib.Graph()
            entity['@context'] = {}
            entity['@context']['@vocab'] = 'http://schema.org/'
            gid = entity['@id']
            gid = rdflib.URIRef('file://' + gid)

            g.parse(data=json.dumps(entity), format='json-ld')

            g.serialize('test.nt', format='nt')

            _, results_graph, _ = validate(
                g, shacl_graph=self._constraints_file, advanced=True)
            results_graph.serialize('./test.ttl', format='turtle')
            start_nodes = list()

            for r, _, _ in results_graph.triples(
                    (None, constants.result_constants['Type'], constants.result_constants['ValidationResult'])):

                if (r,
                        constants.result_constants['FocusNode'], gid) in results_graph:
                    start_nodes.append(r)

            for r in start_nodes:
                c = self.__add_report(results_graph, r, typ, '', id)
                conforms = conforms and c

        return conforms

    def __add_report(self,
                     graph: rdflib.Graph,
                     result_id: str,
                     typ: str,
                     path: str,
                     src_identifier: str) -> bool:
        """Perform a DFS over the results. Identify the root cause of the
        validation error. Add the cause to reports.

        Args:
            graph (rdflib.Graph): The result graph representing the validation
                                  errors.
            result_id (str): The id of result that is being inspected.
            typ (str): The @type of the main entity that is being validated.
            path (str): The path from the main entity to the cause of error.
            src_identifier (str): The @id of the main entity that is being
                                     validated.

        Returns:
            bool: The conformance of entity that is validated by the result
                  which is identified by result_id.
        """

        attr = graph.value(
            result_id, constants.result_constants['ResultPath'], None)
        attr = utils.strip_url(attr)

        value = graph.value(
            result_id, constants.result_constants['Value'], None)
        severity = graph.value(
            result_id, constants.result_constants['ResultSeverity'], None)
        severity = utils.strip_shacl_prefix(severity)
        conforms = True

        if not isinstance(value, rdflib.URIRef):
            message = '-'

            if value is None:
                value = '-'

            msg = graph.value(
                result_id, constants.result_constants['Message'], None)

            if msg:
                message = str(msg)

            result = utils.ResultRow(
                src_identifier, message, path + '.' + attr, str(value), severity)
            self.reports[typ].append(result)

            if severity == 'Violation':
                return False

        else:
            next_ids = list()
            for r, _, _ in graph.triples(
                    (None, constants.result_constants['Type'], constants.result_constants['ValidationResult'])):

                if (r,
                        constants.result_constants['FocusNode'], value) in graph:
                    next_ids.append(r)

            for r in next_ids:
                conforms = (conforms and self.__add_report(
                    graph, r, typ, path + '.' + attr, src_identifier))

        return conforms

    def __get_aggregates(self) -> dict:
        """Computes the aggregates and returns it.

        Returns:
            dict: Dictionary containing computed aggregates for every entity.
        """

        aggregates = {}

        for x in self.reports.keys():
            aggregates[x] = {}
            aggregates[x]['Info'] = {}
            aggregates[x]['Warning'] = {}
            aggregates[x]['Violation'] = {}
            aggregates[x]['Info']['entity'] = set()
            aggregates[x]['Warning']['entity'] = set()
            aggregates[x]['Violation']['entity'] = set()
            aggregates[x]['Info']['count'] = 0
            aggregates[x]['Warning']['count'] = 0
            aggregates[x]['Violation']['count'] = 0

            for r in self.reports[x]:
                aggregates[x][r.severity]['count'] += 1
                aggregates[x][r.severity]['entity'].add(r.id)

            aggregates[x]['Info']['entity'] = len(
                aggregates[x]['Info']['entity'])
            aggregates[x]['Warning']['entity'] = len(
                aggregates[x]['Warning']['entity'])
            aggregates[x]['Violation']['entity'] = len(
                aggregates[x]['Violation']['entity'])

        return aggregates

    def close(self):
        """Generate a report, write it to file and close the validator."""

        assert self._is_closed == False, 'Validator has already been closed.'

        this_folder = os.path.dirname(os.path.abspath(__file__))
        templates_folder = os.path.join(this_folder, 'templates')
        file_loader = FileSystemLoader(templates_folder)

        env = Environment(loader=file_loader,
                          trim_blocks=True, lstrip_blocks=True)
        env.globals['enumerate'] = enumerate

        aggregates = self.__get_aggregates()
        items_list = ', '.join(sorted(self.reports.keys()))
        out_html = env.get_template('report.html').render(
            results=self.reports, aggregates=aggregates, items=items_list, total=self._total)

        f = open(self._report_file, 'w')
        f.write(out_html)
        f.close()
