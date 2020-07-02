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
import json
from datetime import datetime
from datetime import date
from datetime import time

class IMDBExample:
    """The IMDBExample reads the database to generate proto ItemList object from movies, series and episodes used for generating JSON-LD feed.

    Attributes:
        _position (int): Next available position in the itemlist.
    """

    def __init__(self):
        self._position = 1
    
    def generate_feed(self,cursor, schema, serializer):
        """Call __movies_to_proto, __series_to_proto, __episodes_to_proto and populate ItemList.

        Args:
            cursor (mysql.cursor): Mysql cursor which is used to query the database.
            schema (module): The compiled protobuf schema.
            serializer (schemaorgutils.JSONLDFeedSerializer): To serialize feed.

        """

        self.__movies_to_proto( cursor, schema, serializer)
        self.__series_to_proto( cursor, schema, serializer)
        self.__episodes_to_proto( cursor, schema, serializer)

    def __movies_to_proto(self, cursor, schema, serializer):
        """Make proto objects for movies and add them to ItemList.

        Args:
            cursor (mysql.cursor): Mysql cursor which is used to query the database.
            schema (module): The compiled protobuf schema.
            serializer (schemaorgutils.JSONLDFeedSerializer): To serialize feed.

        """
        
        cursor.execute("SELECT url, name , image , content_rating , description , date_published , keywords , duration_minutes , rating_count , rating , best_rating , worst_rating from movie;")

        query_list = list(cursor)

        for m in query_list:
            movie = schema.Movie()

            if m[0]:
                movie.url.add().url = m[0]
                movie.id = m[0]

            if m[1]:
                movie.name.add().text = m[1]

            if m[2]:
                movie.image.add().url = m[2]

            if m[3]:
                movie.content_rating.add().text=m[3]

            if m[4]:
                movie.description.add().text = m[4]

            if m[5]:
                date_published = movie.date_published.add().date
                date_published = self.__add_date(date_published, m[5])

            if m[6]:
                movie.keywords.add().text = m[6]

            if m[7]:
                duration = movie.duration.add().duration
                duration = self.__add_duration(duration, m[7])

            if m[9]:
                aggregate_rating = movie.aggregate_rating.add().aggregate_rating

                if m[8]:
                    aggregate_rating.rating_count.add().integer = int(m[8])

                if m[9]:
                    aggregate_rating.rating_value.add().number = float(m[9])

                if m[10]:
                    aggregate_rating.best_rating.add().number = float(m[10])

                if m[11]:
                    aggregate_rating.worst_rating.add().number = float(m[11])

            movie = self.__add_genres(m[0], movie, cursor)
            movie = self.__add_actors(m[0], movie, cursor)
            movie = self.__add_directors(m[0], movie, cursor)
            movie = self.__add_creators(m[0], movie, cursor)
            movie = self.__add_reviews(m[0], movie, cursor)
            movie = self.__add_trailers(m[0], movie, cursor)
            serializer.add_item(movie, schema)


    def __series_to_proto(self, cursor, schema, serializer):
        """Make proto objects for series and add them to ItemList.

        Args:
            cursor (mysql.cursor): Mysql cursor which is used to query the database.
            schema (module): The compiled protobuf schema.
            serializer (schemaorgutils.JSONLDFeedSerializer): To serialize feed.

        """
        
        cursor.execute("SELECT url, name , image , content_rating , description , date_published , keywords , rating_count , rating , best_rating , worst_rating from series;")

        query_list = list(cursor)

        for m in query_list:
            tv_series = schema.TVSeries()

            if m[0]:
                tv_series.id = m[0]
                tv_series.url.add().url = m[0]

            if m[1]:
                tv_series.name.add().text = m[1]

            if m[2]:
                tv_series.image.add().url = m[2]

            if m[3]:
                tv_series.content_rating.add().text=m[3]

            if m[4]:
                tv_series.description.add().text = m[4]

            if m[5]:
                date_published = tv_series.date_published.add().date
                date_published = self.__add_date(date_published, m[5])

            if m[6]:
                tv_series.keywords.add().text = m[6]

            if m[8]:
                aggregate_rating = tv_series.aggregate_rating.add().aggregate_rating

                if m[7]:
                    aggregate_rating.rating_count.add().integer = int(m[7])

                if m[8]:
                    aggregate_rating.rating_value.add().number = float(m[8])

                if m[9]:
                    aggregate_rating.best_rating.add().number = float(m[9])
                    
                if m[10]:
                    aggregate_rating.worst_rating.add().number = float(m[10])

            tv_series = self.__add_genres(m[0], tv_series, cursor)
            tv_series = self.__add_actors(m[0], tv_series, cursor)
            tv_series = self.__add_directors(m[0], tv_series, cursor)
            tv_series = self.__add_creators(m[0], tv_series, cursor)
            tv_series = self.__add_reviews(m[0], tv_series, cursor)
            tv_series = self.__add_trailers(m[0], tv_series, cursor)
            serializer.add_item(tv_series, schema)


    def __episodes_to_proto(self, cursor, schema, serializer):
        """Make proto objects for episodes and add them to ItemList.

        Args:
            cursor (mysql.cursor): Mysql cursor which is used to query the database.
            schema (module): The compiled protobuf schema.
            serializer (schemaorgutils.JSONLDFeedSerializer): To serialize feed.
            
        """

        cursor.execute("SELECT url, name , image , content_rating , description , date_published , keywords , duration_minutes , rating_count , rating , best_rating , worst_rating from episode;")

        query_list = list(cursor)

        for m in query_list:
            tv_episode = schema.TVEpisode()

            if m[0]:
                tv_episode.url.add().url = m[0]
                tv_episode.id = m[0]

            if m[1]:
                tv_episode.name.add().text = m[1]

            if m[2]:
                tv_episode.image.add().url = m[2]

            if m[3]:
                tv_episode.content_rating.add().text=m[3]

            if m[4]:
                tv_episode.description.add().text = m[4]

            if m[5]:
                date_published = tv_episode.date_published.add().date
                date_published = self.__add_date(date_published, m[5])

            if m[6]:
                tv_episode.keywords.add().text = m[6]

            if m[7]:
                duration = tv_episode.time_required.add().duration
                duration = self.__add_duration(duration, m[7])

            if m[9]:
                aggregate_rating = tv_episode.aggregate_rating.add().aggregate_rating

                if m[8]:
                    aggregate_rating.rating_count.add().integer = int(m[8])

                if m[9]:
                    aggregate_rating.rating_value.add().number = float(m[9])

                if m[10]:
                    aggregate_rating.best_rating.add().number = float(m[10])

                if m[11]:
                    aggregate_rating.worst_rating.add().number = float(m[11])

            tv_episode = self.__add_genres(m[0], tv_episode, cursor)
            tv_episode = self.__add_actors(m[0], tv_episode, cursor)
            tv_episode = self.__add_directors(m[0], tv_episode, cursor)
            tv_episode = self.__add_creators(m[0], tv_episode, cursor)
            tv_episode = self.__add_reviews(m[0], tv_episode, cursor)
            tv_episode = self.__add_trailers(m[0], tv_episode, cursor)
            serializer.add_item(tv_episode, schema)


    def __add_date(self, date_proto, date_obj):
        """Set fields of date proto object from python date object.

        Args:
            cursor (mysql.cursor): Mysql cursor which is used to query the database.
            date_proto (proto object): Date proto object.
            date_obj (date object): Python date object.
        
        Returns:
            date_proto (proto object): Date proto object with fields set.
        """

        date_proto.year = date_obj.year
        date_proto.month = date_obj.month
        date_proto.day = date_obj.day
        return date_proto

    def __add_datetime(self, datetime_proto, datetime_obj):
        """Set fields of datetime proto object from python date object.

        Args:
            cursor (mysql.cursor): Mysql cursor which is used to query the database.
            datetime_proto (proto object): Datetime proto object.
            datetime_obj (datetime object): Python datetime object.
        
        Returns:
            datetime_proto (proto object): Datetime proto object with fields set.
        """

        datetime_obj.time.hours = datetime_obj.hours
        datetime_obj.time.minutes = datetime_obj.minutes
        datetime_obj.time.seconds = datetime_obj.seconds

        return datetime_obj

    def __add_duration(self, duration_proto, duration_minutes):

        duration_proto.seconds = duration_minutes * 60
        return duration_proto


    def __add_genres(self, url, entity, cursor):
        """Make proto objects for genres and add them to entity.

        Args:
            cursor (mysql.cursor): Mysql cursor which is used to query the database.
            url (str): The url of entity whose genres need to be added.
            entity (schema object): Schema object to which genres need to be added.
        
        Returns:
            entity (schema object): Updated entity which includes genres.
        """

        cursor.execute("SELECT name from genre where entity_url = {};".format(json.dumps(url))) 

        for x in cursor:
            entity.genre.add().text = x[0]

        return entity

    def __add_actors(self, url, entity, cursor):
        """Make proto objects for actors and add them to entity.

        Args:
            cursor (mysql.cursor): Mysql cursor which is used to query the database.
            url (str): The url of entity whose actors need to be added.
            entity (schema object): Schema object to which actors need to be added.
        
        Returns:
            entity (schema object): Updated entity which includes actors.
        """

        cursor.execute("SELECT url, name from actor where entity_url = {};".format(json.dumps(url))) 
        
        for x in cursor:
            person = entity.actor.add().person
            if x[1]:
                person.name.add().text = x[1]
            if x[0]:
                person.url.add().url = x[0]
                person.id = x[0]

        return entity

    def __add_directors(self, url, entity, cursor):
        """Make proto objects for directors and add them to entity.

        Args:
            cursor (mysql.cursor): Mysql cursor which is used to query the database.
            url (str): The url of entity whose directors need to be added.
            entity (schema object): Schema object to which directors need to be added.
        
        Returns:
            entity (schema object): Updated entity which includes directors.
        """

        cursor.execute("SELECT url, name from director where entity_url = {};".format(json.dumps(url))) 
        
        for x in cursor:
            person = entity.director.add().person
            if x[1]:
                person.name.add().text = x[1]
            if x[0]:
                person.url.add().url = x[0]
                person.id = x[0]

        return entity

    def __add_creators(self, url, entity, cursor):
        """Make proto objects for creators and add them to entity.

        Args:
            cursor (mysql.cursor): Mysql cursor which is used to query the database.
            url (str): The url of entity whose creators need to be added.
            entity (schema object): Schema object to which creators need to be added.
        
        Returns:
            entity (schema object): Updated entity which includes creators.
        """

        cursor.execute("SELECT url, name, type from creator where entity_url = {};".format(json.dumps(url))) 
        
        for x in cursor:
            if x[2] == "PERSON":
                person = entity.creator.add().person
                if x[1]:
                    person.name.add().text = x[1]
                if x[0]:
                    person.url.add().url = x[0]
                    person.id = x[0]
            elif x[2] == "ORGANIZATION":
                organization = entity.creator.add().organization
                if x[1]:
                    organization.name.add().text = x[1]
                if x[0]:
                    organization.url.add().url = x[0]
                    organization.id = x[0]

        return entity

    def __add_reviews(self, url, entity, cursor):
        """Make proto objects for reviews and add them to entity.

        Args:
            cursor (mysql.cursor): Mysql cursor which is used to query the database.
            url (str): The url of entity whose reviews need to be added.
            entity (schema object): Schema object to which reviews need to be added.
        
        Returns:
            entity (schema object): Updated entity which includes reviews.
        """

        cursor.execute("SELECT author , date_created , language , name , review_body , rating , best_rating , worst_rating from review where entity_url = {};".format(json.dumps(url)))
        
        for x in cursor:
            review = entity.review.add().review

            if x[0]:
                review.author.add().person.name.add().text = x[0]

            if x[1]:
                date_created = review.date_created.add().date
                self.__add_date(date_created, x[1])

            if x[2]:
                review.in_language.add().text = x[2]

            if x[3]:
                review.name.add().text = x[3]

            if x[4]:
                review.review_body.add().text = x[4]
            
            if x[5]: 
                rating = review.review_rating.add().rating
                rating.rating_value.add().number = float(x[5])

                if x[6]:
                    rating.best_rating.add().number = float(x[6])
                if x[7]:
                    rating.worst_rating.add().number = float(x[7])
            
            review.item_reviewed.add().creative_work.url.add().url = url

        return entity

    def __add_trailers(self, url, entity, cursor):
        """Make proto objects for trailers and add them to entity.

        Args:
            cursor (mysql.cursor): Mysql cursor which is used to query the database.
            url (str): The url of entity whose trailers need to be added.
            entity (schema object): Schema object to which trailers need to be added.
        
        Returns:
            entity (schema object): Updated entity which includes trailers.
        """

        cursor.execute("SELECT name, embed_url, thumbnail_url , description , upload_date from trailer where entity_url = {}".format(json.dumps(url)))

        for x in cursor:
            trailer = entity.trailer.add().video_object
            
            if x[0]:
                trailer.name.add().text = x[0]
            
            if x[1]:
                trailer.embed_url.add().url = x[1]
                trailer.id = x[1]
            
            if x[2]:
                trailer.thumbnail_url.add().url = x[2]
                trailer.thumbnail.add().image_object.content_url.add().url = x[2]
            
            if x[3]:
                trailer.description.add().text = x[3]

            if x[4]:
                date_obj = trailer.upload_date.add().date
                self.__add_date(date_obj, x[4])
        return entity

