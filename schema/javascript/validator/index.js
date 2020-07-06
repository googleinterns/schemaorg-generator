const factory = require('rdf-ext')
const SHACLValidator = require('rdf-validate-shacl')
const fs = require('fs')
const assert = require('assert');
const dataTypes = require("./utils/constants").dataTypes;
const resultConstants = require("./utils/constants").resultConstants;
const utils = require("./utils/utils");

class SchemaValidator{
    
    constructor(constraintsFile, reportFile){
        this.constraintsFile = constraintsFile;
        this.reportFile = reportFile;
        this.position = 0;
        this.isClosed = false;
        this.shapesLoaded = false;
        this.reports = {};
    }

    async loadShapes(){

        assert(this.shapesLoaded == false, "The shapes have already been loaded.");
        assert(this.isClosed == false, "The validator has already been closed.");
        this.shapes = await utils.loadTurtleFile(this.constraintsFile);
        this.shapesLoaded = true;
    }

    async addEntity(entity){

        assert(this.shapesLoaded == true, "Please load the shapes before adding entity.");
        assert(this.isClosed == false, "The validator has already been closed.");

        entity = JSON.parse(JSON.stringify(entity));

        entity["@context"] = {
            "@vocab": "http://schema.org/" 
        }

        this.position = this.position + 1;
        let id = "";

        if(entity["@id"]) id = "Id: " + entity["@id"];
        else id = "Position: " + this.position.toString()

        entity["@id"] = "Start Node Id";
        let gid = factory.namedNode("Start Node Id");
        let typ = entity["@type"];
        
        let data = await utils.loadJSONLd(entity);
        let validator = new SHACLValidator(this.shapes, { factory })
        let resultGraph = (await validator.validate(data)).dataset;
        let conforms = true;
        let startNodes = [];

        for(let q of resultGraph.match(null, resultConstants["Type"], resultConstants["ValidationResult"])){
            if(resultGraph.has(factory.quad(q["subject"], resultConstants["FocusNode"], gid))){
                startNodes.push(q["subject"]);
            }
        }

        for( let s of startNodes){
            conforms = conforms && this.addReport(resultGraph, s, typ, "", id);
        }

        return conforms;

    }

    addReport(graph, resultNode, typ, path, srcIdentifier){

        let attr = ""
        for(let q of graph.match(resultNode, resultConstants["ResultPath"])){
            attr = utils.stripUrl(q["object"].toString());
        }

        let value = ""
        for(let q of graph.match(resultNode, resultConstants["Value"])){
            value = q["object"];
        }

        let severity = ""
        for(let q of graph.match(resultNode, resultConstants["ResultSeverity"])){
            severity = utils.stripShaclPrefix(q["object"].toString());
        }

        let conforms = true;

        let nextNodes = [];

        for(let q of graph.match(null, resultConstants["Type"], resultConstants["ValidationResult"])){
            if(graph.has(factory.quad(q["subject"], resultConstants["FocusNode"], value))){
                nextNodes.push(q["subject"]);
            }
        }

        if(nextNodes.length){
            for(let n of nextNodes){
                conforms = conforms && this.addReport(graph, n , typ, path + "." + attr, srcIdentifier);
            }
            
            return conforms;
        }
        else{
            if(!this.reports[typ]){
                this.reports[typ] = [];
            }

            let message = ""
            for(let q of graph.match(resultNode, resultConstants["Message"])){
                message = utils.stripUrl(q["object"].toString());
            }
            let result = new utils.ResultRow(srcIdentifier,message, path + "." + attr, this.literalToValue(value), severity);
            this.reports[typ].push(result);

            return severity == "Violation" ?false:true;
        }
    }

    literalToValue(node){
        let typ = dataTypes[node.datatype.value];

        if(typ == "integer"){
            return parseInt(node.value);
        }
        else if(typ == "double"){
            return parseFloat(node.value);
        }
        else if(typ == "boolean"){
            return node.value == "true" ? true:false;
        }
        else if(typ == "string"){
            return node.value;
        }
        else{
            return "";
        }
    }

    close(){
        assert(this.isClosed == false, "The validator has already been closed.");
        
        this.isClosed = true;
        console.log(JSON.stringify(this.reports, null , 4));
    }
}


// async function main() {
//     let v = new SchemaValidator("./movie_constraints.ttl", "./reportjs.html");
//     await v.loadShapes();
//     console.log(await v.addEntity(feed));
//     v.close();
// }

// async function main2() {
//     const schema = require("../serializer/schema_pb");
//     const schemaDescriptor = require("../serializer/schema_descriptor.json");
//     const JSONSerializer = require("../serializer/index").JSONLDFeedSerializer;

//     let val = new SchemaValidator("./movie_constraints.ttl", "./report.html");
//     await val.loadShapes();

//     let ser = new JSONSerializer("./test.json", "ItemList", validator = val);
//     let mv = new schema.Movie();
//     mv.setId("myid123");
//     let nm = new schema.NameProperty();
//     nm.setText("abcd name");
//     mv.addName(nm);

//     await ser.addItem(mv, "Movie", schemaDescriptor);
//     ser.close();
// }

// main2();


module.exports.SchemaValidator = SchemaValidator;
