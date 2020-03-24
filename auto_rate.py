import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import json
import dbus
import time

# Note: The wait time probably varies depending on hardware, and how good spotify's implementation is. Also depends on Dbus. 
def parse_ratings(playlist_length):
    wait_time_in_secs = 0.3
    bus = dbus.SessionBus()
    spotify_mpris_id = 'org.mpris.MediaPlayer2.spotify'
    player = bus.get_object(spotify_mpris_id, '/org/mpris/MediaPlayer2')
    song_ratings = {}
    for i in range(playlist_length):
        metadata = player.Get('org.mpris.MediaPlayer2.Player',
                              'Metadata',
                              dbus_interface='org.freedesktop.DBus.Properties')
        rating = float(metadata['xesam:autoRating'])
        title = str(metadata['xesam:title'])
        player.Next(dbus_interface='org.mpris.MediaPlayer2.Player')
        print(f'title: {title}, rating: {rating}')
        song_ratings[title] = rating
        time.sleep(wait_time_in_secs)
    print("pre-sort")
    print(song_ratings)
    sorted_song_ratings = sorted(song_ratings.items(), key=lambda x: x[1])

    print("post sort")
    print(sorted_song_ratings)
    return sorted_song_ratings


def main():
    # Assumes that Credentials are set up as environment variables
    spotify = spotipy.Spotify(
        client_credentials_manager=SpotifyClientCredentials())
    playlist_id = 'spotify:playlist:2P5zEQaeWuplHLRK845geh'
    playlist_length = spotify.playlist(playlist_id)['tracks']['total']
    print(f"playlist length: {playlist_length}")
    parse_ratings(playlist_length)


if __name__ == '__main__':
    main()
