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

module.exports.JSONLDSerializer = JSONLDSerializer;

// Test code will be removed later

// var movie = new schema.Movie();
// var actor1 = new schema.ActorProperty();
// var person1 = new schema.Person();
// var name1 = new schema.NameProperty();
// var actor2 = new schema.ActorProperty();
// var person2 = new schema.Person();
// var name2 = new schema.NameProperty();
// var actor3 = new schema.ActorProperty();
// var person3 = new schema.Person();
// var name3 = new schema.NameProperty();
// name1.setText("Johnny Depp");
// person1.addName(name1);
// actor1.setPerson(person1);
// name2.setText("Johnny Depp2");
// person2.addName(name2);
// actor2.setPerson(person2);
// name3.setText("Johnny Depp3");
// person3.addName(name3);
// actor3.setPerson(person3);
// movie.addActor(actor1);
// movie.addActor(actor2);
// movie.addActor(actor3);

// var schema = require('./schema_pb');
// var schemaDescriptor = require("./schema_descriptor.json")
// console.log(person1);
// console.log(schemaDescriptor.messages["Person"].fields[44]);

// dt = new schema.Time()
// dtt = new schema.DateTime()
// dt.setHours(10)
// dt.setMinutes(5)
// dt.setSeconds(2)

// d = new schema.Date()
// d.setYear(2000)
// d.setMonth(2)
// d.setDay(9)

// dtt.setTime(dt)
// dtt.setDate(d)

// console.log(dt)
// console.log(dtt)

// jss = new JSONLDSerializer()
// jss.writeToFile(movie, "Movie", schemaDescriptor, "./out.json");
// console.log(JSON.stringify(jss.protoToDict(dtt, "DateTime", schemaDescriptor)))

// var e1 = new schema.PaymentStatusType()
// var e2 = new schema.PaymentStatusType()

// var cs = new schema.PaymentStatusTypeClass()
// cs.addName(name1)


// e1.setId(schema.PaymentStatusTypeClass.Id["PAYMENT_COMPLETE"])
// e2.setPaymentStatusType(cs)

// console.log(e1)
// console.log(e2)
// console.log(JSON.stringify(jss.protoToDict(e1, "PaymentStatusType", schemaDescriptor)))
// console.log(JSON.stringify(jss.protoToDict(e2, "PaymentStatusType", schemaDescriptor)))

