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
import mysql.connector
import json
import re
import isodate
from dateutil import parser

class IMDBSeeder():
    """The IMDBSeeder populates the database with data that is required for running IMDBExample class.

    Args:
        cursor (mysql.cursor): Mysql cursor which is used to seed the database.
        db_name (str): The name of mysql database to be created.
    """

    def __init__(self, cursor, db_name):
        cursor.execute("DROP DATABASE IF EXISTS {};".format(db_name))
        cursor.execute("CREATE DATABASE {};".format(db_name))
        cursor.execute("USE {};".format(db_name))

        movie_table = "CREATE table movie (url varchar(200) primary key, name varchar(200), image varchar(200), content_rating varchar(10), description varchar(1000), date_published date, keywords varchar(200), duration_minutes int, rating_count int, rating float(4,2), best_rating float(4,2), worst_rating float(4,2));"
        series_table = "CREATE table series (url varchar(200) primary key, name varchar(200), image varchar(200), content_rating varchar(10), description varchar(1000), date_published date, keywords varchar(200), rating_count int, rating float(4,2), best_rating float(4,2), worst_rating float(4,2));"
        episode_table = "CREATE table episode (url varchar(200) primary key, name varchar(200), image varchar(200), content_rating varchar(10), description varchar(1000), date_published date, keywords varchar(200), duration_minutes int, rating_count int, rating float(4,2), best_rating float(4,2), worst_rating float(4,2));"
        genres_table = "CREATE table genre ( entity_url varchar(200),  name varchar(200) );"
        actor_table = "CREATE table actor ( entity_url varchar(200), url varchar(200), name varchar(200) );"
        director_table = "CREATE table director ( entity_url varchar(200), url varchar(200), name varchar(200) );"
        creator_table = "CREATE table creator ( entity_url varchar(200), url varchar(200), name varchar(200), type enum('PERSON', 'ORGANIZATION'));"
        review_table = "CREATE table review ( entity_url varchar(200), author varchar(200), date_created date, language varchar(20), name varchar(200), review_body varchar(20000), rating float(4,2), best_rating float(4,2), worst_rating float(4,2) );"
        trailer_table = "CREATE table trailer( name varchar(200), embed_url varchar(200), thumbnail_url varchar(200), description varchar(1000), upload_date datetime, entity_url varchar(200) );"

        cursor.execute(movie_table)
        cursor.execute(series_table)
        cursor.execute(episode_table)
        cursor.execute(genres_table)
        cursor.execute(actor_table)
        cursor.execute(director_table)
        cursor.execute(creator_table)
        cursor.execute(review_table)
        cursor.execute(trailer_table)
        

    def seed_db(self, cursor, movie_list, series_list, episode_list):
        """Call __seed_movies, __seed_series, __seed_episodes and seed the database .

        Args:
            cursor (mysql.cursor): Mysql cursor which is used to seed the database.
            db_name (str): The name of mysql database to be created.
            movie_list (list): The list of JSON-LD movie objects to seed.
            series_list (list): The list of JSON-LD series objects to seed.
            episode_list (list): The list of JSON-LD episode objects to seed.
        """

        self.__seed_movies(cursor, movie_list)
        self.__seed_series(cursor, series_list)
        self.__seed_episodes(cursor, episode_list)

    def __seed_movies(self, cursor, movie_list):
        """Seed movies into the database.

        Args:
            cursor (mysql.cursor): Mysql cursor which is used to seed the database.
            movie_list (list): The list of JSON-LD movie objects to seed.
        """
        
        for m in movie_list:
            query = "INSERT INTO movie values ({}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {});".format(
                        json.dumps(m.get("url", "")), 
                        json.dumps(m.get("name", "")), 
                        json.dumps(m.get("image", "")), 
                        json.dumps(m.get("contentRating", "")), 
                        json.dumps(m.get("description", "")), 
                        json.dumps(m.get("datePublished", "")), 
                        json.dumps(m.get("keywords", "")), 
                        self.__get_duration(m.get("duration", "")), 
                        m["aggregateRating"].get("ratingCount", ""), 
                        m["aggregateRating"].get("ratingValue", ""), 
                        m["aggregateRating"].get("bestRating", ""), 
                        m["aggregateRating"].get("worstRating", "")
                    )
            cursor.execute(query)
            
            if "actor" in m:
                if isinstance(m["actor"], list):
                    for a in m["actor"]:
                        self.__seed_actor(cursor, a, m.get("url", ""))
                else:
                    self.__seed_actor(cursor, m["actor"], m.get("url", ""))
            
            if "director" in m:
                if isinstance(m["director"], list):
                    for a in m["director"]:
                        self.__seed_director(cursor, a, m.get("url", ""))
                else:
                    self.__seed_director(cursor, m["director"], m.get("url", ""))
            
            if "creator" in m:
                if isinstance(m["creator"], list):
                    for a in m["creator"]:
                        self.__seed_creator(cursor, a, m.get("url", ""))
                else:
                    self.__seed_creator(cursor, m["creator"], m.get("url", ""))
            
            if "genre" in m:
                if isinstance(m["genre"], list):
                    for a in m["genre"]:
                        self.__seed_genre(cursor, a, m.get("url", ""))
                else:
                    self.__seed_genre(cursor, m["genre"], m.get("url", ""))

            if "review" in m:
                if isinstance(m["review"], list):
                    for a in m["review"]:
                        self.__seed_review(cursor, a, m.get("url", ""))
                else:
                    self.__seed_review(cursor, m["review"], m.get("url", ""))

            if "trailer" in m:
                if isinstance(m["trailer"], list):
                    for a in m["trailer"]:
                        self.__seed_trailer(cursor, a, m.get("url", ""))
                else:
                    self.__seed_trailer(cursor, m["trailer"], m.get("url", ""))

    def __seed_series(self, cursor, series_list):
        """Seed series into the database.

        Args:
            cursor (mysql.cursor): Mysql cursor which is used to seed the database.
            series_list (list): The list of JSON-LD series objects to seed.
        """
        
        for m in series_list:
            query = "INSERT INTO series values ({}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {});".format(
                        json.dumps(m.get("url", "")), 
                        json.dumps(m.get("name", "")), 
                        json.dumps(m.get("image", "")), 
                        json.dumps(m.get("contentRating", "")), 
                        json.dumps(m.get("description", "")), 
                        json.dumps(m.get("datePublished", "")), 
                        json.dumps(m.get("keywords", "")), 
                        m["aggregateRating"].get("ratingCount", ""), 
                        m["aggregateRating"].get("ratingValue", ""), 
                        m["aggregateRating"].get("bestRating", ""), 
                        m["aggregateRating"].get("worstRating", "")
                    )
            cursor.execute(query)
            
            if "actor" in m:
                if isinstance(m["actor"], list):
                    for a in m["actor"]:
                        self.__seed_actor(cursor, a, m.get("url", ""))
                else:
                    self.__seed_actor(cursor, m["actor"], m.get("url", ""))
            
            if "director" in m:
                if isinstance(m["director"], list):
                    for a in m["director"]:
                        self.__seed_director(cursor, a, m.get("url", ""))
                else:
                    self.__seed_director(cursor, m["director"], m.get("url", ""))
            
            if "creator" in m:
                if isinstance(m["creator"], list):
                    for a in m["creator"]:
                        self.__seed_creator(cursor, a, m.get("url", ""))
                else:
                    self.__seed_creator(cursor, m["creator"], m.get("url", ""))
            
            if "genre" in m:
                if isinstance(m["genre"], list):
                    for a in m["genre"]:
                        self.__seed_genre(cursor, a, m.get("url", ""))
                else:
                    self.__seed_genre(cursor, m["genre"], m.get("url", ""))

            if "review" in m:
                if isinstance(m["review"], list):
                    for a in m["review"]:
                        self.__seed_review(cursor, a, m.get("url", ""))
                else:
                    self.__seed_review(cursor, m["review"], m.get("url", ""))

            if "trailer" in m:
                if isinstance(m["trailer"], list):
                    for a in m["trailer"]:
                        self.__seed_trailer(cursor, a, m.get("url", ""))
                else:
                    self.__seed_trailer(cursor, m["trailer"], m.get("url", ""))

            
    def __seed_episodes(self, cursor, episode_list):
        """Seed episodes into the database.

        Args:
            cursor (mysql.cursor): Mysql cursor which is used to seed the database.
            episode_list (list): The list of JSON-LD episode objects to seed.
        """
        
        for m in episode_list:
            query = "INSERT INTO episode values ({}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {});".format(
                        json.dumps(m.get("url", "")), 
                        json.dumps(m.get("name", "")), 
                        json.dumps(m.get("image", "")), 
                        json.dumps(m.get("contentRating", "")), 
                        json.dumps(m.get("description", "")), 
                        json.dumps(m.get("datePublished", "")), 
                        json.dumps(m.get("keywords", "")), 
                        self.__get_duration(m.get("timeRequired", "")), 
                        m["aggregateRating"].get("ratingCount", ""), 
                        m["aggregateRating"].get("ratingValue", ""), 
                        m["aggregateRating"].get("bestRating", ""), 
                        m["aggregateRating"].get("worstRating", "")
                    )
            cursor.execute(query)
            
            if "actor" in m:
                if isinstance(m["actor"], list):
                    for a in m["actor"]:
                        self.__seed_actor(cursor, a, m.get("url", ""))
                else:
                    self.__seed_actor(cursor, m["actor"], m.get("url", ""))
            
            if "director" in m:
                if isinstance(m["director"], list):
                    for a in m["director"]:
                        self.__seed_director(cursor, a, m.get("url", ""))
                else:
                    self.__seed_director(cursor, m["director"], m.get("url", ""))
            
            if "creator" in m:
                if isinstance(m["creator"], list):
                    for a in m["creator"]:
                        self.__seed_creator(cursor, a, m.get("url", ""))
                else:
                    self.__seed_creator(cursor, m["creator"], m.get("url", ""))
            
            if "genre" in m:
                if isinstance(m["genre"], list):
                    for a in m["genre"]:
                        self.__seed_genre(cursor, a, m.get("url", ""))
                else:
                    self.__seed_genre(cursor, m["genre"], m.get("url", ""))

            if "review" in m:
                if isinstance(m["review"], list):
                    for a in m["review"]:
                        self.__seed_review(cursor, a, m.get("url", ""))
                else:
                    self.__seed_review(cursor, m["review"], m.get("url", ""))

            if "trailer" in m:
                if isinstance(m["trailer"], list):
                    for a in m["trailer"]:
                        self.__seed_trailer(cursor, a, m.get("url", ""))
                else:
                    self.__seed_trailer(cursor, m["trailer"], m.get("url", ""))
            

    def __seed_actor(self, cursor, actor, url):
        """Seed actor into the database.

        Args:
            cursor (mysql.cursor): Mysql cursor which is used to seed the database.
            actor (object): The JSON-LD actor object to insert.
            url (str): The URL of entity to which actor belongs to.
        """

        query = "INSERT INTO actor values ({}, {}, {})".format(
                    json.dumps(url), 
                    json.dumps(actor.get("url", "")), 
                    json.dumps(actor.get("name", ""))
                )
        cursor.execute(query)

    def __seed_director(self, cursor, director, url):
        """Seed director into the database.

        Args:
            cursor (mysql.cursor): Mysql cursor which is used to seed the database.
            director (object): The JSON-LD director object to insert.
            url (str): The URL of entity to which director belongs to.
        """

        query = "INSERT INTO director values ({}, {}, {})".format(
                    json.dumps(url), 
                    json.dumps(director.get("url", "")), 
                    json.dumps(director.get("name", ""))
                )
        cursor.execute(query)
    
    
    def __seed_creator(self, cursor, creator, url):
        """Seed creator into the database.

        Args:
            cursor (mysql.cursor): Mysql cursor which is used to seed the database.
            creator (object): The JSON-LD creator object to insert.
            url (str): The URL of entity to which creator belongs to.
        """

        query = "INSERT INTO creator values ({}, {}, {}, {})".format(
                    json.dumps(url), 
                    json.dumps(creator.get("url", "")), 
                    json.dumps(creator.get("name", "")), 
                    json.dumps(creator.get("@type", "").upper())
                )            
        cursor.execute(query)

    def __seed_genre(self, cursor, genre, url):
        """Seed genre into the database.

        Args:
            cursor (mysql.cursor): Mysql cursor which is used to seed the database.
            genre (str): The genre string to insert.
            url (str): The URL of entity to which genre belongs to.
        """

        query = "INSERT INTO genre values ({}, {});".format(
                    json.dumps(url), 
                    json.dumps(genre)
                )
        cursor.execute(query)

    def __seed_review(self, cursor, review, url):
        """Seed review into the database.

        Args:
            cursor (mysql.cursor): Mysql cursor which is used to seed the database.
            review (object): The JSON-LD review object to insert.
            url (str): The URL of entity to which review belongs to.
        """

        if "reviewRating" in review:
            query = "INSERT INTO review values ({}, {}, {}, {}, {}, {}, {}, {}, {})".format(
                        json.dumps(url),
                        json.dumps(review["author"].get("name","")),
                        json.dumps(review.get("dateCreated","")),
                        json.dumps(review.get("inLanguage", "")),
                        json.dumps(review.get("name", "")),
                        json.dumps(review.get("reviewBody", "")),
                        review["reviewRating"].get("ratingValue",0),
                        review["reviewRating"].get("bestRating", 0),
                        review["reviewRating"].get("worstRating", 0)
                    )
        else:
            query = "INSERT INTO review (entity_url, author, date_created, language, name, review_body) values ({}, {}, {}, {}, {}, {})".format(
                        json.dumps(url),
                        json.dumps(review["author"].get("name","")),
                        json.dumps(review.get("dateCreated","")),
                        json.dumps(review.get("inLanguage", "")),
                        json.dumps(review.get("name", "")),
                        json.dumps(review.get("reviewBody", ""))
                    )

        cursor.execute(query)

    def __seed_trailer(self, cursor, trailer, url):
        """Seed trailer into the database.

        Args:
            cursor (mysql.cursor): Mysql cursor which is used to seed the database.
            trailer (object): The JSON-LD trailer object to insert.
            url (str): The URL of entity to which trailer belongs to.
        """

        query = "INSERT INTO trailer values( {}, {}, {}, {}, {},{})".format(
                    json.dumps(trailer.get("name", "")),
                    json.dumps(trailer.get("embedUrl", "")),
                    json.dumps(trailer.get("thumbnailUrl", "")),
                    json.dumps(trailer.get("description", "")),
                    json.dumps(self.__get_datetime(trailer.get("uploadDate", ""))),
                    json.dumps(url)
                )
        cursor.execute(query)
    
    def __get_duration(self, x):
        """Parse ISO8601 duration and return minutes.

        Args:
            int: Duration as minutes.
        """

        duration = isodate.parse_duration(x)
        minutes = int(duration.seconds/60)
        return minutes

    def __get_datetime(self, x):
        """Parse ISO8601 datetime and return ISO9075 datetime.

        Args:
            str: ISO9075 string.
        """
        dt = parser.isoparse(x)
        formatted_date = dt.strftime('%Y-%m-%d %H:%M:%S')
        return formatted_date
