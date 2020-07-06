// Copyright 2020 Google LLC

// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at

//     https://www.apache.org/licenses/LICENSE-2.0

// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.
const ParserN3 = require('@rdfjs/parser-n3');
const ParserJsonld = require('@rdfjs/parser-jsonld');
const Readable = require('stream').Readable;
const factory = require('rdf-ext');
const fs = require('fs');

/**
 * Parse JSONLD and form a rdf graph.
 * @param  {Object} jsonObj The JSONLD entity to be loaded.
 * @return {factory.dataset}      RDF graph generated from given jsonld.
 */
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

/**
 * Load the tutle file and form a rdf graph.
 * @param  {String} filePath The path to turtle file to be loaded.
 * @return {factory.dataset}      RDF graph generated from the file.
 */
async function loadTurtleFile(filePath){
    const stream = fs.createReadStream(filePath)
    const parser = new ParserN3({ factory })
    return factory.dataset().import(parser.import(stream))
};

/**
 * Strip URL from the string.
 * @param  {String} x String to strip url from.
 * @return {String}      The value of url.
 */
function stripUrl(x){
    let spt = x.split("/");
    return spt[spt.length - 1];
};

/**
 * Strip SHACL prefix from the string.
 * @param  {String} x String to strip url from.
 * @return {String}      The value of string after stripping prefix.
 */
function stripShaclPrefix(x){
    return x.substring(27);
};

/**
 * ResultRow indicates a row in the validation report.
 * @class
 */
class ResultRow{
    /**
     * Constructor for ResultRow.
     * @constructor
     * @param  {String} id Identfier of the outermost entity that caused the validation error.
     * @param  {String} message The message indicating the cause of error.
     * @param  {String} propertyPath The path to the source of error.
     * @param  {String} value The value of attribute that caused error.
     * @param  {String} severity The severity of error.
     */
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
