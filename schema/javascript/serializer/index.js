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

/**
 * JSONLDSerializer is used to serialize schema proto object to JSONLD feed.
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
            return outObj
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
            let dt = new Date(obj.array[0], obj.array[1], obj.array[2]);
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
            // TODO: Timezone
            let dt = new Date(2000, 1, 1, obj.array[0], obj.array[1], obj.array[2]);
            return dt.toISOString().substring(11, 19);
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
            // TODO: Timezone
            let dt = new Date(obj.array[0][0],obj.array[0][1],obj.array[0][2]
                                ,obj.array[1][0],obj.array[1][1],obj.array[1][2]);

            return dt.toISOString().substr(0, 19);
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
        else if(messageType=="DatatypeQuantitaive"){
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

class JSONLDItemListSerializer extends JSONLDSerializer {

    constructor(outFile){
        super();
        this.outFile = fs.openSync(outFile, 'w');
        this.count = 0;
        this.isClosed = false;

        fs.writeSync(this.outFile, "{\n");
        fs.writeSync(this.outFile, "\t\"@context\":\"https://schema.org\",\n");
        fs.writeSync(this.outFile, "\t\"@type\":\"ItemList\",\n");
        fs.writeSync(this.outFile, "\t\"itemListElement\":[");

    }

    addItem(listItem, schema, schemaDescriptor) {

        assert(this.isClosed == false, "The serializer has already been closed.");

        if(this.count){
            fs.writeSync(this.outFile, ",");
        }

        let listItemSerialized = super.protoToDict(listItem, "ListItem", schemaDescriptor);
        listItemSerialized = JSON.stringify(listItemSerialized, null, 4);
        listItemSerialized = "\n" + listItemSerialized
        listItemSerialized = listItemSerialized.split("\n").join("\n\t\t");

        fs.writeSync(this.outFile, listItemSerialized);
        this.count = this.count + 1;
        
    }

    close() {

        assert(this.isClosed == false, "The serializer has already been closed.");

        fs.writeSync(this.outFile, "\n\t]\n");
        fs.writeSync(this.outFile, "}\n");
        fs.closeSync(this.outFile);
        this.isClosed = true;
    }
    
}

module.exports.JSONLDSerializer = JSONLDSerializer;
module.exports.JSONLDItemListSerializer = JSONLDItemListSerializer;


// // Test code will be removed later
// let j = new JSONLDItemListSerializer("./out.json");

// const schema = require("./schema_pb.js");
// const schemaDescriptor = require("./schema_descriptor.json");
// for(let i=0; i<4; i++){
//     let listItem = new schema.ListItem();
//     let item = new schema.ItemProperty();
//     let position = new schema.PositionProperty();
//     position.setInteger(i+1);
//     listItem.addPosition(position);

//     let movie = new schema.Movie();
//     let name = new schema.NameProperty();
//     name.setText("movie name" + String(i+1));
//     movie.addName(name);

//     let actor = new schema.ActorProperty();
//     let person = new schema.Person();
//     name = new schema.NameProperty();
//     name.setText("actor name" + String(i+1) +"-1");
//     person.addName(name);
//     actor.setPerson(person);
//     movie.addActor(actor);

//     actor = new schema.ActorProperty();
//     person = new schema.Person();
//     name = new schema.NameProperty();
//     name.setText("actor name" + String(i+1) +"-2");
//     person.addName(name);
//     actor.setPerson(person);
//     movie.addActor(actor);

//     actor = new schema.ActorProperty();
//     person = new schema.Person();
//     name = new schema.NameProperty();
//     name.setText("actor name" + String(i+1) +"-3");
//     person.addName(name);
//     actor.setPerson(person);
//     movie.addActor(actor);

//     item.setMovie(movie);
//     listItem.addItem(item);

//     j.addItem(listItem, schema, schemaDescriptor);

// }

// j.close();

