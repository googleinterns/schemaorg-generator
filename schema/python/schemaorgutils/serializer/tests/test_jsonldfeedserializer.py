import serializer.serializer as serializer
import serializer.schema_pb2 as schema
import os
import json

def test_item_list():
    jis = serializer.JSONLDFeedSerializer("./tests/expectedjson/test_jsonld_item_list_out.json", feed_type="ItemList")

    for i in range(5):
        mv = schema.Movie()
        mv.name.add().text = "Movie " + str(i+1)
        mv.id = "Id of Movie " + str(i+1)
        for j in range(3):
            actor = mv.actor.add().person
            actor.name.add().text = "Actor " + str(j+1)
        jis.add_item(mv, schema)
    
    jis.close()

    with open("./tests/expectedjson/test_jsonld_item_list_out.json") as f:
        output = json.load(f)
    
    with open("./tests/expectedjson/test_jsonld_item_list.json") as f:
        expected = json.load(f)

    os.remove("./tests/expectedjson/test_jsonld_item_list_out.json")

    assert output == expected, "Error in Serialization of ItemList."

def test_data_feed():
    jis = serializer.JSONLDFeedSerializer("./tests/expectedjson/test_jsonld_data_feed_out.json", feed_type="DataFeed")

    for i in range(5):
        mv = schema.Movie()
        mv.name.add().text = "Movie " + str(i+1)
        mv.id = "Id of Movie " + str(i+1)
        for j in range(3):
            actor = mv.actor.add().person
            actor.name.add().text = "Actor " + str(j+1)
        jis.add_item(mv, schema)
    
    jis.close()

    with open("./tests/expectedjson/test_jsonld_data_feed_out.json") as f:
        output = json.load(f)
    
    with open("./tests/expectedjson/test_jsonld_data_feed.json") as f:
        expected = json.load(f)

    os.remove("./tests/expectedjson/test_jsonld_data_feed_out.json")

    assert output == expected, "Error in Serialization of DataFeed."
