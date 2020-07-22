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
const expect = require('chai').expect;
const SchemaValidator = require("../index").SchemaValidator;
const utils = require("../utils/utils");
const fs = require("fs");

// Test SchemaValidator.
//     Procedure:
//         - Create a new validator.
//         - Create shacl constraints with error of severity:
//             * Violation
//             * Warning
//             * Info
//         - Create an entity with error in a literal.
//         - Create an entity with nested error(inside a object).
//         - Create an entity that has errors in multiple objects that belong to same attribute.
//         - Make sure these errors are of varying severity.
//         - Validate all entities.
    
//     Verification:
//         - Check if all errors are detected.
//         - Check if the paths of nested errors are identfied properly.
//         - Check if multiple invalid objects within same attribute throw multiple errors. 
//         - Check if the conformance is false only if severity is Violation.
//         - Check if messages are identified properly.
describe("Test validator", () => {
    it("Testing validator.", async () => {
        let validator = new SchemaValidator("./test/files/validator_test_constraints.ttl", "./test/files/validator_test_report.html");
        await validator.loadShapes();
        const dump = require("./files/validator_test_data_feed.json");
        let expectedConformance = [false, true, true]
        let outConformance = []

        for(let x of dump["dataFeedElement"]){
            outConformance.push(await validator.addEntity(x));
        }
        
        expect(expectedConformance).to.eql(outConformance)

        let expected = []
        expected.push(
            new utils.ResultRow(
                "Id: movieid1",
                "Name of movie must be string.",
                ".name",
                "123",
                "Violation"
            ))
        
        expected.push(  
            new utils.ResultRow(
                "Id: id2",
                "Name of person must be string.",
                ".actor.name",
                "123",
                "Warning"
            ))
        
        expected.push(
            new utils.ResultRow(
            "Id: id3",
            "Name of person must be string.",
            ".creator.name",
            "123",
            "Warning"
            ))

        expected.push(
            new utils.ResultRow(
                "Id: id3",
                "Name of organization must be string.",
                ".creator.url",
                "345",
                "Info"
            ))

        validator.close();
        fs.unlinkSync("./test/files/validator_test_report.html");
        expect(expected).to.deep.include.members(validator.reports["Movie"]);
        
    });
});

// Test SchemaValidator with ItemList.
//     Procedure:
//         - Create a new validator.
//         - Create shacl constraints with error of severity:
//             * Violation
//             * Warning
//             * Info
//         - Create a itemlist.
//         - Add an entity with error in a literal.
//         - Add an entity with nested error(inside a object).
//         - Add an entity that has errors in multiple objects that belong to same attribute.
//         - Make sure these errors are of varying severity.
//         - Validate itemlist.
    
//     Verification:
//         - Check if all errors within the nested items are detected.
//         - Check if the paths of nested errors are identfied properly.
//         - Check if multiple invalid objects within same attribute throw multiple errors. 
//         - Check if the conformance is false only if severity is Violation.
//         - Check if messages are identified properly.
describe("Test validator itemlist", () => {
    it("Testing validator when itemlist is used.", async () => {
        let validator = new SchemaValidator("./test/files/validator_test_constraints.ttl", "./test/files/validator_test_report.html");
        await validator.loadShapes();
        const dump = require("./files/validator_test_item_list.json");
        let expectedConformance = false;
        let outConformance = await validator.addEntity(dump);
        
        expect(expectedConformance).to.eql(outConformance);
        
        let expected = []
        expected.push(
            new utils.ResultRow(
                "Id: movieid1",
                "Name of movie must be string.",
                ".name",
                "123",
                "Violation"
            ))
        
        expected.push(  
            new utils.ResultRow(
                "Id: id2",
                "Name of person must be string.",
                ".actor.name",
                "123",
                "Warning"
            ))
        
        expected.push(
            new utils.ResultRow(
            "Id: id3",
            "Name of person must be string.",
            ".creator.name",
            "123",
            "Warning"
            ))

        expected.push(
            new utils.ResultRow(
                "Id: id3",
                "Name of organization must be string.",
                ".creator.url",
                "345",
                "Info"
            ))

        validator.close();
        fs.unlinkSync("./test/files/validator_test_report.html");
        expect(expected).to.deep.include.members(validator.reports["Movie"]);
        
    });
});

// Test SchemaValidator with DataFeed.
//     Procedure:
//         - Create a new validator.
//         - Create shacl constraints with error of severity:
//             * Violation
//             * Warning
//             * Info
//         - Create a datafeed.
//         - Add an entity with error in a literal.
//         - Add an entity with nested error(inside a object).
//         - Add an entity that has errors in multiple objects that belong to same attribute.
//         - Make sure these errors are of varying severity.
//         - Validate datafeed.
    
//     Verification:
//         - Check if all errors within the nested feeds are detected.
//         - Check if the paths of nested errors are identfied properly.
//         - Check if multiple invalid objects within same attribute throw multiple errors. 
//         - Check if the conformance is false only if severity is Violation.
//         - Check if messages are identified properly.
describe("Test validator dataFeed", () => {
    it("Testing validator when dataFeed is used.", async () => {
        let validator = new SchemaValidator("./test/files/validator_test_constraints.ttl", "./test/files/validator_test_report.html");
        await validator.loadShapes();
        const dump = require("./files/validator_test_data_feed.json");
        let expectedConformance = false;
        let outConformance = await validator.addEntity(dump);
        
        expect(expectedConformance).to.eql(outConformance);
        
        let expected = []
        expected.push(
            new utils.ResultRow(
                "Id: movieid1",
                "Name of movie must be string.",
                ".name",
                "123",
                "Violation"
            ))
        
        expected.push(  
            new utils.ResultRow(
                "Id: id2",
                "Name of person must be string.",
                ".actor.name",
                "123",
                "Warning"
            ))
        
        expected.push(
            new utils.ResultRow(
            "Id: id3",
            "Name of person must be string.",
            ".creator.name",
            "123",
            "Warning"
            ))

        expected.push(
            new utils.ResultRow(
                "Id: id3",
                "Name of organization must be string.",
                ".creator.url",
                "345",
                "Info"
            ))

        validator.close();
        fs.unlinkSync("./test/files/validator_test_report.html");
        expect(expected).to.deep.include.members(validator.reports["Movie"]);
        
    });
});
