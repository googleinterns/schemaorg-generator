import json
import rdflib
import uuid
import utils.constants as constants
import utils.utils as utils
from pyshacl import validate
from jinja2 import Environment, FileSystemLoader

class SchemaValidator():
    def __init__(self, constraints_file):
        
        self.constraints_file = constraints_file
        self.reports = dict()
        self.position = 0
        self.is_closed = False

    def add_ids(self, entity):

        if not isinstance(entity, dict):
            return entity
        else:
            entity["@id"] = "/schemavalidator/" + str(uuid.uuid4())
            
            for key in sorted(entity.keys()):
                entity[key] = self.add_ids(entity[key])
            
            return entity

    def add_entity(self, entity):

        assert self.is_closed == False, "Validator has already been closed."

        self.position = self.position + 1
        
        id = ""
        
        if "@id" in entity:
            id = "Id: " + entity["@id"]
        else:
            id = "Position: " + str(self.position)
        

        typ = entity["@type"]
        entity = self.add_ids(entity)
        g = rdflib.Graph()
        entity["@context"] = {}
        entity["@context"]["@vocab"] = "http://schema.org/"
        gid = entity["@id"]
        gid = rdflib.URIRef("file://" + gid)

        g.parse(data=json.dumps(entity), format="json-ld")

        g.serialize("test.nt", format = "nt")

        _, results_graph, _ = validate(g, shacl_graph=self.constraints_file)

        start_nodes = list()
        conforms = True

        for r, _, _ in results_graph.triples((None, constants.result_constants["Type"], constants.result_constants["ValidationResult"])):
            if (r, constants.result_constants["FocusNode"], gid) in results_graph:
                start_nodes.append(r)

        for r in start_nodes:
            conforms = (conforms and self.add_report(results_graph, r, typ, "", id))

        return conforms


    def add_report(self, graph, result_id, typ, path, src_identifier):

        attr = graph.value(result_id, constants.result_constants["ResultPath"], None)
        attr = utils.strip_url(attr)

        value = graph.value(result_id, constants.result_constants["Value"], None)
        severity = graph.value(result_id, constants.result_constants["ResultSeverity"], None)
        severity = utils.strip_shacl_prefix(severity)
        conforms = True

        if not isinstance(value, rdflib.URIRef):
            message = ""

            if typ not in self.reports:
                self.reports[typ] = list()
            
            msg = graph.value(result_id, constants.result_constants["Message"], None)

            if msg:
                message = str(msg)

            result = utils.ResultRow(src_identifier, message, path + "." + attr, value, severity)
            self.reports[typ].append(result)

            if severity == "Violation":
                return False

        else:
            next_ids = list()
            for r, _, _ in graph.triples((None, constants.result_constants["Type"], constants.result_constants["ValidationResult"])):
                if (r, constants.result_constants["FocusNode"], value) in graph:
                    next_ids.append(r)
                
            for r in next_ids:
                conforms = (conforms and self.add_report(graph, r, typ, path + "." + attr, src_identifier))
            
        
        return conforms


    def get_report_and_close(self, report_path):
        assert self.is_closed == False, "Validator has already been closed."
        
        file_loader = FileSystemLoader('./templates')
        env = Environment(loader=file_loader, trim_blocks=True, lstrip_blocks=True)
        env.globals["enumerate"] = enumerate

        out_html = env.get_template('report.html').render(results = self.reports)

        f = open(report_path, "w")
        f.write(out_html)
        f.close()
        

    
# s = SchemaValidator("./movie_constraints.ttl")
# with open('./movie_single.json') as f:
#     data = json.load(f)

# print(s.add_entity(data))
# s.get_report_and_close("./report.html")
