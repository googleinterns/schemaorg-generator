import schemaorgutils.serializer as serializer
import schema_pb2 as schema
import os
import json


def test_item_list():
    """Test serialization of ItemList using feed serializer.
    Procedure:
        - Create a new feed serializer.
        - Create multiple entities of any type.
        - Call serializer.add_item along with schema and the entity for each
          entity.
        - Close the serializer.

    Verification:
        - Check if all the entities are enclosed inside ListItem.
        - Check if all the ListItem has position fields set in order.
        - Check if all the ListItems are enclosed inside an ItemList.
        - Check if '@type' field is set properly for ListItem and ItemList.
    """

    jis = serializer.JSONLDFeedSerializer(
        './tests/files/test_jsonld_item_list_out.json',
        feed_type='ItemList')

    for i in range(5):
        mv = schema.Movie()
        mv.name.add().text = 'Movie ' + str(i + 1)
        mv.id = 'Id of Movie ' + str(i + 1)
        for j in range(3):
            actor = mv.actor.add().person
            actor.name.add().text = 'Actor ' + str(j + 1)
        jis.add_item(mv, schema)

    jis.close()

    with open('./tests/files/test_jsonld_item_list_out.json') as f:
        output = json.load(f)

    with open('./tests/files/test_jsonld_item_list.json') as f:
        expected = json.load(f)

    os.remove('./tests/files/test_jsonld_item_list_out.json')

    assert output == expected, 'Error in Serialization of ItemList.'


def test_data_feed():
    """Test serialization of DataFeed using feed serializer.
    Procedure:
        - Create a new feed serializer.
        - Create multiple entities of any type.
        - Call serializer.add_item along with schema and the entity for each
          entity.
        - Close the serializer.

    Verification:
        - Check if all the entities are enclosed inside DataFeedItem.
        - Check if all the DataFeedItem are enclosed inside an DataFeed.
        - Check if '@type' field is set properly for DataFeed and DataFeedItem.
    """

    jis = serializer.JSONLDFeedSerializer(
        './tests/files/test_jsonld_data_feed_out.json',
        feed_type='DataFeed')

    for i in range(5):
        mv = schema.Movie()
        mv.name.add().text = 'Movie ' + str(i + 1)
        mv.id = 'Id of Movie ' + str(i + 1)
        for j in range(3):
            actor = mv.actor.add().person
            actor.name.add().text = 'Actor ' + str(j + 1)
        jis.add_item(mv, schema)

    jis.close()

    with open('./tests/files/test_jsonld_data_feed_out.json') as f:
        output = json.load(f)

    with open('./tests/files/test_jsonld_data_feed.json') as f:
        expected = json.load(f)

    os.remove('./tests/files/test_jsonld_data_feed_out.json')

    assert output == expected, 'Error in Serialization of DataFeed.'
