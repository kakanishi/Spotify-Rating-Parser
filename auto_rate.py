import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import json
import dbus
import time
import csv
from collections import defaultdict

# Note: The wait time probably varies depending on hardware, and how good spotify's implementation is. Also depends on Dbus. 
def parse_ratings(playlist_length):
    wait_time_in_secs = 0.3
    bus = dbus.SessionBus()
    spotify_mpris_id = 'org.mpris.MediaPlayer2.spotify'
    player = bus.get_object(spotify_mpris_id, '/org/mpris/MediaPlayer2')
    song_ratings = defaultdict(float)
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
    sorted_song_ratings = dict(sorted(song_ratings.items(), key=lambda x: x[1]))

    return sorted_song_ratings


def main():
    # Assumes that Credentials are set up as environment variables
    spotify = spotipy.Spotify(
        client_credentials_manager=SpotifyClientCredentials())
    playlist_id = 'spotify:playlist:6OY8LffwEltyoG4rb0kkVr'
    playlist = spotify.playlist(playlist_id)
    playlist_length = playlist['tracks']['total']
    print(f"playlist length: {playlist_length}")
    playlist_name = playlist['name']
    print(f"playlist_name: {playlist_name}")
    ratings = parse_ratings(playlist_length)
    print(len(ratings))
    with open('rating.csv', mode='w') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        print(ratings.items())
        writer.writerows(ratings.items())
if __name__ == '__main__':
    main()
