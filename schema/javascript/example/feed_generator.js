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
class IMDBExample{

    async moviesToProto(query, schema, serializer, schemaDescriptor){

        let q = `SELECT 
                    url, 
                    name , 
                    image , 
                    content_rating , 
                    description , 
                    date_published , 
                    keywords , 
                    duration_minutes , 
                    rating_count , 
                    rating , 
                    best_rating , 
                    worst_rating 
                    from movie;`;

        
        let movies = await query(q);

        for(let m of movies){
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

            
            movie = await this.addActors(query, schema, movie, m["url"]);
            movie = await this.addDirectors(query, schema, movie, m["url"]);
            movie = await this.addCreators(query, schema, movie, m["url"]);
            movie = await this.addGenres(query, schema, movie, m["url"]);
            movie = await this.addReviews(query, schema, movie, m["url"]);
            movie = await this.addTrailers(query, schema, movie, m["url"]);

            serializer.addItem(movie, "Movie", schemaDescriptor);

        }
    }

    async seriesToProto(query, schema, serializer, schemaDescriptor){

        let q = `SELECT 
                    url, 
                    name , 
                    image , 
                    content_rating , 
                    description , 
                    date_published , 
                    keywords , 
                    rating_count , 
                    rating , 
                    best_rating , 
                    worst_rating 
                    from series;`;

        
        let series = await query(q);

        for(let m of series){
            let series = new schema.TVSeries();

            if(m["url"]){
                let url = new schema.UrlProperty();
                url.setUrl(m["url"]);
                series.addUrl(url);
                series.setId(m["url"]);
            }

            if(m["name"]){
                let name = new schema.NameProperty();
                name.setText(m["name"]);
                series.addName(name);
            }

            if(m["image"]){
                let image = new schema.ImageProperty();
                image.setUrl(m["image"]);
                series.addImage(image);
            }

            if(m["content_rating"]){
                let contentRating = new schema.ContentRatingProperty();
                contentRating.setText(m["name"]);
                series.addContentRating(contentRating);
            }

            if(m["description"]){
                let description = new schema.DescriptionProperty();
                description.setText(m["description"]);
                series.addDescription(description);
            }

            if(m["date_published"]){
                let datePublished = new schema.DatePublishedProperty();
                datePublished.setDate(this.addDate(m["date_published"], schema));
                series.addDatePublished(datePublished);
            }

            if(m["keywords"]){
                let keywords = new schema.KeywordsProperty();
                keywords.setText(m["keywords"]);
                series.addKeywords(keywords);
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
                series.addAggregateRating(aggregateRatingProp);
            }

            
            series = await this.addActors(query, schema, series, m["url"]);
            series = await this.addDirectors(query, schema, series, m["url"]);
            series = await this.addCreators(query, schema, series, m["url"]);
            series = await this.addGenres(query, schema, series, m["url"]);
            series = await this.addReviews(query, schema, series, m["url"]);
            series = await this.addTrailers(query, schema, series, m["url"]);

            serializer.addItem(series, "TVSeries", schemaDescriptor);

        }
    }

    async episodesToProto(query, schema, serializer, schemaDescriptor){

        let q = `SELECT 
                    url, 
                    name , 
                    image , 
                    content_rating , 
                    description , 
                    date_published , 
                    keywords , 
                    duration_minutes , 
                    rating_count , 
                    rating , 
                    best_rating , 
                    worst_rating 
                    from episode;`;

        
        let episodes = await query(q);

        for(let m of episodes){
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

            
            episode = await this.addActors(query, schema, episode, m["url"]);
            episode = await this.addDirectors(query, schema, episode, m["url"]);
            episode = await this.addCreators(query, schema, episode, m["url"]);
            episode = await this.addGenres(query, schema, episode, m["url"]);
            episode = await this.addReviews(query, schema, episode, m["url"]);
            episode = await this.addTrailers(query, schema, episode, m["url"]);


            serializer.addItem(episode, "TVEpisode", schemaDescriptor);

        }
    }

    async addActors(query, schema, entity, url){
        let q = `SELECT url, name from actor where entity_url = ${JSON.stringify(url)};`
        let actors = await query(q);
        
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

    async addDirectors(query, schema, entity, url){
        let q = `SELECT url, name from director where entity_url = ${JSON.stringify(url)};`
        let directors = await query(q);
        
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

    async addCreators(query, schema, entity, url){
        let q = `SELECT url, name, type from creator where entity_url = ${JSON.stringify(url)};`
        let creators = await query(q);
        
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

    async addGenres(query, schema, entity, url){
        let q = `SELECT name from genre where entity_url = ${JSON.stringify(url)};`;

        let genres = await query(q);
        for(let a of genres){
            let genre = new schema.GenreProperty();

            if(a["name"]){
                genre.setText(a["name"]);
            }

            entity.addGenre(genre);
        }

        return entity;
    }

    async addReviews(query, schema, entity, url){
        let q = `SELECT 
                    author , 
                    date_created , 
                    language , 
                    name , 
                    review_body , 
                    rating , 
                    best_rating , 
                    worst_rating 
                from review where entity_url = ${JSON.stringify(url)};`;

        let reviews = await query(q);
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

    async addTrailers(query, schema, entity, url){
        let q = `SELECT 
                    name, 
                    embed_url, 
                    thumbnail_url , 
                    description , 
                    upload_date 
                from trailer where entity_url = ${JSON.stringify(url)};`;

        let trailers = await query(q);
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
        let dt = new schema.Date();
        dt.setYear(dateObj.getFullYear());
        dt.setMonth(dateObj.getMonth()+1);
        dt.setDay(dateObj.getDate());
        return dt;
    }

    addDuration(durationMin, schema) {
        let duration = new schema.Duration();
        duration.setSeconds(durationMin * 60);
        return duration;
    }

    async generateFeed(query, schema, serializer, schemaDescriptor){

        await this.moviesToProto(query, schema, serializer, schemaDescriptor);
        await this.seriesToProto(query, schema, serializer, schemaDescriptor);
        await this.episodesToProto(query, schema, serializer, schemaDescriptor);

    }

}

module.exports.IMDBExample = IMDBExample;