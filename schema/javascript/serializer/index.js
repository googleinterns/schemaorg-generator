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
const fs = require('fs');
const util = require('util');
const moment = require('moment');
const assert = require('assert');
const sortObject = require("sort-object-keys");

/**
 * JSONLDSerializer is used to serialize schema proto object to JSONLD.
 * @class
 */
class JSONLDSerializer {

    /**
     * Check if a given objectType is a primitive object.
     * @param  {String} objectType The schema object type.
     * @param  {Object} schemaDescriptor The JSON schemaDescriptor.
     * @return {Boolean}      If or not the object is primitive.
     */
    checkPrimitive(objectType, schemaDescriptor) {
        return schemaDescriptor.primitives.includes(objectType);
    }

    /**
     * Convert schema class to dictionary object.
     * @param  {Object} obj The schema class object.
     * @param  {String} objectType The schema object type.
     * @param  {Object} schemaDescriptor The JSON schemaDescriptor.
     * @return {Object}      The schema class as dictionary object.
     */
    classToDict(obj, objectType, schemaDescriptor) {

        if(obj.wrappers_==null){
            return null;
        }
        else{
            let outObj = {};
            outObj["@type"] = schemaDescriptor.messages[objectType]["@type"];

            for(let i=0; i<schemaDescriptor.messages[objectType].fields.length; i++){
                let key = (i + 1).toString();

                if(obj.wrappers_[key]!=null ){
                    outObj[schemaDescriptor.messages[objectType].fields[i]] = [];

                    for(let j=0; j<obj.wrappers_[key].length; j++){
                        outObj[schemaDescriptor.messages[objectType].fields[i]].push(this.protoToDict(obj.wrappers_[key][j], schemaDescriptor.messages[objectType].fields[i], schemaDescriptor));
                    }

                    if(outObj[schemaDescriptor.messages[objectType].fields[i]].length==1){
                        outObj[schemaDescriptor.messages[objectType].fields[i]]=outObj[schemaDescriptor.messages[objectType].fields[i]][0];
                    }
                }
                else if(schemaDescriptor.messages[objectType].fields[i] == "@id"){
                    if(obj.array[0]){
                        outObj["@id"] = obj.array[0];
                    }
                }
            }
            return sortObject(outObj);
        }

    }

    /**
     * Convert schema property to the value assigned to it.
     * @param  {Object} obj The schema property object.
     * @param  {String} objectType The schema property type.
     * @param  {Object} schemaDescriptor The JSON schemaDescriptor.
     * @return {Object}      The value of schema property.
     */
    getPropertyValue(obj, objectType, schemaDescriptor){
        if(obj.wrappers_){
            for(let i=0; i<schemaDescriptor.messages[objectType].fields.length; i++){
                let key = (i + 1).toString();

                if(obj.wrappers_[key]!=null && obj.wrappers_[key]!=undefined){
                        return this.protoToDict(obj.wrappers_[key], schemaDescriptor.messages[objectType].fields[i], schemaDescriptor);
                }
            }
        }
        else{
            for(let i=0; i<obj.array.length; i++){
                if(obj.array[i]) return obj.array[i];
            }
        }
    }

    /**
     * Convert schema class to dictionary object.
     * @param  {Object} obj The schema enumeration object.
     * @param  {String} objectType The schema object type.
     * @param  {Object} schemaDescriptor The JSON schemaDescriptor.
     * @return {Object}      The schema enumeration as dictionary object or its value string.
     */
    enumToDict(obj, objectType, schemaDescriptor){
        if(obj.wrappers_){
            return this.protoToDict(obj.wrappers_['2'], schemaDescriptor.messages[objectType].fields[1], schemaDescriptor); 
        }
        else {
            return schemaDescriptor.messages[objectType].values[obj.array[0]];
        }
    }

    /**
     * Convert schema class to string.
     * @param  {Object} obj The schema date object.
     * @return {String}      The schema date as a string.
     */
    dateToString(obj) {
        if(!(obj.array[0]&&obj.array[1]&&obj.array[2])){
            throw("Date with empty fields found.");
        }
        else{
            let dt = moment.utc([obj.array[0],obj.array[1]-1, obj.array[2] ]);
            if(!dt.isValid()) throw("Invalid Date Found.");
            
            return dt.toISOString().substring(0, 10);
        }
    }

    /**
     * Convert schema time to string.
     * @param  {Object} obj The schema time object.
     * @return {String}      The schema time as a string.
     */
    timeToString(obj) {
        if(!(obj.array[0]&&obj.array[1]&&obj.array[2])){
            throw("Time with empty fields found.");
        }
        else{
            let dt = moment.utc({ hour:obj.array[0], minute:obj.array[1], second: obj.array[2] });
            if(!dt.isValid()) throw("Invalid Time Found.");
            
            let dtString = dt.toISOString();
            
            if(obj.array[3]){
                dtString = dtString.substr(0, 19);
                dtString = dtString + obj.array[3];
                dt = moment(dtString, moment.ISO_8601);
                
                if(dt.isValid()){
                    return dtString.substr(11);
                }
                else{
                    throw("Invalid Timezone.");
                }
            }
            else{
                return dtString.substr(11, 8);
            }
        }
    }

    /**
     * Convert schema datetime to string.
     * @param  {Object} obj The schema datetime object.
     * @return {String}      The schema datetime as a string.
     */
    dateTimeToString(obj) {
        if(!((obj.array[0]&&obj.array[0][0]&&obj.array[0][1]&&obj.array[0][2])
            &&(obj.array[1]&&obj.array[1][0]&&obj.array[1][1]&&obj.array[1][2]))) {
                 
                throw("Datetime with empty fields found.");
        }
        else{

            let dt = moment.utc([ obj.array[0][0], obj.array[0][1]-1, obj.array[0][2],
                                obj.array[1][0], obj.array[1][1], obj.array[1][2]]);

            
            if(!dt.isValid()) throw("Invalid DateTime Found.");
            let dtString = dt.toISOString();
            
            if(obj.array[1][3]){
                dtString = dtString.substr(0, 19);
                dtString = dtString + obj.array[1][3];
                dt = moment(dtString, moment.ISO_8601);
                
                if(dt.isValid()){
                    return dtString;
                }
                else{
                    throw("Invalid Timezone.");
                }
            }
            else{
                return dtString.substr(0, 19);
            }
        }
    }

    /**
     * Convert schema quantitative object to string.
     * @param  {Object} obj The schema quantitative object.
     * @return {String}      The schema quantitative object as a string.
     */
    quantitativeToString(obj) {
        if(!obj.array[0]) throw("Value not set in quantitative value.");
        if(!obj.array[1]) throw("Units not set in quantitative value.");

        return (obj.array[0].toString() + " " + obj.array[1]);
    }

    /**
     * Convert schema duration object to string.
     * @param  {Object} obj The schema duration object.
     * @return {String}      The schema duration as a string.
     */
    durationToString(obj) {
        if(!obj.array[0]) throw("Invalid duration object.");

        let dr = moment.duration(obj.array[0], 'seconds');
        return dr.toISOString()
    }

    /**
     * Convert schema object to dictionary object.
     * @param  {Object} obj The schema object.
     * @param  {String} objectType The schema object type.
     * @param  {Object} schemaDescriptor The JSON schemaDescriptor.
     * @return {Object}      The schema object as dictionary object.
     */
    protoToDict(obj, objectType, schemaDescriptor) {

        if(this.checkPrimitive(objectType, schemaDescriptor)){
            return obj;
        }
        
        let messageType = schemaDescriptor.messages[objectType]['@type'];

        if(messageType=="Property"){
            return this.getPropertyValue(obj, objectType, schemaDescriptor);
        }
        else if(messageType=="EnumWrapper"){
            return this.enumToDict(obj, objectType, schemaDescriptor);
        }
        else if(messageType=="DatatypeDate"){
            return this.dateToString(obj);
        }
        else if(messageType=="DatatypeDateTime"){
            return this.dateTimeToString(obj);
        }
        else if(messageType=="DatatypeTime"){
            return this.timeToString(obj);
        }
        else if(messageType=="DatatypeQuantitative"){
            return this.quantitativeToString(obj);
        }
        else if(messageType=="DatatypeDuration"){
            return this.durationToString(obj);
        }
        else {
            return this.classToDict(obj, objectType, schemaDescriptor);
        }
    }

    /**
     * Serialize to JSON-LD and write schema object to file.
     * @param  {Object} obj The schema object.
     * @param  {String} objectType The schema object type.
     * @param  {Object} schemaDescriptor The JSON schemaDescriptor.
     * @param  {String} outFile The path to output file.
     */
    async writeToFile(obj, objectType, schemaDescriptor, outFile){
        let outObj = this.protoToDict(obj, objectType, schemaDescriptor);
        outObj["@context"] = "http://schema.org";
        let jsonContent = JSON.stringify(outObj,null, 4);
        let writeFile = util.promisify(fs.writeFile).bind(fs);
        await writeFile(outFile, jsonContent, 'utf8');
    }
    
}

/**
 * JSONLDFeedSerializer is used to serialize schema proto object to JSONLD item by item as ItemList or DataFeed.
 * @class
 */
class JSONLDFeedSerializer extends JSONLDSerializer {

    /**
     * Constructor for JSONLDFeedSerializer.
     * @constructor
     * @param  {String} outFile The outfile where the feed has to be written to.
     * @param  {String} feedType The type of feed ItemList/DataFeed.
     * @param  {SchemaValidator} [validator = null] Validator if feed has to be validated.
     */
    constructor(outFile, feedType = "ItemList", validator = null){
        assert(feedType == "ItemList" || feedType == "DataFeed", "feed_type must be 'ItemList' or 'DataFeed'.");
        super();
        this.outFile = fs.openSync(outFile, 'w');
        this.count = 0;
        this.isClosed = false;
        this.feedType = feedType;

        if(validator){
            this.validator = validator;
        }

        if(this.feedType == "ItemList"){
            fs.writeSync(this.outFile, "{\n");
            fs.writeSync(this.outFile, "\t\"@context\":\"https://schema.org\",\n");
            fs.writeSync(this.outFile, "\t\"@type\":\"ItemList\",\n");
            fs.writeSync(this.outFile, "\t\"itemListElement\":[");
        }
        else if(this.feedType == "DataFeed"){
            fs.writeSync(this.outFile, "{\n");
            fs.writeSync(this.outFile, "\t\"@context\":\"https://schema.org\",\n");
            fs.writeSync(this.outFile, "\t\"@type\":\"DataFeed\",\n");
            fs.writeSync(this.outFile, "\t\"dataFeedElement\":[");
        }


    }

    /**
     * Serialize an item and validate it if validator exists. Write the item to the file.
     * @param  {Object} obj The schema object.
     * @param  {String} objectType The schema object type.
     * @param  {Object} schemaDescriptor The JSON schemaDescriptor.
     */
    addItem(entity, entityType, schemaDescriptor) {

        assert(this.isClosed == false, "The serializer has already been closed.");

        let entitySerialized = super.protoToDict(entity, entityType, schemaDescriptor);
        
        // if(this.validator){
        //     let conforms = await this.validator.addEntity(entitySerialized);

        //     if(!conforms) return;
        // }
        
        if(this.count){
            fs.writeSync(this.outFile, ",");
        }

        let outObj;

        if(this.feedType == "ItemList"){
            outObj = {};
            outObj["@type"] = "ListItem";
            outObj["item"] = entitySerialized;
            outObj["position"] = this.count + 1;
        }
        else{
            outObj = entitySerialized
        }

        outObj = JSON.stringify(outObj, null, 4);
        outObj = "\n" + outObj
        outObj = outObj.split("\n").join("\n\t\t");

        fs.writeSync(this.outFile, outObj);
        this.count = this.count + 1;
        
    }

    /**
     *Close the serializer and validator (if exists).
     */
    close() {

        assert(this.isClosed == false, "The serializer has already been closed.");

        fs.writeSync(this.outFile, "\n\t]\n");
        fs.writeSync(this.outFile, "}\n");
        fs.closeSync(this.outFile);

        if(this.validator){
            this.validator.close();
        }
        this.isClosed = true;
    }
    
}

module.exports.JSONLDSerializer = JSONLDSerializer;
module.exports.JSONLDFeedSerializer = JSONLDFeedSerializer;
