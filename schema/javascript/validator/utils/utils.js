const ParserN3 = require('@rdfjs/parser-n3');
const ParserJsonld = require('@rdfjs/parser-jsonld');
const Readable = require('stream').Readable;
const factory = require('rdf-ext');
const fs = require('fs');

async function loadJSONLd(jsonObj){
    const parserJsonld = new ParserJsonld();
    const input = new Readable({
        read: () => {
            input.push(JSON.stringify(jsonObj));
            input.push(null);
        }
    });
    return factory.dataset().import(parserJsonld.import(input));
};

async function loadTurtleFile(filePath){
    const stream = fs.createReadStream(filePath)
    const parser = new ParserN3({ factory })
    return factory.dataset().import(parser.import(stream))
};

function stripUrl(x){
    let spt = x.split("/");
    return spt[spt.length - 1];
};

function stripShaclPrefix(x){
    return x.substring(27);
};

class ResultRow{
    constructor(id, message, propertyPath, value, severity){
        this.id = id;
        this.message = message;
        this.propertyPath = propertyPath;
        this.value = value;
        this.severity = severity;
    }
};

module.exports.loadJSONLd = loadJSONLd;
module.exports.loadTurtleFile = loadTurtleFile;
module.exports.stripUrl = stripUrl;
module.exports.stripShaclPrefix = stripShaclPrefix;
module.exports.ResultRow = ResultRow;
