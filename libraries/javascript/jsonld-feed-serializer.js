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
"use strict";
const fs = require('fs');
const assert = require('assert');
const deasync = require("deasync");
const JSONLDSerializer = require("./jsonld-serializer");

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
        
        if(this.validator){
            let conforms, done=false;
            this.validator.addEntity(entitySerialized).then(v => {
                conforms = v;
                done = true;
            });

            deasync.loopWhile(function(){return !done;});
            if(!conforms) return;
        }
        
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

module.exports = JSONLDFeedSerializer;
