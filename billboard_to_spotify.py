import billboard
from util import spotify_api_helper
import re

DEFAULT_USERNAME = "mcookhome"

def run(chart_name, date):
    chart = billboard.ChartData(chart_name, date=date)
    sp = spotify_api_helper.create_spotify_instance(DEFAULT_USERNAME)
    track_uris = convert_chart_to_uri_list(sp, chart)
    playlist_name = chart_name + " from " + date
    playlist_id = spotify_api_helper.create_playlist(sp, DEFAULT_USERNAME, playlist_name)
    spotify_api_helper.add_tracks(sp, DEFAULT_USERNAME, playlist_id, track_uris)
    print("Otherwise, the playlist '" + playlist_name + "' should be created in your Spotify client!")

def convert_chart_to_uri_list(sp, chart):
    track_uris = []
    count_not_found = 0
    for track in chart:
        name_query = re.sub(r" ?\([^)]+\)", "", track.title)
        name_and_artist_query = name_query + " - " + track.artist
        name_and_partial_artist_query = name_query + " " + " ".join(track.artist.split(" ")[0:2])
        #print(name_and_artist_query)
        queries = [name_query, name_and_artist_query, name_and_partial_artist_query]
        all_results = [{"query": query, "result" : spotify_api_helper.search_billboard(sp, query)} for query in queries]
        for entry in all_results:
            result = entry["result"]
            query = entry["query"]
            print(query)
            if len(result["tracks"]["items"]) == 1:
                print(query + ": " + result["tracks"]["items"][0]["name"])

        #print(all_results)
        results = spotify_api_helper.search_billboard(sp, name_and_partial_artist_query)
        if len(results["tracks"]["items"]) == 0:
            print("Could not find a Spotify track for this query: " + name_and_partial_artist_query)
            count_not_found = count_not_found + 1
        else:
            track = results["tracks"]["items"][0]
            track_name = track["name"]
            artist_name = track["artists"][0]["name"]
            #print(track_name + " - " + artist_name)
            track_uris.append(track["uri"])
    print("Sorry, but I couldn't find " + str(count_not_found) + " tracks")
    return track_uris

if __name__ == '__main__':
    chart_name = 'hot-100'
    date = "2000-01-01"
    run(chart_name, date)
