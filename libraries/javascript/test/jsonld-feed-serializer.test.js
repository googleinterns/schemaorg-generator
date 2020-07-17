const expect = require('chai').expect;
const schema = require("./schema_pb");
const schemaDescriptor = require("./schema_descriptor.json");
const fs = require("fs");
const JSONLDFeedSerializer = require("../index").JSONLDFeedSerializer;

// Test serialization of ItemList using feed serializer.
//     Procedure:
//         - Create a new feed serializer.
//         - Create multiple entities of any type.
//         - Call serializer.add_item along with schema and the entity for each entity.
//         - Close the serializer.
    
//     Verification:
//         - Check if all the entities are enclosed inside ListItem.
//         - Check if all the ListItem has position fields set in order.
//         - Check if all the ListItems are enclosed inside an ItemList. 
//         - Check if '@type' field is set properly for ListItem and ItemList.
describe("Test Serialization of ItemList", () => {
    it("Testing serialization of ItemList.", () => {
        let serializer = new JSONLDFeedSerializer("./test/files/serializer_test_item_list_out.json", "ItemList");

        for(let i=0; i<5; i++){
            let mv = new schema.Movie();
            let name = new schema.NameProperty();
            name.setText("Movie " + (i+1).toString());
            mv.addName(name);
            mv.setId("Id of Movie " + (i+1).toString());

            for(let j=0; j<3; j++){
                let actor = new schema.ActorProperty();
                let person = new schema.Person();
                let nm = new schema.NameProperty();
                nm.setText("Actor " + (j+1).toString());
                person.addName(nm);
                actor.setPerson(person);
                mv.addActor(actor);
            }

            serializer.addItem(mv, "Movie", schemaDescriptor);
        }

        serializer.close();

        const output = require("./files/serializer_test_item_list_out.json");
        const expected = require("./files/serializer_test_item_list.json");
        fs.unlinkSync("./test/files/serializer_test_item_list_out.json");

        expect(output).to.eql(expected);
    });
});

// Test serialization of DataFeed using feed serializer.
//     Procedure:
//         - Create a new feed serializer.
//         - Create multiple entities of any type.
//         - Call serializer.add_item along with schema and the entity for each entity.
//         - Close the serializer.
    
//     Verification:
//         - Check if all the entities are enclosed inside DataFeedItem.
//         - Check if all the DataFeedItem are enclosed inside an DataFeed.
//         - Check if '@type' field is set properly for DataFeed and DataFeedItem.
describe("Test Serialization of DataFeed", () => {
    it("Testing serialization of DataFeed.", () => {
        let serializer = new JSONLDFeedSerializer("./test/files/serializer_test_data_feed_out.json", "DataFeed");

        for(let i=0; i<5; i++){
            let mv = new schema.Movie();
            let name = new schema.NameProperty();
            name.setText("Movie " + (i+1).toString());
            mv.addName(name);
            mv.setId("Id of Movie " + (i+1).toString());

            for(let j=0; j<3; j++){
                let actor = new schema.ActorProperty();
                let person = new schema.Person();
                let nm = new schema.NameProperty();
                nm.setText("Actor " + (j+1).toString());
                person.addName(nm);
                actor.setPerson(person);
                mv.addActor(actor);
            }

            serializer.addItem(mv, "Movie", schemaDescriptor);
        }

        serializer.close();

        const output = require("./files/serializer_test_data_feed_out.json");
        const expected = require("./files/serializer_test_data_feed.json");
        fs.unlinkSync("./test/files/serializer_test_data_feed_out.json");

        expect(output).to.eql(expected);
    });
});
