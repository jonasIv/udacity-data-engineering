# Data Modeling - Project 1
This is the first project of the Udacity Data Engineering Nano Degree. Its purpose is to...
- Apply concepts of data modeling with Postgres.
- Define fact and dimension tables for a star schema.
- Build an ETL pipeline using Python and SQL.

**Table of contents**

* [Context](#context)
* [Data](#data)
  - [Song Data](#song-data)
  - [Log Data](#log-data)
* [Database Schema](#database-schema)
  - [Fact Table](#fact-table)
  - [Dimension Tables](#dimension-tables)
* [Project Structure](#project-structure)
* [Docker, PostgreSQL, and Jupyter Notebook](#docker-postgresql-and-jupyter-notebook)
* [Running the pipeline](#running-the-pipeline)

## Context
From the project introduction:
> A startup called Sparkify wants to analyze the data they've been collecting on songs and user activity on their new music streaming app. The analytics team is particularly interested in understanding what songs users are listening to. Currently, they don't have an easy way to query their data, which resides in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app.

> They'd like a data engineer to create a Postgres database with tables designed to optimize queries on song play analysis, and bring you on the project. Your role is to create a database schema and ETL pipeline for this analysis. You'll be able to test your database and ETL pipeline by running queries given to you by the analytics team from Sparkify and compare your results with their expected results.

## Data

### Song Data
The song data is in JSON format and contains metadata about a song and the artist of that song. The files can be found in `data/song_data/`. Below is an example of the content of a song data file:
<table border="1" class="dataframe">
  <thead>
    <tr>
      <th></th>
      <th>num_songs</th>
      <th>artist_id</th>
      <th>artist_latitude</th>
      <th>artist_longitude</th>
      <th>artist_location</th>
      <th>artist_name</th>
      <th>song_id</th>
      <th>title</th>
      <th>duration</th>
      <th>year</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>AR7G5I41187FB4CE6C</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>London, England</td>
      <td>Adam Ant</td>
      <td>SONHOTT12A8C13493C</td>
      <td>Something Girls</td>
      <td>233.40363</td>
      <td>1982</td>
    </tr>
  </tbody>
</table>

### Log Data
The log data consists of log files in JSON format that simulate activity logs from a music streaming app. They files can be found in `data/log_data/`. Below is an example of the content of a log data file:
<table border="1" class="dataframe">
  <thead>
    <tr>
      <th></th>
      <th>artist</th>
      <th>auth</th>
      <th>firstName</th>
      <th>gender</th>
      <th>itemInSession</th>
      <th>lastName</th>
      <th>length</th>
      <th>level</th>
      <th>location</th>
      <th>method</th>
      <th>page</th>
      <th>registration</th>
      <th>sessionId</th>
      <th>song</th>
      <th>status</th>
      <th>ts</th>
      <th>userAgent</th>
      <th>userId</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Frumpies</td>
      <td>Logged In</td>
      <td>Anabelle</td>
      <td>F</td>
      <td>0</td>
      <td>Simpson</td>
      <td>134.47791</td>
      <td>free</td>
      <td>Philadelphia-Camden-Wilmington, PA-NJ-DE-MD</td>
      <td>PUT</td>
      <td>NextSong</td>
      <td>1.541044e+12</td>
      <td>455</td>
      <td>Fuck Kitty</td>
      <td>200</td>
      <td>1541903636796</td>
      <td>"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4...</td>
      <td>69</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Kenny G with Peabo Bryson</td>
      <td>Logged In</td>
      <td>Anabelle</td>
      <td>F</td>
      <td>1</td>
      <td>Simpson</td>
      <td>264.75057</td>
      <td>free</td>
      <td>Philadelphia-Camden-Wilmington, PA-NJ-DE-MD</td>
      <td>PUT</td>
      <td>NextSong</td>
      <td>1.541044e+12</td>
      <td>455</td>
      <td>By The Time This Night Is Over</td>
      <td>200</td>
      <td>1541903770796</td>
      <td>"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4...</td>
      <td>69</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Biffy Clyro</td>
      <td>Logged In</td>
      <td>Anabelle</td>
      <td>F</td>
      <td>2</td>
      <td>Simpson</td>
      <td>189.83138</td>
      <td>free</td>
      <td>Philadelphia-Camden-Wilmington, PA-NJ-DE-MD</td>
      <td>PUT</td>
      <td>NextSong</td>
      <td>1.541044e+12</td>
      <td>455</td>
      <td>God &amp; Satan</td>
      <td>200</td>
      <td>1541904034796</td>
      <td>"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4...</td>
      <td>69</td>
    </tr>
    <tr>
      <th>3</th>
      <td>None</td>
      <td>Logged In</td>
      <td>Lily</td>
      <td>F</td>
      <td>0</td>
      <td>Burns</td>
      <td>NaN</td>
      <td>free</td>
      <td>New York-Newark-Jersey City, NY-NJ-PA</td>
      <td>GET</td>
      <td>Home</td>
      <td>1.540621e+12</td>
      <td>456</td>
      <td>None</td>
      <td>200</td>
      <td>1541910841796</td>
      <td>"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebK...</td>
      <td>32</td>
    </tr>
    <tr>
      <th>4</th>
      <td>HIM</td>
      <td>Logged In</td>
      <td>Lily</td>
      <td>F</td>
      <td>1</td>
      <td>Burns</td>
      <td>212.06159</td>
      <td>free</td>
      <td>New York-Newark-Jersey City, NY-NJ-PA</td>
      <td>PUT</td>
      <td>NextSong</td>
      <td>1.540621e+12</td>
      <td>456</td>
      <td>Beautiful</td>
      <td>200</td>
      <td>1541910973796</td>
      <td>"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebK...</td>
      <td>32</td>
    </tr>
  </tbody>
</table>

## Database Schema
The schema is a star schema based around a fact table that represents the song plays. This allows Sparkify to analyze their songplay data accross different dimensions. For example:
- Top 50 of songs last month (or other time frame)
- Top artists in a given time frame
- Top albmus in a given time frame
- Most active users in a given time frame
- Map of active users
- Browsers/Devices being used
- Songplays per hour on a given day
- Compare behaviour of paid vs non-paid users

### Fact Table
#### songplays
Records in log data associated with song plays.
- songplay_id serial PRIMARY KEY
- start_time timestamp NOT NULL REFERENCES time(start_time)
- user_id int NOT NULL REFERENCES users(user_id)
- level varchar
- song_id varchar REFERENCES songs(song_id)
- artist_id varchar REFERENCES artists(artist_id)
- session_id int NOT NULL
- location varchar
- user_agent varchar


### Dimension Tables
#### users
Users in the app.
- user_id int PRIMARY KEY
- first_name varchar NOT NULL
- last_name varchar NOT NULL
- gender varchar
- level varchar NOT NULL

#### artists
Artists in music database.
- artist_id varchar PRIMARY KEY
- name varchar NOT NULL
- location varchar
- latitude float
- longitude float

#### songs
Songs in music database.
- song_id varchar PRIMARY KEY
- title varchar NOT NULL
- artist_id varchar NOT NULL REFERENCES artists (artist_id)
- year smallint NOT NULL
- duration numeric NOT NULL

#### time
Timestamps of records in songplays broken down into specific units.
- start_time timestamp PRIMARY KEY
- hour smallint
- day smallint
- week smallint
- month smallint
- year smallint
- weekday varchar
    
## Project Structure
- `src/data` - Directory with song data and log data.
- `src/create_tables.py` - Script for creating the database tables based on a star schema.
- `src/etl.ipynb` - Jupyter Notebook for researching ETL pipeline steps.
- `src/etl.py` - Script for running the ETL pipeline.
- `src/sql_queries.py` - Script that defines the database schema (used by `create_tables.py`).
- `src/test.ipynb` - Jupyter Notebook for checking the database content.
- `Dockerfile` - File is used for creating the Jupyter Notebook container.
- `docker-compose.yml` - File for launching the database and Jupyter Notebook.
- `postgres-data` - Local directory for the PostgreSQL Database file.

## Docker, PostgreSQL, and Jupyter Notebook
The project requires a PostgreSQL database and a Jupyter Notebook. The files include a `docker-compose` file that starts two containers, one for the database and one for the notebook. Files can be edited from the notebook or locally (they are synced to the notebook container).

First, make sure you have Docker installed. Then, run Docker Compose:
```bash
$ docker-compose up
```

## Running the pipeline
Open a new Terminal in the Jupyter Notebook. Then, change into the `work/` directory. Create the database tables by executing
```
$ python create-tables.py
```

To start the ETL script run
```bash
$ python etl.py
```
