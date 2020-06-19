# END To END Example Javascript
This directory contains an example on how to use the generated python schema and python serializer to generate data feed. The feed generated here is that of Movie, TVSeries and TVEpisodes.

The data dump is scraped from IMDB website and contains JSON-LD feed for different Movies, TVSeries and TVEpisodes.

## Components
- The IMDBSeeder class reads the data dump and seeds the database with data that is needed for simulating the environement where user has to fetch data from database and generate feed out of it.

- The IMDB Example class reads the data from the database and generates proto objects out of the data and returns and ItemList object.

- The JSONLDSerializer then serializes the proto object to JSON-LD feed used similar to how it is used in websites.

## Usage

 - `npm install` in the current directory.
 - `npm install` in the javascript serializer directory.
 - Create a new file named config.json.
 - Copy contents of config.example.json to config.json.
 - Fill the configuration settings inside config.json.
 - Copy the compiled schema to a file named schema_pb2.js in this directory.
 - Copy the JSON descriptor to a file named schema_descriptor.json in this directory.
 - `node index.js` Run the index file.