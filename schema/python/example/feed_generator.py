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


class IMDBExample:
    """The IMDBExample reads the database to generate proto ItemList object
    from movies, series and episodes used for generating JSON-LD feed."""

    def get_feed(self, cursor, schema):
        """Call __get_movies, __get_series, __get_episodes and generate feed.

        Args:
            cursor (mysql.cursor): Mysql cursor which is used to query the database.
            schema (module): The compiled protobuf schema.
        """

        for x in self.__get_movies(cursor, schema):
            yield x

        for x in self.__get_series(cursor, schema):
            yield x

        for x in self.__get_episodes(cursor, schema):
            yield x

    def __get_movies(self, cursor, schema):
        """Make proto objects for movies and yield each movie.

        Args:
            cursor (mysql.cursor): Mysql cursor which is used to query the database.
            schema (module): The compiled protobuf schema.
        """

        query = """
        select
        m.url as url,
        m.name as name,
        m.image as image,
        m.content_rating as content_rating,
        m.description as description,
        m.date_published as date_published,
        m.keywords as keywords,
        m.duration_minutes as duration_minutes,
        m.rating_count as rating_count,
        m.rating as rating,
        m.best_rating as best_rating,
        m.worst_rating as worst_rating,
        (select JSON_ARRAYAGG(JSON_OBJECT(
            'name', name
            )) from genre where genre.entity_url=m.url) as genres,
        (select JSON_ARRAYAGG(JSON_OBJECT(
            'name', name,
            'url', url
            )) from actor where actor.entity_url=m.url) as actors,
        (select JSON_ARRAYAGG(JSON_OBJECT(
            'name', name,
            'url', url
            )) from director where director.entity_url=m.url) as directors,
        (select JSON_ARRAYAGG(JSON_OBJECT(
            'name', name,
            'url', url,
            'type', type
            )) from creator where creator.entity_url=m.url) as creators,
        (select JSON_ARRAYAGG(JSON_OBJECT(
            'author', author,
            'date_created', date_created,
            'language', language,
            'name', name,
            'review_body', review_body,
            'rating', rating,
            'best_rating', best_rating,
            'worst_rating', worst_rating
            )) from review where review.entity_url=m.url) as reviews,
        (select JSON_ARRAYAGG(JSON_OBJECT(
            'name', name,
            'embed_url', embed_url,
            'thumbnail_url', thumbnail_url,
            'description', description,
            'upload_date', upload_date
            )) from trailer where trailer.entity_url=m.url) as trailers

        from movie m;
        """
        cursor.execute(query)

        m = cursor.fetchone()
        while m is not None:
            movie = schema.Movie()

            if m['url']:
                movie.url.add().url = m['url']
                movie.id = m['url']

            if m['name']:
                movie.name.add().text = m['name']

            if m['image']:
                movie.image.add().url = m['image']

            if m['content_rating']:
                movie.content_rating.add().text = m['content_rating']

            if m['description']:
                movie.description.add().text = m['description']

            if m['date_published']:
                date_published = movie.date_published.add().date
                date_published = self.__add_date(
                    date_published, m['date_published'])

            if m['keywords']:
                movie.keywords.add().text = m['keywords']

            if m['duration_minutes']:
                duration = movie.duration.add().duration
                duration = self.__add_duration(duration, m['duration_minutes'])

            if m['rating']:
                aggregate_rating = movie.aggregate_rating.add().aggregate_rating

                if m['rating_count']:
                    aggregate_rating.rating_count.add(
                    ).integer = int(m['rating_count'])

                if m['rating']:
                    aggregate_rating.rating_value.add(
                    ).number = float(m['rating'])

                if m['best_rating']:
                    aggregate_rating.best_rating.add(
                    ).number = float(m['best_rating'])

                if m['worst_rating']:
                    aggregate_rating.worst_rating.add(
                    ).number = float(m['worst_rating'])

            if m['genres']:
                movie = self.__add_genres(movie, json.loads(m['genres']))
            if m['actors']:
                movie = self.__add_actors(movie, json.loads(m['actors']))
            if m['directors']:
                movie = self.__add_directors(movie, json.loads(m['directors']))
            if m['creators']:
                movie = self.__add_creators(movie, json.loads(m['creators']))
            if m['reviews']:
                movie = self.__add_reviews(
                    m['url'], movie, json.loads(
                        m['reviews']))
            if m['trailers']:
                movie = self.__add_trailers(movie, json.loads(m['trailers']))

            yield movie
            m = cursor.fetchone()

    def __get_series(self, cursor, schema):
        """Make proto objects for series and and yield each TVSeries.

        Args:
            cursor (mysql.cursor): Mysql cursor which is used to query the database.
            schema (module): The compiled protobuf schema.
        """

        query = """
        select
        m.url as url,
        m.name as name,
        m.image as image,
        m.content_rating as content_rating,
        m.description as description,
        m.date_published as date_published,
        m.keywords as keywords,
        m.rating_count as rating_count,
        m.rating as rating,
        m.best_rating as best_rating,
        m.worst_rating as worst_rating,
        (select JSON_ARRAYAGG(JSON_OBJECT(
            'name', name
            )) from genre where genre.entity_url=m.url) as genres,
        (select JSON_ARRAYAGG(JSON_OBJECT(
            'name', name,
            'url', url
            )) from actor where actor.entity_url=m.url) as actors,
        (select JSON_ARRAYAGG(JSON_OBJECT(
            'name', name,
            'url', url
            )) from director where director.entity_url=m.url) as directors,
        (select JSON_ARRAYAGG(JSON_OBJECT(
            'name', name,
            'url', url,
            'type', type
            )) from creator where creator.entity_url=m.url) as creators,
        (select JSON_ARRAYAGG(JSON_OBJECT(
            'author', author,
            'date_created', date_created,
            'language', language,
            'name', name,
            'review_body', review_body,
            'rating', rating,
            'best_rating', best_rating,
            'worst_rating', worst_rating
            )) from review where review.entity_url=m.url) as reviews,
        (select JSON_ARRAYAGG(JSON_OBJECT(
            'name', name,
            'embed_url', embed_url,
            'thumbnail_url', thumbnail_url,
            'description', description,
            'upload_date', upload_date
            )) from trailer where trailer.entity_url=m.url) as trailers

        from series m;
        """
        cursor.execute(query)

        m = cursor.fetchone()
        while m is not None:
            tvseries = schema.TVSeries()

            if m['url']:
                tvseries.url.add().url = m['url']
                tvseries.id = m['url']

            if m['name']:
                tvseries.name.add().text = m['name']

            if m['image']:
                tvseries.image.add().url = m['image']

            if m['content_rating']:
                tvseries.content_rating.add().text = m['content_rating']

            if m['description']:
                tvseries.description.add().text = m['description']

            if m['date_published']:
                date_published = tvseries.date_published.add().date
                date_published = self.__add_date(
                    date_published, m['date_published'])

            if m['keywords']:
                tvseries.keywords.add().text = m['keywords']

            if m['rating']:
                aggregate_rating = tvseries.aggregate_rating.add().aggregate_rating

                if m['rating_count']:
                    aggregate_rating.rating_count.add(
                    ).integer = int(m['rating_count'])

                if m['rating']:
                    aggregate_rating.rating_value.add(
                    ).number = float(m['rating'])

                if m['best_rating']:
                    aggregate_rating.best_rating.add(
                    ).number = float(m['best_rating'])

                if m['worst_rating']:
                    aggregate_rating.worst_rating.add(
                    ).number = float(m['worst_rating'])

            if m['genres']:
                tvseries = self.__add_genres(tvseries, json.loads(m['genres']))
            if m['actors']:
                tvseries = self.__add_actors(tvseries, json.loads(m['actors']))
            if m['directors']:
                tvseries = self.__add_directors(
                    tvseries, json.loads(m['directors']))
            if m['creators']:
                tvseries = self.__add_creators(
                    tvseries, json.loads(m['creators']))
            if m['reviews']:
                tvseries = self.__add_reviews(
                    m['url'], tvseries, json.loads(m['reviews']))
            if m['trailers']:
                tvseries = self.__add_trailers(
                    tvseries, json.loads(m['trailers']))

            yield tvseries
            m = cursor.fetchone()

    def __get_episodes(self, cursor, schema):
        """Make proto objects for episodes and and yield each episode.

        Args:
            cursor (mysql.cursor): Mysql cursor which is used to query the database.
            schema (module): The compiled protobuf schema.
        """

        query = """
        select
        m.url as url,
        m.name as name,
        m.image as image,
        m.content_rating as content_rating,
        m.description as description,
        m.date_published as date_published,
        m.keywords as keywords,
        m.duration_minutes as duration_minutes,
        m.rating_count as rating_count,
        m.rating as rating,
        m.best_rating as best_rating,
        m.worst_rating as worst_rating,
        (select JSON_ARRAYAGG(JSON_OBJECT(
            'name', name
            )) from genre where genre.entity_url=m.url) as genres,
        (select JSON_ARRAYAGG(JSON_OBJECT(
            'name', name,
            'url', url
            )) from actor where actor.entity_url=m.url) as actors,
        (select JSON_ARRAYAGG(JSON_OBJECT(
            'name', name,
            'url', url
            )) from director where director.entity_url=m.url) as directors,
        (select JSON_ARRAYAGG(JSON_OBJECT(
            'name', name,
            'url', url,
            'type', type
            )) from creator where creator.entity_url=m.url) as creators,
        (select JSON_ARRAYAGG(JSON_OBJECT(
            'author', author,
            'date_created', date_created,
            'language', language,
            'name', name,
            'review_body', review_body,
            'rating', rating,
            'best_rating', best_rating,
            'worst_rating', worst_rating
            )) from review where review.entity_url=m.url) as reviews,
        (select JSON_ARRAYAGG(JSON_OBJECT(
            'name', name,
            'embed_url', embed_url,
            'thumbnail_url', thumbnail_url,
            'description', description,
            'upload_date', upload_date
            )) from trailer where trailer.entity_url=m.url) as trailers

        from episode m;
        """
        cursor.execute(query)

        m = cursor.fetchone()
        while m is not None:
            episode = schema.TVEpisode()

            if m['url']:
                episode.url.add().url = m['url']
                episode.id = m['url']

            if m['name']:
                episode.name.add().text = m['name']

            if m['image']:
                episode.image.add().url = m['image']

            if m['content_rating']:
                episode.content_rating.add().text = m['content_rating']

            if m['description']:
                episode.description.add().text = m['description']

            if m['date_published']:
                date_published = episode.date_published.add().date
                date_published = self.__add_date(
                    date_published, m['date_published'])

            if m['keywords']:
                episode.keywords.add().text = m['keywords']

            if m['duration_minutes']:
                duration = episode.time_required.add().duration
                duration = self.__add_duration(duration, m['duration_minutes'])

            if m['rating']:
                aggregate_rating = episode.aggregate_rating.add().aggregate_rating

                if m['rating_count']:
                    aggregate_rating.rating_count.add(
                    ).integer = int(m['rating_count'])

                if m['rating']:
                    aggregate_rating.rating_value.add(
                    ).number = float(m['rating'])

                if m['best_rating']:
                    aggregate_rating.best_rating.add(
                    ).number = float(m['best_rating'])

                if m['worst_rating']:
                    aggregate_rating.worst_rating.add(
                    ).number = float(m['worst_rating'])

            if m['genres']:
                episode = self.__add_genres(episode, json.loads(m['genres']))
            if m['actors']:
                episode = self.__add_actors(episode, json.loads(m['actors']))
            if m['directors']:
                episode = self.__add_directors(
                    episode, json.loads(m['directors']))
            if m['creators']:
                episode = self.__add_creators(
                    episode, json.loads(m['creators']))
            if m['reviews']:
                episode = self.__add_reviews(
                    m['url'], episode, json.loads(m['reviews']))
            if m['trailers']:
                episode = self.__add_trailers(
                    episode, json.loads(m['trailers']))

            yield episode
            m = cursor.fetchone()

    def __add_date(self, date_proto, date_obj):
        """Set fields of date proto object from python date object or python
        date string.

        Args:
            date_proto (proto object): Date proto object.
            date_obj (datetime.date | string): Datetime date object or mysql date string.

        Returns:
            date_proto (proto object): Date proto object with fields set.
        """

        if isinstance(date_obj, str):
            date_obj = datetime.strptime(date_obj, '%Y-%m-%d')

        date_proto.year = date_obj.year
        date_proto.month = date_obj.month
        date_proto.day = date_obj.day
        return date_proto

    def __add_date_from_datetime(self, date_proto, datetime_obj):
        """Set fields of date proto object from python datetime object or mysql
        datetime string.

        Args:
            date_proto (proto object): Date proto object.
            datetime_obj (datetime.datetime | string): Datetime date object or mysql datetime string.

        Returns:
            date_proto (proto object): Date proto object with fields set.
        """

        if isinstance(datetime_obj, str):
            datetime_obj = datetime.strptime(
                datetime_obj, '%Y-%m-%d %H:%M:%S.%f')

        date_proto.year = datetime_obj.year
        date_proto.month = datetime_obj.month
        date_proto.day = datetime_obj.day
        return date_proto

    def __add_duration(self, duration_proto, duration_minutes):
        """Set fields of duration proto object from duration in minutes.

        Args:
            duration_proto (proto object): Duration proto object.
            duration_minutes (integer): Duration in minutes.

        Returns:
            duration_proto (proto object): Duration proto object with fields set.
        """
        duration_proto.seconds = duration_minutes * 60
        return duration_proto

    def __add_genres(self, entity, genres):
        """Make proto objects for genres and add them to entity.

        Args:
            entity (schema object): Schema object to which genres need to be added.
            genres (list): List of genres to be added.

        Returns:
            entity (schema object): Updated entity which includes genres.
        """

        for x in genres:
            entity.genre.add().text = x['name']

        return entity

    def __add_actors(self, entity, actors):
        """Make proto objects for actors and add them to entity.

        Args:
            entity (schema object): Schema object to which actors need to be added.
            actors (list): List of actors to be added.

        Returns:
            entity (schema object): Updated entity which includes actors.
        """

        for x in actors:
            person = entity.actor.add().person
            if x['name']:
                person.name.add().text = x['name']
            if x['url']:
                person.url.add().url = x['url']
                person.id = x['url']

        return entity

    def __add_directors(self, entity, directors):
        """Make proto objects for directors and add them to entity.

        Args:
            entity (schema object): Schema object to which directors need to be added.
            directors (list): List of directors to be added.

        Returns:
            entity (schema object): Updated entity which includes directors.
        """

        for x in directors:
            person = entity.director.add().person
            if x['name']:
                person.name.add().text = x['name']
            if x['url']:
                person.url.add().url = x['url']
                person.id = x['url']

        return entity

    def __add_creators(self, entity, creators):
        """Make proto objects for creators and add them to entity.

        Args:
            entity (schema object): Schema object to which creators need to be added.
            creators (list): List of creators to be added.

        Returns:
            entity (schema object): Updated entity which includes creators.
        """

        for x in creators:
            if x['type'] == 'PERSON':
                person = entity.creator.add().person
                if x['name']:
                    person.name.add().text = x['name']
                if x['url']:
                    person.url.add().url = x['url']
                    person.id = x['url']
            elif x['type'] == 'ORGANIZATION':
                organization = entity.creator.add().organization
                if x['name']:
                    organization.name.add().text = x['name']
                if x['url']:
                    organization.url.add().url = x['url']
                    organization.id = x['url']

        return entity

    def __add_reviews(self, url, entity, reviews):
        """Make proto objects for reviews and add them to entity.

        Args:
            url (str): The url of entity whose reviews need to be added.
            entity (schema object): Schema object to which reviews need to be added.
            reviews (list): List of reviews to be added.

        Returns:
            entity (schema object): Updated entity which includes reviews.
        """

        for x in reviews:
            review = entity.review.add().review

            if x['author']:
                review.author.add().person.name.add().text = x['author']

            if x['date_created']:
                date_created = review.date_created.add().date
                self.__add_date(date_created, x['date_created'])

            if x['language']:
                review.in_language.add().text = x['language']

            if x['name']:
                review.name.add().text = x['name']

            if x['review_body']:
                review.review_body.add().text = x['review_body']

            if x['rating']:
                rating = review.review_rating.add().rating
                rating.rating_value.add().number = float(x['rating'])

                if x['best_rating']:
                    rating.best_rating.add().number = float(x['best_rating'])
                if x['worst_rating']:
                    rating.worst_rating.add().number = float(x['worst_rating'])

            review.item_reviewed.add().creative_work.url.add().url = url

        return entity

    def __add_trailers(self, entity, trailers):
        """Make proto objects for trailers and add them to entity.

        Args:
            entity (schema object): Schema object to which trailers need to be added.
            trailers (list): List of trailers to be added.

        Returns:
            entity (schema object): Updated entity which includes trailers.
        """

        for x in trailers:
            trailer = entity.trailer.add().video_object

            if x['name']:
                trailer.name.add().text = x['name']

            if x['embed_url']:
                trailer.embed_url.add().url = x['embed_url']
                trailer.id = x['embed_url']

            if x['thumbnail_url']:
                trailer.thumbnail_url.add().url = x['thumbnail_url']
                trailer.thumbnail.add().image_object.content_url.add(
                ).url = x['thumbnail_url']

            if x['description']:
                trailer.description.add().text = x['description']

            if x['upload_date']:
                date_obj = trailer.upload_date.add().date
                self.__add_date_from_datetime(date_obj, x['upload_date'])
        return entity
