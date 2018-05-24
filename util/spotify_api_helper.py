import sys
import spotipy
import spotipy.util as util

DEFAULT_USERNAME = "mcookhome"
def create_spotify_instance(username):
    scope = 'playlist-modify-public user-library-read'

    token = util.prompt_for_user_token(username, scope)

    if token:
        return spotipy.Spotify(auth=token)
    else:
        print("Can't get token for", username)

def search_billboard(sp, query):
    print("Query: " + query)
    results = sp.search(query, limit=1, type='track')
    return results

def create_playlist(sp, username, playlist_name):
    result = sp.user_playlist_create(username, playlist_name)
    return result["id"]

def add_tracks(sp, username, playlist_id, tracks):
    result = sp.user_playlist_add_tracks(username, playlist_id, tracks)
    return result

def run(username):
    sp = create_spotify_instance(username)
    tracks = search_billboard(sp, "")
    playlist_id = create_playlist(sp, username, "blabaaaah")
    add_tracks(sp, username, playlist_id, tracks)

if __name__ == '__main__':
    main_username = DEFAULT_USERNAME
    if len(sys.argv) > 1:
        main_username = sys.argv[1]
    run(main_username)