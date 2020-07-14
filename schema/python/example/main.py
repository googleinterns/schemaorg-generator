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
import MySQLdb
import MySQLdb.cursors
import feed_generator
import schema_pb2
import schemaorgutils.serializer as serializer
import schemaorgutils.validator as validator


def main():
    with open('./config.json') as f:
        config = json.load(f)

    with open('./dump.json') as f:
        dump = json.load(f)

    mydb = MySQLdb.connect(
        host=config['DBConfig']['host'],
        user=config['DBConfig']['user'],
        password=config['DBConfig']['password'],
        cursorclass=MySQLdb.cursors.SSDictCursor
    )

    cursor = mydb.cursor()
    new_seeder = seeder.IMDBSeeder(cursor, config['DBConfig']['dbname'])
    new_seeder.seed_db(cursor, dump['movies'], dump['tvseries'], dump['tvepisodes'])
    mydb.commit()

    cursor.execute('use {};'.format(config['DBConfig']['dbname']))
    new_validator = validator.SchemaValidator('./constraints.ttl', './report.html')
    new_serializer = serializer.JSONLDFeedSerializer(
        './generated-feed.json',
        feed_type='ItemList',
        validator=new_validator)
    example = feed_generator.IMDBExample()

    for x in example.get_feed(cursor, schema_pb2):
        new_serializer.add_item(x, schema_pb2)

    new_serializer.close()


if __name__ == '__main__':
    """Seeds the DB with movie data and serializes it into JSON-LD feed."""
    main()
