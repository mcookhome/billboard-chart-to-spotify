import billboard
import argparse
from util import spotify_api_helper
import re
import collections
import sys

DEFAULT_USERNAME = "mcookhome"

def run(chart_name, date):
    chart = billboard.ChartData(chart_name, date=date)
    sp = spotify_api_helper.create_spotify_instance(DEFAULT_USERNAME)
    track_uris = convert_chart_to_uri_list(sp, chart)
    playlist_name = chart_name + " from " + date
    playlist_id = spotify_api_helper.create_playlist(sp, DEFAULT_USERNAME, playlist_name)
    spotify_api_helper.add_tracks(sp, DEFAULT_USERNAME, playlist_id, track_uris)
    print("Otherwise, the playlist '" + playlist_name + "' should be created in your Spotify client!")

def run_with_access_token(chart_name, date, access_token):
    chart = billboard.ChartData(chart_name, date=date.encode('ascii','ignore'))
    sp = spotify_api_helper.create_spotify_instance_with_access_token(access_token)
    username = spotify_api_helper.get_username(sp)
    track_uris = convert_chart_to_uri_list(sp, chart)
    playlist_name = chart_name + " from " + date
    playlist = spotify_api_helper.create_playlist(sp, username, playlist_name)
    spotify_api_helper.add_tracks(sp, username, playlist["id"], track_uris)
    print("Otherwise, the playlist '" + playlist_name + "' should be created in your Spotify client!")
    return playlist["external_urls"]["spotify"]

def convert_chart_to_uri_list(sp, chart):
    track_uris = []
    count_not_found = 0
    chart_num = 1
    year = chart.date[0:4]
    print(year)
    for track in chart:
        print(str(chart_num) + ": ")
        print(track)
        name_query = re.sub(r" ?\([^)]+\)", "", track.title.lower())
        artist = re.sub('".*?"', '', track.artist.lower())
        artist = "".join(artist.split("*"))
        artist = "".join(artist.split("featuring "))
        name_and_artist_query = name_query + " - " + artist
        name_and_two_word_artist_query = name_query + " " + " ".join(artist.split(" ")[0:2])
        name_and_one_word_artist_query = name_query + " " + " ".join(artist.split(" ")[0:1])

        queries = [name_and_two_word_artist_query, name_and_one_word_artist_query, name_query, name_and_artist_query]
        queries = [query + " NOT instrumental NOT karaoke" for query in queries]
        full_results_for_queries = {}
        for query in queries:
            result = spotify_api_helper.search_billboard(sp, query)
            if len(result["tracks"]["items"]) != 0:
                retrieved_track = result["tracks"]["items"][0]
                value = {"name": retrieved_track["name"], "artists": retrieved_track["artists"][0]["name"]}
                if retrieved_track["uri"] not in full_results_for_queries:
                    value["count"] = 1
                    value["queries"] = [query]
                    full_results_for_queries[retrieved_track["uri"]] = value
                else:
                    #print(full_results_for_queries[retrieved_track["uri"]])
                    value["count"] = full_results_for_queries[retrieved_track["uri"]]["count"] + 1
                    value["queries"] = full_results_for_queries[retrieved_track["uri"]]["queries"]
                    value["queries"].append(query)
                    full_results_for_queries[retrieved_track["uri"]] = value
        print(str(full_results_for_queries))
        if not full_results_for_queries:
            count_not_found = count_not_found + 1
            print("Could not find a Spotify track for this track: " + name_query)
        else:
            chosen_track_uri = max(full_results_for_queries, key=lambda key: full_results_for_queries[key]["count"])
            track_uris.append(chosen_track_uri)
        chart_num = chart_num + 1
    print("Sorry, but I couldn't find " + str(count_not_found) + " tracks")
    return track_uris

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--date", type=str, required=True)
    parser.add_argument("-c", "--chart", type=str, default='hot-100')
    args = parser.parse_args()

    chart_name = 'hot-100'
    date = "2000-01-01"
    #run(chart_name, date)
    run(args.chart, args.date)
