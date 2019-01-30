import praw
import requests
import re


# https://stackoverflow.com/questions/419163/what-does-if-name-main-do
class RedditBot:

    def __init__(self):
        self.reddit = praw.Reddit('bot1', user_agent='bot1 user agent')

    # Get top n hot sorted titles
    def get_top_media(self, subreddit):
        top_list = []

        time_filter = ['all', 'day', 'hour', 'month', 'week', 'year']

        if subreddit == '':
            raise ValueError('Error: Subreddit not initialized')

        for tf in time_filter:
            print('*' * 3 + 'Gathering from: ' + tf.upper() + '*' * 3)
            for submission in self.reddit.subreddit(subreddit).top(tf):
                if submission.selftext == '' and submission.title not in top_list:
                    top_list.append(submission.title)
            self.reddit = praw.Reddit('bot1', user_agent='bot1 user agent')

        return top_list

    def save_top_pics(self, subreddit):
        if subreddit == '':
            raise ValueError('Error: Subreddit not initialized')

        pics_extensions = ['.png', '.jpg']
        # folder = r'C:\Users\rusty\Downloads'+subreddit

        i = 1
        for submission in self.reddit.subreddit(subreddit).top('week'):
            print(str(i) + '\t' + str(submission.score) + ' ' + submission.title)
            if submission.url[-4:] in pics_extensions:
                ftype = pics_extensions.index(submission.url[-4:])
                open(subreddit+'_'+str(i) + pics_extensions[ftype], 'wb').write(requests.get(submission.url).content)
            i += 1

    def _trim_string(self, s):
        s = s.lower()
        s = re.sub(r'\W+', ' ', s)
        return s

    # parse: [artist][-- | -][song]
    # parse titles from music subreddits, return tuple
    def song_parse(self, title):
        artist_title_pair = None
        delimiter = '-'
        # trim off the genre & year
        # # [!!}: Discussion posts result in an empty tuple
        trim_index = 0
        tag_flags = ['(', '[', '{']
        for c in title:
            if c in tag_flags:
                break
            else:
                trim_index += 1
        title = title[:trim_index]
        if '-' in title:
            # split double-dash, & dash
            if '--' in title:
                delimiter = '--'
            artist_title_pair = title.split(delimiter, 1)
            artist_title_pair[0] = self._trim_string(artist_title_pair[0])
            artist_title_pair[1] = self._trim_string(artist_title_pair[1])
        else:
            artist_title_pair = None
            # remove punctuations from tuple
        return artist_title_pair
        # return artist_title_pair


def main():
    r = RedditBot()
    top_titles = r.get_top_media('music')
    i = 1
    for title in top_titles:
        # print(str(i)+'\t'+title)
        artist_track_pair = r.song_parse(title)
        if artist_track_pair:
            print(artist_track_pair[0] + ' by ' + artist_track_pair[1])
        i += 1
    # r.music_title_parse()


if __name__ == "__main__":
    main()
