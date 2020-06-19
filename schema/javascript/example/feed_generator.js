class IMDBExample{

    constructor(){
        this.position = 1;
    }

    async moviesToProto(query, schema, itemList){

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
            let itemListElement = new schema.ItemListElementProperty();
            let listItem = new schema.ListItem();

            let position = new schema.PositionProperty();
            position.setInteger(this.position);
            this.position = this.position + 1;

            listItem.addPosition(position);

            let item = new schema.ItemProperty();
            let movie = new schema.Movie();

            if(m["url"]){
                let url = new schema.UrlProperty();
                url.setUrl(m["url"]);
                movie.addUrl(url);
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

            // TODO: Duration

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


            item.setMovie(movie);
            listItem.addItem(item);
            itemListElement.setListItem(listItem);
            itemList.addItemListElement(itemListElement);

        }
        return itemList;
    }

    async seriesToProto(query, schema, itemList){

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
            let itemListElement = new schema.ItemListElementProperty();
            let listItem = new schema.ListItem();

            let position = new schema.PositionProperty();
            position.setInteger(this.position);
            this.position = this.position + 1;

            listItem.addPosition(position);

            let item = new schema.ItemProperty();
            let series = new schema.TVSeries();

            if(m["url"]){
                let url = new schema.UrlProperty();
                url.setUrl(m["url"]);
                series.addUrl(url);
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

            // TODO: Duration

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


            item.setTvSeries(series);
            listItem.addItem(item);
            itemListElement.setListItem(listItem);
            itemList.addItemListElement(itemListElement);

        }
        return itemList;
    }

    async episodesToProto(query, schema, itemList){

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
            let itemListElement = new schema.ItemListElementProperty();
            let listItem = new schema.ListItem();

            let position = new schema.PositionProperty();
            position.setInteger(this.position);
            this.position = this.position + 1;

            listItem.addPosition(position);

            let item = new schema.ItemProperty();
            let episode = new schema.TVEpisode();

            if(m["url"]){
                let url = new schema.UrlProperty();
                url.setUrl(m["url"]);
                episode.addUrl(url);
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

            // TODO: Duration

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


            item.setTvEpisode(episode);
            listItem.addItem(item);
            itemListElement.setListItem(listItem);
            itemList.addItemListElement(itemListElement);

        }
        return itemList;
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

    async generateFeed(query, schema){
        let itemList = new schema.ItemList();

        itemList = await this.moviesToProto(query, schema, itemList);
        itemList = await this.seriesToProto(query, schema, itemList);
        itemList = await this.episodesToProto(query, schema, itemList);

        return itemList;
    }

}

module.exports.IMDBExample = IMDBExample;
