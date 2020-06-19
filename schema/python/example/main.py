import seeder
import json
import mysql
import feed_generator
import schema_pb2
# import /path/to/serializer as serializer

def main():
    with open('./config.json') as f:
      config = json.load(f)

    with open('./dump.json') as f:
      dump = json.load(f)

    mydb = mysql.connector.connect(
      host=config["DBConfig"]["host"],
      user=config["DBConfig"]["user"],
      password=config["DBConfig"]["password"],
    )

    cursor = mydb.cursor()
    sdr = seeder.IMDBSeeder(cursor, config["DBConfig"]["dbname"])
    sdr.seed_db(cursor, dump["movies"], dump["tvseries"], dump["tvepisodes"])
    mydb.commit()

    i = feed_generator.IMDBExample()
    item_list = i.get_feed(cursor, schema_pb2)

    szr = serializer.JSONLDSerializer()
    szr.write(item_list, "./generated-feed.json", schema_pb2)


if __name__ == '__main__':
    """Seeds the DB with movie data and serializes it into JSON-LD feed."""
    main()


