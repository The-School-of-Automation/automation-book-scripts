import spotipy
import spotipy.util as util

"""
We need to export the following environemt variables in our Terminal
    export SPOTIPY_CLIENT_ID='your-spotify-client-id' (e.g. 9462643b3a644d98b13bd1d57eb338ce)
    export SPOTIPY_CLIENT_SECRET='your-spotify-client-secret' (e.g. 806c0814622148bf891e24e4b1b3e3ab)
    export SPOTIPY_REDIRECT_URI='your-app-redirect-url' (http://localhost:8080 for testing)
"""

# create the spotipy instance with the read scope
# set a fixed username for now
username = "aowve1162mwuc9f56s3k3gxsu"
read_token = util.prompt_for_user_token(username, "user-library-read")
read_scoped_sp = spotipy.Spotify(auth=read_token)

def reduce_track_information(track_list):
    """
    Reduce the amount of information in the given list.
    Create a triplet of the track information from
    artist name, song name, and track id.

    Parametrs:
    track_list - dict of track lists of tracks returned by spotify

    Returns:
    List of tracks in the format (artist_name, song_name, track_id)
    """

    reduced_tracks = []
    tracks = [track["track"] for track in track_list["items"]]

    # extract the song name, artist name and track id
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
    List of, by the user, saved tracks with name and track_id
    """
    results = read_scoped_sp.current_user_saved_tracks()
    reduced_tracks = reduce_track_information(results)

    return reduced_tracks

def print_options():
    """
    Print the possible options
    """

    print("")
    print("0. List Saved Tracks")
    print("1. Add new Saved Track")
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
                print("Currently saved tracks:")
                tracks = read_saved_tracks()

                for track in tracks:
                    print(f"{track[0]} - {track[1]}")

            if choice == 1:
                # TODO add new track
                pass

            if choice == 2:
                # Stop the main loop
                running = False

        except ValueError as err:
            print(f"Invalid choice, please select a valid number... {err}")


if __name__ == "__main__":
    main()