import spotipy
import spotipy.util as util

"""
We need to export the following environemt variables in our Terminal
    export SPOTIPY_CLIENT_ID='your-spotify-client-id' (e.g. 34a58b3a5a924c99be3bc36c925bc814)
    export SPOTIPY_CLIENT_SECRET='your-spotify-client-secret' (e.g. 7facae18b589421298fcb82f76440799)
    export SPOTIPY_REDIRECT_URI='your-app-redirect-url' (http://localhost:8080 for testing)
"""

# create the spotipy instance with the read and write scope
# set a fixed username for now
username = "aowve1162mwuc9f56s3k3gxsu"
read_token = util.prompt_for_user_token(username, "user-library-read")
read_scoped_sp = spotipy.Spotify(auth=read_token)

write_token = util.prompt_for_user_token(username, "user-library-modify")
write_scoped_sp = spotipy.Spotify(auth=write_token)

def reduce_track_information(track_list):
    """
    Reduce the amount of information in the given list.
    Creates a triplet of the track information from
    artist name, song name, and track id.

    Parameters:
    track_list - List of tracks returned by spotify

    Returns:
    List of tracks in the format (artist_name, song_name, track_id
    """

    reduced_tracks = []
    tracks = track_list.get("tracks", None)

    # get the list of tracks, handle search and show
    if tracks is not None:
        # format of search tracks
        tracks = tracks["items"]
    else:
        # format of get saved tracks
        tracks = [track["track"] for track in track_list["items"]]

    # only extract the song name, artist name and track id
    for track in tracks:
        track_name = track["name"]
        artist_name = track["artists"][0]["name"]
        track_id = track["id"]

        reduced_tracks.append((
            artist_name,
            track_name,
            track_id
        ))

    return reduced_tracks


def read_saved_tracks():
    """
    Get a list of tracks currently saved by the user

    Returns:
    List of, by the user, saved tracks with name and track id
    """
    
    results = read_scoped_sp.current_user_saved_tracks()
    tracks = reduce_track_information(results)
    
    return tracks


def get_tracks_for_search_text(search_input):
    """
    Get tracks that match the given text and map them to triplets
    containing the artist, song, and track id

    Parameters:
    search_text - Name of the song and/or artist to be searched for

    Returns:
    List of Triplets with artist and song names and track ids
    """

    result = read_scoped_sp.search(search_input)
    tracks = reduce_track_information(result)

    return tracks


def add_saved_track_by_id(track_id):
    """
    Add the track with the given id to the saved tracks list.

    Parameters:
    track_id - id of the to be added track
    """

    write_scoped_sp.current_user_saved_tracks_add(tracks=[track_id])


def add_selected_track(found_tracks, selection):
    """
    Parse the given selection from the user and add the given track_id
    tot the users saved track list
    """

    try:
        parsed_select = int(selection)
        selected_track = found_tracks[parsed_select]
        track_name = f"{selected_track[0]} - {selected_track[1]}"

        print(f"Adding {track_name} to your saved tracks...")
        # add the selected track using the track_id saved in the third place (2)
        add_saved_track_by_id(selected_track[2])

    except ValueError as err:
        print(f"Invalid selection, please select a valid number... {err}")


def print_options():
    """
    Prints the possible choices
    """

    print("")
    print("0. List Saved Tracks")
    print("1. Add to Saved Tracks")
    print("2. Exit")


def main():
    """
    Main "game" loop to handle user input
    """

    running = True

    while running:
        print_options()
        user_choice = input("What do you want to do (choose number)?\n")

        try:
            choice = int(user_choice)

            if choice == 0:
                print(f"Currently saved tracks:")
                tracks = read_saved_tracks()

                for track in tracks:
                    print(f"{track[0]} - {track[1]}")

            if choice == 1:
                search_input = input("What track do you want to add?\n")
                found_tracks = get_tracks_for_search_text(search_input)

                for index, track in enumerate(found_tracks):
                    track_name = f"{track[0]} - {track[1]}"
                    print(f"{index}. {track_name}")

                selection = input("Give the number of the right track: ")
                add_selected_track(found_tracks, selection)

            if choice == 2:
                # Stop the main loop
                running = False

        except ValueError as err:
            print(f"Invalid choice, please select a valid number... {err}")


if __name__ == "__main__":
    main()