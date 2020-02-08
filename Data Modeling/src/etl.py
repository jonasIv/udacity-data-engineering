import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *


def process_song_file(cur, filepath):
    """
        Read JSON file form filepath and write artist data and song data to
        according tables in the database.

        cur -- Database cursor
        filepath -- Path to JSON file
    """
    # open song file
    df = pd.read_json(filepath, lines=True)

    # insert artist record
    artist_data = df[['artist_id', 'artist_name', 'artist_location', 'artist_latitude', 'artist_longitude']].values[0].tolist()
    cur.execute(artist_table_insert, artist_data)

    # insert song record
    song_data = df[['song_id', 'title', 'artist_id', 'year', 'duration']].values[0].tolist()
    cur.execute(song_table_insert, song_data)


def process_log_file(cur, filepath):
    """
        Read JSON file from filepath and write time data, user data and songplay
        data to according tables in the database.

        cur -- Database cursor
        filepath -- Path to JSON file
    """
    # open log file
    df = pd.read_json(filepath, lines=True)

    # filter by NextSong action
    df = df[df['page'] == 'NextSong']

    # convert timestamp column to datetime
    t = pd.to_datetime(df['ts'], unit='ms')

    # insert time data records
    time_data = []
    for entry in t:
        time_data.append([entry, entry.hour, entry.day, entry.week, entry.month, entry.year, entry.day_name()])
    column_labels = ['start_time', 'hour', 'day', 'week', 'month', 'year', 'weekday']
    time_df = pd.DataFrame.from_records(time_data, columns=column_labels)

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table
    user_df = df[['userId', 'firstName', 'lastName', 'gender', 'level']]

    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    # insert songplay records
    for index, row in df.iterrows():

        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()
        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        # insert songplay record
        songplay_data = (pd.to_datetime(row.ts, unit='ms'), int(row.userId), row.level, songid, artistid, row.sessionId, row.location, row.userAgent)
        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    """
        Read all JSON files from given directory (including files from
        subdirectories) and pass file content into callback function.

        cur -- Databse cursor
        conn -- Database connection
        filepath -- Path to directory of files
        func -- Callback function
    """
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    # Connect to database
    conn = psycopg2.connect("host=postgres-db dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    # Process data
    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    # Close connection
    conn.close()


if __name__ == "__main__":
    main()
