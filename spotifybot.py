import spotipy
import spotipy.util as util
import spotipy.oauth2 as oauth2
import re
import os
import json


class SpotifyBot:

    def __init__(self):
        self.creds = {
                'spotify_cid': '',
                'spotify_secret': '',
                'spotify_uid': '',
                'spotify_redir_url': ''
        }
        self.setcreds(self.creds)

    def setcreds(self, creds):
        try:
            with open('spotifycreds.json') as data_file:
                data = json.load(data_file)
                creds['spotify_cid'] = data['SPOTIFY_CID']
                creds['spotify_secret'] = data['SPOTIFY_SECRET']
                creds['spotify_uid'] = data['SPOTIFY_UID']
                creds['spotify_redir_url'] = data['SPOTIFY_REDIR_URL']
        except IOError:
            print("Could not read file: creds.json")
        
    # REQUIRES USER AUTH
    def add_tracks_to_playlist(self, track_ids, playlist_name):
        scope = 'playlist-modify-private'
        token = util.prompt_for_user_token(self.creds['spotify_uid'], scope,
                                           client_id=self.creds['spotify_cid'],
                                           client_secret=self.creds['spotify_secret'],
                                           redirect_uri=self.creds['spotify_redir_url'])

        if token:
            sp = spotipy.Spotify(auth=token)
            sp.trace = False
            # create the playlist
            playlist = sp.user_playlist_create(self.creds['spotify_uid'], playlist_name, public=False)
            # add tracks
            sp.user_playlist_add_tracks(self.creds['spotify_uid'], playlist['id'], track_ids)
        else:
            print("Can't get token for " + self.creds['spotify_uid'])

    # # Pagenation example: 
    # def get_playlist_tracks(username,playlist_id):
    # results = sp.user_playlist_tracks(username,playlist_id)
    # tracks = results['items']
    # while results['next']:
    # results = sp.next(results)
    # tracks.extend(results['items'])
    # return tracks

    # https://developer.spotify.com/documentation/web-api/reference/search/search/
    def show_top(self):
        scope = 'user-top-read'
        token = util.prompt_for_user_token(self.creds['spotify_uid'], scope,
                                           client_id=self.creds['spotify_cid'],
                                           client_secret=self.creds['spotify_secret'],
                                           redirect_uri=self.creds['spotify_redir_url'])
        if token:
            sp = spotipy.Spotify(auth=token)
            sp.trace = False
            print('--- ' + 'My Top Artists' + ' ---')
            top_art = [n['name'] for n in sp.current_user_top_artists(time_range='long_term', limit=10)['items']]
            for i, name in enumerate(top_art):
                print(str(i + 1) + '\t' + name)

            print('--- ' + 'My Top Tracks' + ' ---')
            top_tracks = sp.current_user_top_tracks(time_range='long_term', limit=10)['items']
            for i, track in enumerate(top_tracks):
                print(str(i + 1) + '\t' + track['name'] + ' - ' + track['artists'][0]['name'])

    @staticmethod
    def _trim_string(s):
        s = s.lower()
        delimiter = ''
        s = re.sub(r'\W+', ' ', s)
        # Nobody does this part the same way so to hell with it
        featuring = [' feat', ' ft', ' featuring']
        for f in featuring:
            s = re.sub(f, delimiter, s)
        return s

    def get_track_id(self, artist, title):

        ccm = oauth2.SpotifyClientCredentials(self.creds['spotify_cid'], self.creds['spotify_secret'])
        # auth api object
        sp = spotipy.Spotify(client_credentials_manager=ccm)

        track_id = ''
        artist = self._trim_string(artist)
        title = self._trim_string(title)
        q1 = 'artist:' + artist
        q2 = 'track:' + title

        results = sp.search(q=artist + ' ' + title, limit=1, offset=0, type='track', market='US')
        # only if total > 0
        if results['tracks']['total'] > 0:
            track_id = results['tracks']['items'][0]['id']
        return track_id

    def get_track(self, track_id):
        ccm = oauth2.SpotifyClientCredentials(self.creds['spotify_cid'], self.creds['spotify_secret'])
        # auth api object
        sp = spotipy.Spotify(client_credentials_manager=ccm)

        return sp.track(track_id)

    # def get_currently_playing(self):
    #     results = ''
    #     ccm = oauth2.SpotifyClientCredentials(os.environ['SPOTIFY_CID'], os.environ['SECRET'])
    #     # get token
    #     token = ccm.get_access_token()
    #     # auth api object
    #     sp = spotipy.Spotify(client_credentials_manager=ccm)
    #     sp.trace = False
    #
    #     return sp.currently_playing()


def main():
    artist = 'Nujabes'
    title = 'City Lights (Ft. Pase Rock & Substantial)'

    print('*' * 5 + 'testing track search'.upper() + '*' * 5)

    sb = SpotifyBot()
    track_id = sb.get_track_id(artist, title)
    print('Song ID: ' + track_id)
    results = sb.get_track(track_id)
    print(results['name'] + ' by ' + results['artists'][0]['name'])

    print('*' * 5 + 'testing auth flow'.upper() + '*' * 5)
    sb.show_top()


if __name__ == "__main__":
    main()
