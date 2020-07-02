# Copyright 2020 Google LLC

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     https://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import seeder
import json
import mysql
import feed_generator
import schema_pb2
import schemaorgutils.serializer.serializer as serializer

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

    szr = serializer.JSONLDFeedSerializer("./generated-feed.json", feed_type="ItemList")
    i = feed_generator.IMDBExample()
    i.generate_feed(cursor, schema_pb2, szr)
    szr.close()



if __name__ == '__main__':
    """Seeds the DB with movie data and serializes it into JSON-LD feed."""
    main()


