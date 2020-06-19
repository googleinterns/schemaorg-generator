const mysql = require('mysql');
const util = require('util');
const dump = require("./dump.json");
const parseIsoDuration = require('parse-iso-duration');
const moment = require('moment');

/**
 * IMDBSeeder is used to seed database with data needed for IMDBExample class to generate JSON-LD feed.
 * @class
 */
class IMDBSeeder {

    /**
     * Creates database that needs to be seeded.
     * @param  {Object} db_config The database configuration.
     * @return {Promise}      Promise that indicates complete execution of function.
     */
    async init(db_config){
        let con = mysql.createConnection({
            host: db_config.db_host,
            user: db_config.db_user,
            password: db_config.db_password
        });

        let query = util.promisify(con.query).bind(con);
        await query(`DROP DATABASE IF EXISTS ${db_config.db_name};`)
        await query(`CREATE DATABASE ${db_config.db_name};`)
        await query(`USE ${db_config.db_name};`)
        con.end();
            
    }

    /**
     * Creates tables that needs to be seeded.
     * @param  {Function} query The promisified version of mysql query function.
     * @return {Promise}      Promise that indicates complete execution of function.
     */
    async createTables(query) {

        let movieTable = "CREATE table movie (url varchar(200) primary key, name varchar(200), image varchar(200), content_rating varchar(10), description varchar(1000), date_published date, keywords varchar(200), duration_minutes int, rating_count int, rating float(4,2), best_rating float(4,2), worst_rating float(4,2));"
        let seriesTable = "CREATE table series (url varchar(200) primary key, name varchar(200), image varchar(200), content_rating varchar(10), description varchar(1000), date_published date, keywords varchar(200), rating_count int, rating float(4,2), best_rating float(4,2), worst_rating float(4,2));"
        let episodeTable = "CREATE table episode (url varchar(200) primary key, name varchar(200), image varchar(200), content_rating varchar(10), description varchar(1000), date_published date, keywords varchar(200), duration_minutes int, rating_count int, rating float(4,2), best_rating float(4,2), worst_rating float(4,2));"
        let genresTable = "CREATE table genre ( entity_url varchar(200),  name varchar(200) );"
        let actorTable = "CREATE table actor ( entity_url varchar(200), url varchar(200), name varchar(200) );"
        let directorTable = "CREATE table director ( entity_url varchar(200), url varchar(200), name varchar(200) );"
        let creatorTable = "CREATE table creator ( entity_url varchar(200), url varchar(200), name varchar(200), type enum('PERSON', 'ORGANIZATION'));"
        let reviewTable = "CREATE table review ( entity_url varchar(200), author varchar(200), date_created date, language varchar(20), name varchar(200), review_body varchar(20000), rating float(4,2), best_rating float(4,2), worst_rating float(4,2) );"
        let trailerTable = "CREATE table trailer( name varchar(200), embed_url varchar(200), thumbnail_url varchar(200), description varchar(1000), upload_date datetime, entity_url varchar(200) );"

        await query(movieTable);
        await query(seriesTable);
        await query(episodeTable);
        await query(genresTable);
        await query(actorTable);
        await query(directorTable);
        await query(creatorTable);
        await query(reviewTable);
        await query(trailerTable);
    }

    /**
     * Calls seedMovies, seedSeries and seedEpisodes to seed the database.
     * @param  {Function} query The promisified version of mysql query function.
     * @param  {Array} movieList The list of movies to be seeded.
     * @param  {Array} seriesList The list of series to be seeded.
     * @param  {Array} episodeList The list of episodes to be seeded.
     * @return {Promise}      Promise that indicates complete execution of function.
     */
    async seedDB(query, movieList, seriesList, episodeList) {
        await this.seedMovies(query, movieList);
        await this.seedSeries(query, seriesList);
        await this.seedEpisodes(query, episodeList);
    }

    /**
     * Seeds movies into the database.
     * @param  {Function} query The promisified version of mysql query function.
     * @param  {Array} movieList The list of movies to be seeded.
     * @return {Promise}      Promise that indicates complete execution of function.
     */
    async seedMovies(query, movieList){
        
        for(let i =0; i<movieList.length; i++) {
            let m = movieList[i];
            let q = `INSERT INTO movie values (
                    ${JSON.stringify(m["url"]) || "\"\""}, 
                    ${JSON.stringify(m["name"]) || "\"\""}, 
                    ${JSON.stringify(m["image"]) || "\"\""}, 
                    ${JSON.stringify(m["contentRating"]) || "\"\""}, 
                    ${JSON.stringify(m["description"]) || "\"\""}, 
                    ${JSON.stringify(m["datePublished"]) || "\"\""}, 
                    ${JSON.stringify(m["keywords"]) || "\"\""}, 
                    ${JSON.stringify(this.getDuration(m["duration"] || "PT0M"))}, 
                    ${JSON.stringify(m["aggregateRating"]["ratingCount"]) || "\"\""}, 
                    ${JSON.stringify(m["aggregateRating"]["ratingValue"]) || "\"\""}, 
                    ${JSON.stringify(m["aggregateRating"]["bestRating"]) || "\"\""}, 
                    ${JSON.stringify(m["aggregateRating"]["worstRating"]) || "\"\""}
                );`
            await query(q);

            if(m["genre"]){
                if(Array.isArray(m["genre"])){
                    for(let j = 0; j<m["genre"].length; j++){
                        await this.seedGenre(query, m["genre"][j], m["url"] || "\"\"");
                    }
                }
                else{
                    await this.seedGenre(query, m["genre"], m["url"] || "\"\"");
                }
            }

            if(m["actor"]){
                if(Array.isArray(m["actor"])){
                    for(let j = 0; j<m["actor"].length; j++){
                        await this.seedActor(query, m["actor"][j], m["url"] || "\"\"");
                    }
                }
                else{
                    await this.seedActor(query, m["actor"], m["url"] || "\"\"");
                }
            }

            if(m["director"]){
                if(Array.isArray(m["director"])){
                    for(let j = 0; j<m["director"].length; j++){
                        await this.seedDirector(query, m["director"][j], m["url"] || "\"\"");
                    }
                }
                else{
                    await this.seedDirector(query, m["director"], m["url"] || "\"\"");
                }
            }

            if(m["creator"]){
                if(Array.isArray(m["creator"])){
                    for(let j = 0; j<m["creator"].length; j++){
                        await this.seedCreator(query, m["creator"][j], m["url"] || "\"\"");
                    }
                }
                else{
                    await this.seedCreator(query, m["creator"], m["url"] || "\"\"");
                }
            }

            if(m["review"]){
                if(Array.isArray(m["review"])){
                    for(let j = 0; j<m["review"].length; j++){
                        await this.seedReview(query, m["review"][j], m["url"] || "\"\"");
                    }
                }
                else{
                    await this.seedReview(query, m["review"], m["url"] || "\"\"");
                }
            }

            if(m["trailer"]){
                if(Array.isArray(m["trailer"])){
                    for(let j = 0; j<m["trailer"].length; j++){
                        await this.seedTrailer(query, m["trailer"][j], m["url"] || "\"\"");
                    }
                }
                else{
                    await this.seedTrailer(query, m["trailer"], m["url"] || "\"\"");
                }
            }
        };
    }

    /**
     * Seeds series into the database.
     * @param  {Function} query The promisified version of mysql query function.
     * @param  {Array} seriesList The list of series to be seeded.
     * @return {Promise}      Promise that indicates complete execution of function.
     */
    async seedSeries(query, seriesList){
        
        for(let i =0; i<seriesList.length; i++) {
            let m = seriesList[i];
            let q = `INSERT INTO series values (
                    ${JSON.stringify(m["url"]) || "\"\""}, 
                    ${JSON.stringify(m["name"]) || "\"\""}, 
                    ${JSON.stringify(m["image"]) || "\"\""}, 
                    ${JSON.stringify(m["contentRating"]) || "\"\""}, 
                    ${JSON.stringify(m["description"]) || "\"\""}, 
                    ${JSON.stringify(m["datePublished"]) || "\"\""}, 
                    ${JSON.stringify(m["keywords"]) || "\"\""}, 
                    ${JSON.stringify(m["aggregateRating"]["ratingCount"]) || "\"\""}, 
                    ${JSON.stringify(m["aggregateRating"]["ratingValue"]) || "\"\""}, 
                    ${JSON.stringify(m["aggregateRating"]["bestRating"]) || "\"\""}, 
                    ${JSON.stringify(m["aggregateRating"]["worstRating"]) || "\"\""}
                );`
            await query(q);

            if(m["genre"]){
                if(Array.isArray(m["genre"])){
                    for(let j = 0; j<m["genre"].length; j++){
                        await this.seedGenre(query, m["genre"][j], m["url"] || "\"\"");
                    }
                }
                else{
                    await this.seedGenre(query, m["genre"], m["url"] || "\"\"");
                }
            }

            if(m["actor"]){
                if(Array.isArray(m["actor"])){
                    for(let j = 0; j<m["actor"].length; j++){
                        await this.seedActor(query, m["actor"][j], m["url"] || "\"\"");
                    }
                }
                else{
                    await this.seedActor(query, m["actor"], m["url"] || "\"\"");
                }
            }

            if(m["director"]){
                if(Array.isArray(m["director"])){
                    for(let j = 0; j<m["director"].length; j++){
                        await this.seedDirector(query, m["director"][j], m["url"] || "\"\"");
                    }
                }
                else{
                    await this.seedDirector(query, m["director"], m["url"] || "\"\"");
                }
            }

            if(m["creator"]){
                if(Array.isArray(m["creator"])){
                    for(let j = 0; j<m["creator"].length; j++){
                        await this.seedCreator(query, m["creator"][j], m["url"] || "\"\"");
                    }
                }
                else{
                    await this.seedCreator(query, m["creator"], m["url"] || "\"\"");
                }
            }

            if(m["review"]){
                if(Array.isArray(m["review"])){
                    for(let j = 0; j<m["review"].length; j++){
                        await this.seedReview(query, m["review"][j], m["url"] || "\"\"");
                    }
                }
                else{
                    await this.seedReview(query, m["review"], m["url"] || "\"\"");
                }
            }

            if(m["trailer"]){
                if(Array.isArray(m["trailer"])){
                    for(let j = 0; j<m["trailer"].length; j++){
                        await this.seedTrailer(query, m["trailer"][j], m["url"] || "\"\"");
                    }
                }
                else{
                    await this.seedTrailer(query, m["trailer"], m["url"] || "\"\"");
                }
            }
        };
    }

    /**
     * Seeds episodes into the database.
     * @param  {Function} query The promisified version of mysql query function.
     * @param  {Array} episodeList The list of episodes to be seeded.
     * @return {Promise}      Promise that indicates complete execution of function.
     */
    async seedEpisodes(query, episodeList){
        
        for(let i =0; i<episodeList.length; i++) {
            let m = episodeList[i];
            let q = `INSERT INTO episode values (
                    ${JSON.stringify(m["url"]) || "\"\"" }, 
                    ${JSON.stringify(m["name"]) || "\"\"" }, 
                    ${JSON.stringify(m["image"]) || "\"\"" }, 
                    ${JSON.stringify(m["contentRating"]) || "\"\"" }, 
                    ${JSON.stringify(m["description"]) || "\"\"" }, 
                    ${JSON.stringify(m["datePublished"]) || "\"\"" }, 
                    ${JSON.stringify(m["keywords"]) || "\"\"" }, 
                    ${JSON.stringify(this.getDuration(m["duration"] || "PT0M")) }, 
                    ${JSON.stringify(m["aggregateRating"]["ratingCount"]) || "\"\"" }, 
                    ${JSON.stringify(m["aggregateRating"]["ratingValue"]) || "\"\"" }, 
                    ${JSON.stringify(m["aggregateRating"]["bestRating"]) || "\"\"" }, 
                    ${JSON.stringify(m["aggregateRating"]["worstRating"]) || "\"\"" }
                );`
            await query(q);

            if(m["genre"]){
                if(Array.isArray(m["genre"])){
                    for(let j = 0; j<m["genre"].length; j++){
                        await this.seedGenre(query, m["genre"][j], m["url"] || "\"\"");
                    }
                }
                else{
                    await this.seedGenre(query, m["genre"], m["url"] || "\"\"");
                }
            }

            if(m["actor"]){
                if(Array.isArray(m["actor"])){
                    for(let j = 0; j<m["actor"].length; j++){
                        await this.seedActor(query, m["actor"][j], m["url"] || "\"\"");
                    }
                }
                else{
                    await this.seedActor(query, m["actor"], m["url"] || "\"\"");
                }
            }

            if(m["director"]){
                if(Array.isArray(m["director"])){
                    for(let j = 0; j<m["director"].length; j++){
                        await this.seedDirector(query, m["director"][j], m["url"] || "\"\"");
                    }
                }
                else{
                    await this.seedDirector(query, m["director"], m["url"] || "\"\"");
                }
            }

            if(m["creator"]){
                if(Array.isArray(m["creator"])){
                    for(let j = 0; j<m["creator"].length; j++){
                        await this.seedCreator(query, m["creator"][j], m["url"] || "\"\"");
                    }
                }
                else{
                    await this.seedCreator(query, m["creator"], m["url"] || "\"\"");
                }
            }

            if(m["review"]){
                if(Array.isArray(m["review"])){
                    for(let j = 0; j<m["review"].length; j++){
                        await this.seedReview(query, m["review"][j], m["url"] || "\"\"");
                    }
                }
                else{
                    await this.seedReview(query, m["review"], m["url"] || "\"\"");
                }
            }

            if(m["trailer"]){
                if(Array.isArray(m["trailer"])){
                    for(let j = 0; j<m["trailer"].length; j++){
                        await this.seedTrailer(query, m["trailer"][j], m["url"] || "\"\"");
                    }
                }
                else{
                    await this.seedTrailer(query, m["trailer"], m["url"] || "\"\"");
                }
            }
        };
    }

    /**
     * Insert genre into the database.
     * @param  {Function} query The promisified version of mysql query function.
     * @param  {String} genre The name of genre that needs to be inserted.
     * @param  {String} url The url of entity for which genre is being added.
     * @return {Promise}      Promise that indicates complete execution of function.
     */
    async seedGenre(query, genre, url){
        let q = `INSERT INTO genre values (
                    ${JSON.stringify(url) || "\"\""},
                    ${JSON.stringify(genre) || "\"\""}
                );`;

        await query(q);
    }

    /**
     * Insert actor into the database.
     * @param  {Function} query The promisified version of mysql query function.
     * @param  {Object} actor The actor that needs to be inserted.
     * @param  {String} url The url of entity for which actor is being added.
     * @return {Promise}      Promise that indicates complete execution of function.
     */
    async seedActor(query, actor, url){

        let q = `INSERT INTO actor values (
                    ${JSON.stringify(url) || "\"\""}, 
                    ${JSON.stringify(actor["url"]) || "\"\""}, 
                    ${JSON.stringify(actor["name"]) || "\"\""}
                );`

        await query(q);
    }

    /**
     * Insert director into the database.
     * @param  {Function} query The promisified version of mysql query function.
     * @param  {Object} director The director that needs to be inserted.
     * @param  {String} url The url of entity for which director is being added.
     * @return {Promise}      Promise that indicates complete execution of function.
     */
    async seedDirector(query, director, url){
        let q = `INSERT INTO director values (
                    ${JSON.stringify(url) || "\"\""}, 
                    ${JSON.stringify(director["url"]) || "\"\""}, 
                    ${JSON.stringify(director["name"]) || "\"\""}
                );`
                
        await query(q);
    }

    /**
     * Insert creator into the database.
     * @param  {Function} query The promisified version of mysql query function.
     * @param  {Object} creator The creator that needs to be inserted.
     * @param  {String} url The url of entity for which creator is being added.
     * @return {Promise}      Promise that indicates complete execution of function.
     */
    async seedCreator(query, director, url){
        let q = `INSERT INTO creator values (
                    ${JSON.stringify(url) || "\"\""}, 
                    ${JSON.stringify(director["url"]) || "\"\""}, 
                    ${JSON.stringify(director["name"]) || "\"\""},
                    ${JSON.stringify(director["@type"].toUpperCase()) || "\"\""}
                );`
                
        await query(q);
    }

    /**
     * Insert review into the database.
     * @param  {Function} query The promisified version of mysql query function.
     * @param  {Object} review The review that needs to be inserted.
     * @param  {String} url The url of entity for which review is being added.
     * @return {Promise}      Promise that indicates complete execution of function.
     */
    async seedReview(query, review, url){
        let q;
        if(review["reviewrating"]){
            q = `INSERT INTO review values (
                    ${JSON.stringify(url) || "\"\""}, 
                    ${JSON.stringify(review["author"]["name"]) || "\"\""}, 
                    ${JSON.stringify(review["dateCreated"]) || "\"\""}, 
                    ${JSON.stringify(review["inLanguage"]) || "\"\""}, 
                    ${JSON.stringify(review["name"]) || "\"\""}, 
                    ${JSON.stringify(review["reviewBody"]) || "\"\""}, 
                    ${JSON.stringify(review["reviewRating"]["ratingValue"]) || 0}, 
                    ${JSON.stringify(review["reviewRating"]["bestRating"]) || 0}, 
                    ${JSON.stringify(review["reviewRating"]["worstRating"]) || 0}
                );`
        }
        else{
            q = `INSERT INTO review (entity_url, author, date_created, language, name, review_body) 
                values (
                    ${JSON.stringify(url) || "\"\""}, 
                    ${JSON.stringify(review["author"]["name"]) || "\"\""}, 
                    ${JSON.stringify(review["dateCreated"]) || "\"\""}, 
                    ${JSON.stringify(review["inLanguage"]) || "\"\""}, 
                    ${JSON.stringify(review["name"]) || "\"\""}, 
                    ${JSON.stringify(review["reviewBody"]) || "\"\""}
                );`
        }

        await query(q);
    }

    /**
     * Insert trailer into the database.
     * @param  {Function} query The promisified version of mysql query function.
     * @param  {Object} trailer The trailer that needs to be inserted.
     * @param  {String} url The url of entity for which trailer is being added.
     * @return {Promise}      Promise that indicates complete execution of function.
     */
    async seedTrailer(query, trailer, url) {
        let q = `INSERT INTO trailer values( 
                    ${JSON.stringify(trailer["name"]) || "\"\""}, 
                    ${JSON.stringify(trailer["embedUrl"]) || "\"\""}, 
                    ${JSON.stringify(trailer["thumbnailUrl"]) || "\"\""}, 
                    ${JSON.stringify(trailer["description"]) || "\"\""}, 
                    ${JSON.stringify(this.getDateTime(trailer["uploadDate"])) || "\"\""},
                    ${JSON.stringify(url) || "\"\""}
                )`;
        
        await query(q);
    }

    /**
     * Parse ISO8601 duration string and return duration as minutes.
     * @param  {String} durationString The ISO8601 duration string.
     * @return {Int}      Duration as minutes.
     */
    getDuration(durationString){
        return parseIsoDuration(durationString)/(1000*60);
    }

     /**
     * Parse ISO8601 datetime string and return ISO9075 datetime string.
     * @param  {String} durationString The ISO8601 datetime string.
     * @return {String}      The ISO9075 datetime string.
     */
    getDateTime(datetimeString) {
        let dt = moment(datetimeString);
        let dtString = dt.format('YYYY-MM-DD HH:MM:SS')

        return dtString;
    }
}

module.exports.IMDBSeeder = IMDBSeeder;
