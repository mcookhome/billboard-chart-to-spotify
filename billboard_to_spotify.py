import billboard
from util import spotify_api_helper
import re

DEFAULT_USERNAME = "mcookhome"

def run(chart_name, date):
    chart = billboard.ChartData(chart_name, date=date)
    sp = spotify_api_helper.create_spotify_instance(DEFAULT_USERNAME)
    count_not_found = 0
    track_uris = []
    for track in chart:
        query = re.sub(r" ?\([^)]+\)", "", track.title) + " - " + track.artist
        #print(query)
        results = spotify_api_helper.search_billboard(sp, query)
        if len(results["tracks"]["items"]) == 0:
            print("Could not find a Spotify track for this query: " + query)
            count_not_found = count_not_found + 1
        else:
            track = results["tracks"]["items"][0]
            track_name = track["name"]
            artist_name = track["artists"][0]["name"]
            #print(track_name + " - " + artist_name)
            track_uris.append(track["uri"])
    playlist_name = chart_name + " from " + date
    playlist_id = spotify_api_helper.create_playlist(sp, DEFAULT_USERNAME, playlist_name)
    spotify_api_helper.add_tracks(sp, DEFAULT_USERNAME, playlist_id, track_uris)
    print("Sorry, but I couldn't find " + str(count_not_found) + " tracks")
    print("Otherwise, the playlist '" + playlist_name + "' should be created in your Spotify client!")


if __name__ == '__main__':
    chart_name = 'hot-100'
    date = "1978-08-25"
    run(chart_name, date)
