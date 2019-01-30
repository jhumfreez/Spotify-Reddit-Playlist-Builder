import redditbot
import spotifybot
import json
import datetime


# reddit pull list from r/listentothis or r/music
# parse: [artist] [--|-] [song], ignore if contains '[discussion]', ignore [genre]
def make_playlist():
    subreddit = 'listentothis'
    track_id_list = []
    PLAYLIST_LIMIT = 100
    r = redditbot.RedditBot()
    sb = spotifybot.SpotifyBot()
    top_titles = r.get_top_media(subreddit)

    for title in top_titles:
        artist_track_pair = r.song_parse(title)
        if artist_track_pair:
            track_id = sb.get_track_id(artist_track_pair[0], artist_track_pair[1])
            # print('Song ID: ' + track_id)
            if track_id != '' and track_id not in track_id_list:
                track_id_list.append(track_id)
                results = sb.get_track(track_id)
                print('\t' + results['name'] + ' by ' + results['artists'][0]['name'])
        if len(track_id_list) == PLAYLIST_LIMIT:
            break
    # TO DO: HANDLE CONNECTION ERROR requests.exceptions.ConnectionError: ('Connection aborted.',
    # ConnectionResetError(10054, 'An existing connection was forcibly closed by the remote host', None, 10054, None))

    # backup
    timestamp = '{:%Y-%m-%d_%H_%M_%S}'.format(datetime.datetime.now())
    with open(subreddit + '_backup_' + timestamp + '.json', 'w') as outfile:
        json.dump(track_id_list, outfile)

    # create playlist
    sb.add_tracks_to_playlist(track_id_list[:PLAYLIST_LIMIT], 'r/' + subreddit + ' Bot Playlist')
    print('*' * 5 + 'completed! '.upper() + str(len(track_id_list)) + ' songs added.' + '*' * 5)


# add to playlist list if exists
def main():
    # r = redditbot.RedditBot()
    # r.save_top_pics('animemes')
    make_playlist()


if __name__ == "__main__":
    main()
