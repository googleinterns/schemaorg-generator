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
const mysql = require('mysql');
const util = require('util');
const dump = require("./dump.json");
const config = require("./config.json");
const schema = require('./schema_pb');
const schemaDescriptor = require('./schema_descriptor.json');
const JSONLDSerializer = require('../serializer').JSONLDSerializer;
const IMDBExample = require('./feed_generator').IMDBExample;
const IMDBSeeder = require('./seeder').IMDBSeeder;

/**
 * Creates new IMDBSeeder and seeds db and creates new IMDBExample and generates feed.
 * @return {Promise}      Promise that indicates complete execution of function.
 */
async function main () {
    let seeder = new IMDBSeeder();
    await seeder.init(config.DBConfig);
    
    let con = mysql.createConnection({
        host: config.DBConfig.host,
        user: config.DBConfig.user,
        password: config.DBConfig.password,
        database: config.DBConfig.dbname
    });
    let query = util.promisify(con.query).bind(con);

    console.log("Started seeding database.");
    await seeder.createTables(query);
    console.log("Tables created successfully.");
    await seeder.seedDB(query, dump["movies"], dump["tvseries"], dump["tvepisodes"]);
    console.log("Database seeding completed.");

    let example = new IMDBExample();
    console.log("Feed generation started.");
    let itemList = await example.generateFeed(query, schema);
    console.log("Feed generation completed.");

    let serializer = new JSONLDSerializer();
    console.log("Serializing feed.");
    await serializer.writeToFile(itemList, "ItemList", schemaDescriptor, "./generated-feed.json");
    console.log("Serialization completed.");

}

main().then(function(){
    console.log("Successfully ran example.");
    process.exit(0);
})