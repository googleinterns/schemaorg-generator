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
const pEvent = require('p-event');
const moment = require('moment');
class IMDBExample{

    async moviesToProto(con, schema, serializer, schemaDescriptor){

        let q = `select 
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
                    `;

        
        let result = con.query(q).stream();
        const movies = pEvent.iterator(result, 'data', {
            resolutionEvents: ['end']
        });

        for await (let m of movies){
            let movie = new schema.Movie();

            if(m["url"]){
                let url = new schema.UrlProperty();
                url.setUrl(m["url"]);
                movie.addUrl(url);
                movie.setId(m["url"]);
            }

            if(m["name"]){
                let name = new schema.NameProperty();
                name.setText(m["name"]);
                movie.addName(name);
            }

            if(m["image"]){
                let image = new schema.ImageProperty();
                image.setUrl(m["image"]);
                movie.addImage(image);
            }

            if(m["content_rating"]){
                let contentRating = new schema.ContentRatingProperty();
                contentRating.setText(m["name"]);
                movie.addContentRating(contentRating);
            }

            if(m["description"]){
                let description = new schema.DescriptionProperty();
                description.setText(m["description"]);
                movie.addDescription(description);
            }

            if(m["date_published"]){
                let datePublished = new schema.DatePublishedProperty();
                datePublished.setDate(this.addDate(m["date_published"], schema));
                movie.addDatePublished(datePublished);
            }

            if(m["keywords"]){
                let keywords = new schema.KeywordsProperty();
                keywords.setText(m["keywords"]);
                movie.addKeywords(keywords);
            }

            if(m["duration_minutes"]){
                let duration = new schema.DurationProperty();
                duration.setDuration(this.addDuration(m["duration_minutes"], schema));
                movie.addDuration(duration);
            }

            if(m["rating"]){
                let aggregateRatingProp = new schema.AggregateRatingProperty();
                let aggregateRating = new schema.AggregateRating();

                if(m["rating_count"]){
                    let ratingCount = new schema.RatingCountProperty();
                    ratingCount.setInteger(m["rating_count"]);
                    aggregateRating.addRatingCount(ratingCount);
                }

                if(m["rating"]){
                    let ratingValue = new schema.RatingValueProperty();
                    ratingValue.setNumber(m["rating"]);
                    aggregateRating.addRatingValue(ratingValue);
                }

                if(m["best_rating"]){
                    let bestRating = new schema.BestRatingProperty();
                    bestRating.setNumber(m["best_rating"]);
                    aggregateRating.addBestRating(bestRating);
                }

                if(m["worst_rating"]){
                    let worstRating = new schema.WorstRatingProperty();
                    worstRating.setNumber(m["worst_rating"]);
                    aggregateRating.addWorstRating(worstRating);
                }
                aggregateRatingProp.setAggregateRating(aggregateRating);
                movie.addAggregateRating(aggregateRatingProp);
            }

            if(m["actors"]){
                movie = this.addActors(JSON.parse(m["actors"]), schema, movie);
            }

            if(m["directors"]){
                movie = this.addDirectors(JSON.parse(m["directors"]), schema, movie);
            }
            
            if(m["creators"]){
                movie = this.addCreators(JSON.parse(m["creators"]), schema, movie);
            }
            
            if(m["genres"]){
                movie = this.addGenres(JSON.parse(m["genres"]), schema, movie);
            }
            
            if(m["reviews"]){
                movie = this.addReviews(JSON.parse(m["reviews"]), schema, movie, m["url"]);
            }
            
            if(m["trailers"]){
                movie = this.addTrailers(JSON.parse(m["trailers"]), schema, movie);
            }
            

            serializer.addItem(movie, "Movie", schemaDescriptor);

        }
    }

    async seriesToProto(con, schema, serializer, schemaDescriptor){

        let q = `select 
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
                    `;

        
        let result = con.query(q).stream();
        const series = pEvent.iterator(result, 'data', {
            resolutionEvents: ['end']
        });

        for await (let m of series){
            let tvseries = new schema.TVSeries();

            if(m["url"]){
                let url = new schema.UrlProperty();
                url.setUrl(m["url"]);
                tvseries.addUrl(url);
                tvseries.setId(m["url"]);
            }

            if(m["name"]){
                let name = new schema.NameProperty();
                name.setText(m["name"]);
                tvseries.addName(name);
            }

            if(m["image"]){
                let image = new schema.ImageProperty();
                image.setUrl(m["image"]);
                tvseries.addImage(image);
            }

            if(m["content_rating"]){
                let contentRating = new schema.ContentRatingProperty();
                contentRating.setText(m["name"]);
                tvseries.addContentRating(contentRating);
            }

            if(m["description"]){
                let description = new schema.DescriptionProperty();
                description.setText(m["description"]);
                tvseries.addDescription(description);
            }

            if(m["date_published"]){
                let datePublished = new schema.DatePublishedProperty();
                datePublished.setDate(this.addDate(m["date_published"], schema));
                tvseries.addDatePublished(datePublished);
            }

            if(m["keywords"]){
                let keywords = new schema.KeywordsProperty();
                keywords.setText(m["keywords"]);
                tvseries.addKeywords(keywords);
            }

            if(m["rating"]){
                let aggregateRatingProp = new schema.AggregateRatingProperty();
                let aggregateRating = new schema.AggregateRating();

                if(m["rating_count"]){
                    let ratingCount = new schema.RatingCountProperty();
                    ratingCount.setInteger(m["rating_count"]);
                    aggregateRating.addRatingCount(ratingCount);
                }

                if(m["rating"]){
                    let ratingValue = new schema.RatingValueProperty();
                    ratingValue.setNumber(m["rating"]);
                    aggregateRating.addRatingValue(ratingValue);
                }

                if(m["best_rating"]){
                    let bestRating = new schema.BestRatingProperty();
                    bestRating.setNumber(m["best_rating"]);
                    aggregateRating.addBestRating(bestRating);
                }

                if(m["worst_rating"]){
                    let worstRating = new schema.WorstRatingProperty();
                    worstRating.setNumber(m["worst_rating"]);
                    aggregateRating.addWorstRating(worstRating);
                }
                aggregateRatingProp.setAggregateRating(aggregateRating);
                tvseries.addAggregateRating(aggregateRatingProp);
            }

            if(m["actors"]){
                tvseries = this.addActors(JSON.parse(m["actors"]), schema, tvseries);
            }

            if(m["directors"]){
                tvseries = this.addDirectors(JSON.parse(m["directors"]), schema, tvseries);
            }
            
            if(m["creators"]){
                tvseries = this.addCreators(JSON.parse(m["creators"]), schema, tvseries);
            }
            
            if(m["genres"]){
                tvseries = this.addGenres(JSON.parse(m["genres"]), schema, tvseries);
            }
            
            if(m["reviews"]){
                tvseries = this.addReviews(JSON.parse(m["reviews"]), schema, tvseries, m["url"]);
            }
            
            if(m["trailers"]){
                tvseries = this.addTrailers(JSON.parse(m["trailers"]), schema, tvseries);
            }
            

            serializer.addItem(tvseries, "TVSeries", schemaDescriptor);

        }
    }

    async episodesToProto(con, schema, serializer, schemaDescriptor){

        let q = `select 
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
                    `;

        
        let result = con.query(q).stream();
        const episodes = pEvent.iterator(result, 'data', {
            resolutionEvents: ['end']
        });

        for await (let m of episodes){
            let episode = new schema.TVEpisode();

            if(m["url"]){
                let url = new schema.UrlProperty();
                url.setUrl(m["url"]);
                episode.addUrl(url);
                episode.setId(m["url"]);
            }

            if(m["name"]){
                let name = new schema.NameProperty();
                name.setText(m["name"]);
                episode.addName(name);
            }

            if(m["image"]){
                let image = new schema.ImageProperty();
                image.setUrl(m["image"]);
                episode.addImage(image);
            }

            if(m["content_rating"]){
                let contentRating = new schema.ContentRatingProperty();
                contentRating.setText(m["name"]);
                episode.addContentRating(contentRating);
            }

            if(m["description"]){
                let description = new schema.DescriptionProperty();
                description.setText(m["description"]);
                episode.addDescription(description);
            }

            if(m["date_published"]){
                let datePublished = new schema.DatePublishedProperty();
                datePublished.setDate(this.addDate(m["date_published"], schema));
                episode.addDatePublished(datePublished);
            }

            if(m["keywords"]){
                let keywords = new schema.KeywordsProperty();
                keywords.setText(m["keywords"]);
                episode.addKeywords(keywords);
            }

            if(m["duration_minutes"]){
                let timeRequired = new schema.TimeRequiredProperty();
                timeRequired.setDuration(this.addDuration(m["duration_minutes"], schema));
                episode.addTimeRequired(timeRequired);
            }

            if(m["rating"]){
                let aggregateRatingProp = new schema.AggregateRatingProperty();
                let aggregateRating = new schema.AggregateRating();

                if(m["rating_count"]){
                    let ratingCount = new schema.RatingCountProperty();
                    ratingCount.setInteger(m["rating_count"]);
                    aggregateRating.addRatingCount(ratingCount);
                }

                if(m["rating"]){
                    let ratingValue = new schema.RatingValueProperty();
                    ratingValue.setNumber(m["rating"]);
                    aggregateRating.addRatingValue(ratingValue);
                }

                if(m["best_rating"]){
                    let bestRating = new schema.BestRatingProperty();
                    bestRating.setNumber(m["best_rating"]);
                    aggregateRating.addBestRating(bestRating);
                }

                if(m["worst_rating"]){
                    let worstRating = new schema.WorstRatingProperty();
                    worstRating.setNumber(m["worst_rating"]);
                    aggregateRating.addWorstRating(worstRating);
                }
                aggregateRatingProp.setAggregateRating(aggregateRating);
                episode.addAggregateRating(aggregateRatingProp);
            }

            if(m["actors"]){
                episode = this.addActors(JSON.parse(m["actors"]), schema, episode);
            }

            if(m["directors"]){
                episode = this.addDirectors(JSON.parse(m["directors"]), schema, episode);
            }
            
            if(m["creators"]){
                episode = this.addCreators(JSON.parse(m["creators"]), schema, episode);
            }
            
            if(m["genres"]){
                episode = this.addGenres(JSON.parse(m["genres"]), schema, episode);
            }
            
            if(m["reviews"]){
                episode = this.addReviews(JSON.parse(m["reviews"]), schema, episode, m["url"]);
            }
            
            if(m["trailers"]){
                episode = this.addTrailers(JSON.parse(m["trailers"]), schema, episode);
            }
            

            serializer.addItem(episode, "TVEpisode", schemaDescriptor);

        }
    }

    addActors(actors, schema, entity){        
        for(let a of actors){
            let actor = new schema.ActorProperty();
            let person = new schema.Person();

            if(a["url"]){
                let url = new schema.UrlProperty();
                url.setUrl(a["url"]);
                person.addUrl(url);
                person.setId(a["url"]);
            }

            if(a["name"]){
                let name = new schema.NameProperty();
                name.setText(a["name"]);
                person.addName(name);
            }
            actor.setPerson(person);
            entity.addActor(actor);
        }

        return entity;
    }

    addDirectors(directors, schema, entity){
        for(let a of directors){
            let director = new schema.DirectorProperty();
            let person = new schema.Person();

            if(a["url"]){
                let url = new schema.UrlProperty();
                url.setUrl(a["url"]);
                person.addUrl(url);
                person.setId(a["url"]);
            }

            if(a["name"]){
                let name = new schema.NameProperty();
                name.setText(a["name"]);
                person.addName(name);
            }
            director.setPerson(person);
            entity.addDirector(director);
        }

        return entity;
    }

    addCreators(creators, schema, entity){        
        for(let a of creators){
            let creator = new schema.CreatorProperty();
            
            if(a["type" ]== "PERSON"){
                let person = new schema.Person();

                if(a["url"]){
                    let url = new schema.UrlProperty();
                    url.setUrl(a["url"]);
                    person.addUrl(url);
                    person.setId(a["url"]);
                }
    
                if(a["name"]){
                    let name = new schema.NameProperty();
                    name.setText(a["name"]);
                    person.addName(name);
                }

                creator.setPerson(person);
            }
            else if(a["type"] == "ORGANIZATION"){
                let organization = new schema.Organization();

                if(a["url"]){
                    let url = new schema.UrlProperty();
                    url.setUrl(a["url"]);
                    organization.addUrl(url);
                    organization.setId(a["url"]);
                }
    
                if(a["name"]){
                    let name = new schema.NameProperty();
                    name.setText(a["name"]);
                    organization.addName(name);
                }
                creator.setOrganization(organization);
            }
            entity.addCreator(creator);

        }

        return entity;
    }

    addGenres(genres, schema, entity){
        for(let a of genres){
            let genre = new schema.GenreProperty();

            if(a["name"]){
                genre.setText(a["name"]);
            }

            entity.addGenre(genre);
        }

        return entity;
    }

    addReviews(reviews, schema, entity, url){
        for(let a of reviews){
            let reviewProp = new schema.ReviewProperty();
            let review = new schema.Review();

            if(a["author"]){
                let author = new schema.AuthorProperty();
                let person = new schema.Person();
                let name = new schema.NameProperty();
                name.setText(a["author"]);
                person.addName(name);
                author.setPerson(person);
                review.addAuthor(author);
            }

            if(a["date_created"]){
                let dateCreated = new schema.DateCreatedProperty();
                let dt = this.addDate(a["date_created"], schema);
                dateCreated.setDate(dt);
                review.addDateCreated(dateCreated);
            }

            if(a["language"]){
                let inLanguage = new schema.InLanguageProperty();
                inLanguage.setText(a["language"]);
                review.addInLanguage(inLanguage);
            }

            if(a["name"]){
                let name = new schema.NameProperty();
                name.setText(a["name"]);
                review.addName(name);
            }

            if(a["review_body"]){
                let reviewBody = new schema.ReviewBodyProperty();
                reviewBody.setText(a["review_body"]);
                review.addReviewBody(reviewBody);
            }

            if(a["rating"]){
                let reviewRating = new schema.ReviewRatingProperty();
                let rating = new schema.Rating();

                let ratingValue = new schema.RatingValueProperty();
                ratingValue.setNumber(parseFloat(a["rating"]));
                rating.addRatingValue(ratingValue);

                if(a["best_rating"]){
                    let bestRating = new schema.BestRatingProperty();
                    bestRating.setNumber(parseFloat(a["best_rating"]));
                    rating.addBestRating(bestRating);
                }

                if(a["worst_rating"]){
                    let worstRating = new schema.WorstRatingProperty();
                    worstRating.setNumber(parseFloat(a["worst_rating"]));
                    rating.addWorstRating(worstRating);
                }

                reviewRating.setRating(rating);
                review.addReviewRating(reviewRating);
            }

            let itemReviewed = new schema.ItemReviewedProperty();
            let creativeWork = new schema.CreativeWork();
            let urlProperty = new schema.UrlProperty();
            urlProperty.setUrl(url);
            creativeWork.addUrl(urlProperty);
            itemReviewed.setCreativeWork(creativeWork);

            review.addItemReviewed(itemReviewed);
            reviewProp.setReview(review);
            entity.addReview(reviewProp);
        }

        return entity;
    }

    addTrailers(trailers, schema, entity){
        for(let a of trailers){
            let trailer = new schema.TrailerProperty();
            let videoObject = new schema.VideoObject();

            if(a["name"]){
                let name = new schema.NameProperty();
                name.setText(a["name"]);
                videoObject.addName(name);
            }

            if(a["embed_url"]){
                let embedUrl = new schema.EmbedUrlProperty();
                embedUrl.setUrl(a["embed_url"]);
                videoObject.addEmbedUrl(embedUrl);
                videoObject.setId(a["embed_url"]);
            }

            if(a["thumbnail_url"]){
                let thumbnalUrl = new schema.ThumbnailUrlProperty();
                thumbnalUrl.setUrl(a["thumbnail_url"]);
                videoObject.addThumbnailUrl(thumbnalUrl);
            }

            if(a["description"]){
                let description = new schema.DescriptionProperty();
                description.setText(a["description"]);
                videoObject.addDescription(description);
            }

            if(a["upload_date"]){
                let uploadDate = new schema.UploadDateProperty();
                let dateObj = this.addDate(a["upload_date"], schema);
                uploadDate.setDate(dateObj);

                videoObject.addUploadDate(uploadDate);
            }

            trailer.setVideoObject(videoObject);
            entity.addTrailer(trailer);
        }

        return entity;
    }


    addDate(dateObj, schema){
        //Throws up lot of inconsisntent values. Needs to be taken care.
        if(typeof dateObj == "string"){
            dateObj = moment.utc(dateObj);
        }
        else{
            dateObj = moment.utc(dateObj.toISOString());
        }
        let dt = new schema.Date();
        dt.setYear(dateObj.year());
        dt.setMonth(dateObj.month()+1);
        dt.setDay(dateObj.date());
        return dt;
    }

    addDuration(durationMin, schema) {
        let duration = new schema.Duration();
        duration.setSeconds(durationMin * 60);
        return duration;
    }

    async generateFeed(con, schema, serializer, schemaDescriptor){

        await this.moviesToProto(con, schema, serializer, schemaDescriptor);
        await this.seriesToProto(con, schema, serializer, schemaDescriptor);
        await this.episodesToProto(con, schema, serializer, schemaDescriptor);

    }

}

module.exports.IMDBExample = IMDBExample;
